from flask import Flask, render_template, request, jsonify
import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io, base64, os
from threading import Lock
from collections import deque

# --------------------
# CONFIG
# --------------------
DATA_DIR = "testdata"
FALLBACK_CSV = os.path.join(DATA_DIR, "P1.csv")
PERSON_PATTERN = "P{}.csv"
PERSON_COUNT = 5
BULK_THRESHOLD = 3000
BULK_FREQ = 3
RISK_THRESHOLD = 40
CSV_LOCK = Lock()

# Expected CSV columns: txn_id, uid, from, to, amount

app = Flask(__name__, template_folder="template1")

# --------------------
# IN-MEM DATA
# --------------------
data_by_person = {}
combined_df = pd.DataFrame()
G = nx.DiGraph()

# --------------------
# HELPERS
# --------------------
def normalize_df(df):
    expected = ['txn_id','uid','from','to','amount']
    for c in expected:
        if c not in df.columns:
            df[c] = ""
    return df[expected].astype(str)

def load_data():
    global data_by_person, combined_df
    data_by_person = {}
    if os.path.isdir(DATA_DIR):
        found_any = False
        for i in range(1, PERSON_COUNT+1):
            path = os.path.join(DATA_DIR, PERSON_PATTERN.format(i))
            if os.path.isfile(path):
                df = pd.read_csv(path, dtype=str)
                df = normalize_df(df)
                df['person'] = f"P{i}"
                data_by_person[f"P{i}"] = df
                found_any = True
        if not found_any and os.path.isfile(FALLBACK_CSV):
            df = pd.read_csv(FALLBACK_CSV, dtype=str)
            df = normalize_df(df)
            df['person'] = "P_all"
            data_by_person["P_all"] = df
    else:
        if os.path.isfile(FALLBACK_CSV):
            df = pd.read_csv(FALLBACK_CSV, dtype=str)
            df = normalize_df(df)
            df['person'] = "P_all"
            data_by_person["P_all"] = df

    if data_by_person:
        combined_df = pd.concat(list(data_by_person.values()), ignore_index=True)
    else:
        combined_df = pd.DataFrame(columns=['txn_id','uid','from','to','amount','person'])

    if not combined_df.empty:
        combined_df['amount'] = pd.to_numeric(combined_df['amount'], errors='coerce').fillna(0)


def build_graph():
    global G
    G = nx.DiGraph()
    if combined_df.empty:
        return
    accounts = pd.unique(combined_df[['from','to']].values.ravel())
    for a in accounts:
        if a != '':
            G.add_node(a)
    for _, r in combined_df.iterrows():
        u = r['from']; v = r['to']
        if u == '' or v == '':
            continue
        if not G.has_edge(u, v):
            G.add_edge(u, v, txns=[])
        G[u][v]['txns'].append({
            'txn_id': r['txn_id'],
            'uid': r.get('uid',''),
            'amount': float(r['amount']),
            'person': r.get('person', '')
        })

# --------------------
# TXN ID GENERATOR
# --------------------
def generate_txn_id_for_person(person):
    """Generate T-prefix txn_id based on person P1..P5"""
    prefix = person[1]  # 'P1' -> '1'
    person_txns = combined_df[combined_df['person']==person]['txn_id'].tolist()
    person_txns = [t for t in person_txns if t.startswith(f"T{prefix}")]
    if not person_txns:
        return f"T{prefix}001"
    last_num = max([int(t[1:]) for t in person_txns])
    return f"T{last_num+1:04d}"

# --------------------
# FRAUD DETECTION
# --------------------
def fraud_scores():
    if combined_df.empty:
        return {}
    df = combined_df.copy()
    stats = df.groupby('from')['amount'].agg(['mean','std','count']).fillna(0)

    z_scores = {}
    spike_flags = {}
    for _, r in df.iterrows():
        sender = r['from']
        amt = r['amount']
        
        #z-score
        if sender not in stats.index:
            continue
        m, s = stats.loc[sender,'mean'], stats.loc[sender,'std']
        if s > 0:
            z = abs((amt - m)/s)
            z_scores[sender] = max(z_scores.get(sender, 0), z)

        #Detect spike
        if m > 0 and amt > 3*m:
            spike_flags[sender] = 1

    #bulk transactions
    bulk_flags = {}
    large = df[df['amount'] >= BULK_THRESHOLD]
    bulk_counts = large.groupby('from').size()
    for acc, cnt in bulk_counts.items():
        bulk_flags[acc] = 1 if cnt >= BULK_FREQ else 0

    #centrality
    core = nx.degree_centrality(G) if G.number_of_nodes() else {}

    scores = {}
    for n in G.nodes():
        z = z_scores.get(n, 0)
        z_norm = min(z/5, 1)
        c = core.get(n, 0)
        b = bulk_flags.get(n, 0)
        sp = spike_flags.get(n, 0)
        score = (0.45*z_norm + 0.25*c + 0.2*b + 0.1*sp) * 100
        scores[n] = round(score, 2)
    return scores

# --------------------
# TRACE PATH
# --------------------
def trace_path(source, target):
    if combined_df.empty or source=="" or target=="":
        return None
    if source not in G.nodes() or target not in G.nodes():
        return None

    df_sorted = combined_df.reset_index(drop=True).copy()
    df_sorted['txn_idx'] = df_sorted.index.astype(int)

    out_map = {}
    for _, r in df_sorted.iterrows():
        frm = r['from']; to = r['to']
        if frm == '' or to == '':
            continue
        out_map.setdefault(frm, []).append((int(r['txn_idx']), to, r['txn_id']))

    q = deque()
    q.append((source, -1, [source]))
    visited = set()

    while q:
        node, last_idx, path_nodes = q.popleft()
        for txn_idx, to_acc, txnid in out_map.get(node, []):
            if txn_idx <= last_idx:
                continue
            new_path = path_nodes + [to_acc]
            if to_acc == target:
                return new_path
            state = (to_acc, txn_idx)
            if state in visited:
                continue
            visited.add(state)
            q.append((to_acc, txn_idx, new_path))
    return None

# --------------------
# LOOKUP TXN
# --------------------
def txn_lookup(txn_id=None):
    if combined_df.empty or not txn_id:
        return None
    row = combined_df[combined_df['txn_id'] == str(txn_id)]
    if not row.empty:
        return row.iloc[0].to_dict()
    return None

# --------------------
# DRAW GRAPH
# --------------------
def draw_graph_image(highlight_path=None, person=None):
    plt.figure(figsize=(8,6))
    ax = plt.gca()
    subG = G
    if person and person in data_by_person:
        df = data_by_person[person]
        nodes = set(df['from'].tolist() + df['to'].tolist())
        subG = G.subgraph(nodes).copy()
    pos = nx.spring_layout(G, seed=42)
    path_pairs = set()
    if highlight_path and len(highlight_path)>=2:
        for a,b in zip(highlight_path, highlight_path[1:]):
            path_pairs.add((a,b))

    node_colors = []
    shared_txns = set()
    for node in subG.nodes():
        if highlight_path and node in highlight_path:
            node_colors.append('orange')
        else:
            node_colors.append('skyblue')

    edge_colors = []
    edge_widths = []
    for u,v in subG.edges():
        if (u,v) in path_pairs:
            edge_colors.append('orange')
            edge_widths.append(3)
        else:
            edge_colors.append('gray')
            edge_widths.append(1)

    nx.draw(subG, pos=pos, ax=ax, with_labels=True, node_color=node_colors,
            node_size=800, edge_color=edge_colors, width=edge_widths, arrows=True, arrowsize=18)

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    return 'data:image/png;base64,' + base64.b64encode(img.getvalue()).decode()

# --------------------
# APPEND TXN
# --------------------
def append_transaction_to_person(df_row, person_key):
    if person_key in data_by_person and person_key.startswith('P'):
        path = os.path.join(DATA_DIR, PERSON_PATTERN.format(person_key[1:]))
    else:
        path = FALLBACK_CSV
    if os.path.dirname(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    CSV_LOCK.acquire()
    try:
        exists = os.path.isfile(path)
        row_df = pd.DataFrame([df_row])
        row_df = normalize_df(row_df)
        if exists:
            row_df.to_csv(path, mode='a', header=False, index=False)
        else:
            row_df.to_csv(path, mode='w', header=True, index=False)
    finally:
        CSV_LOCK.release()

# --------------------
# INITIAL LOAD
# --------------------
load_data()
build_graph()

# --------------------
# ROUTES
# --------------------
@app.route("/")
def index():
    persons = sorted([k for k in data_by_person.keys() if k.startswith('P')]) or ["P_all"]
    graph_img = draw_graph_image()
    return render_template("faihtml.html", persons=persons, graph_img=graph_img)

@app.route("/graph/<person>")
def graph_person(person):
    img = draw_graph_image(person=person if person!="all" else None)
    return jsonify({"img": img})

@app.route("/txn_search", methods=["POST"])
def txn_search():
    txn_id = request.form.get("txn_id","").strip()
    res = txn_lookup(txn_id=txn_id if txn_id else None)
    return jsonify({"result": res})

@app.route("/trace", methods=["POST"])
def trace():
    source = request.form.get("source","").strip()
    target = request.form.get("target","").strip()
    path = trace_path(source, target)
    img = draw_graph_image(highlight_path=path) if path else None
    return jsonify({"path": path, "img": img})

@app.route("/fraud", methods=["GET"])
def fraud():
    scores = fraud_scores()
    suspicious = {acc: sc for acc, sc in scores.items() if sc >= RISK_THRESHOLD}
    return jsonify({"scores": scores, "suspicious": suspicious})

@app.route("/add_txn", methods=["POST"])
def add_txn():
    txn_id = request.form.get("txn_id", "").strip()
    uid = request.form.get("uid", "").strip()
    frm = request.form.get("from", "").strip()
    to = request.form.get("to", "").strip()
    amount = request.form.get("amount", "0").strip()
    person = request.form.get("person", "").strip()
    if person == "": person = "P_all"

    # Auto-generate txn_id if empty
    if txn_id == "":
        txn_id = generate_txn_id_for_person(person)

    new_row = {
        'txn_id': txn_id,
        'uid': uid or "",
        'from': frm,
        'to': to,
        'amount': str(amount)
    }
    append_transaction_to_person(new_row, person)
    load_data()
    build_graph()
    img = draw_graph_image(person=person if person in data_by_person else None)
    return jsonify({"status":"ok", "img": img})

# --------------------
# RUN
# --------------------
if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(debug=True)