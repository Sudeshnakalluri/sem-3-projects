import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, img_as_float, color, data
from skimage.metrics import structural_similarity as ssim
from skimage.restoration import denoise_tv_chambolle
from scipy.signal import fftconvolve
from numpy.fft import fft2, ifft2
import cv2
from numpy.linalg import norm
from scipy.ndimage import sobel
import warnings
warnings.filterwarnings("ignore")

# -----------------------------
# FSIM implementation (approximate)
# -----------------------------
def fsim(im1, im2):
    def gradient_magnitude(img):
        Ix = sobel(img, axis=0)
        Iy = sobel(img, axis=1)
        return np.sqrt(Ix**2 + Iy**2)
    gm1 = gradient_magnitude(im1)
    gm2 = gradient_magnitude(im2)
    T1 = 0.85
    sim = (2 * gm1 * gm2 + T1) / (gm1**2 + gm2**2 + T1)
    return np.mean(sim)

# -----------------------------
# Utilities & core functions
# -----------------------------
def load_image_safe(path=None, as_gray=True):
    if path is None:
        img = data.camera() if as_gray else data.astronaut()
        img = img_as_float(img)
        return img
    path = os.path.normpath(path)
    try:
        img = io.imread(path)
    except Exception:
        img_bgr = cv2.imread(path)
        if img_bgr is None:
            raise FileNotFoundError(f"Cannot load image: {path}")
        img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img = img_as_float(img)
    if as_gray and img.ndim == 3:
        img = color.rgb2gray(img)
    return img

def build_gaussian_kernel(ksize=25, sigma=3.0):
    g = cv2.getGaussianKernel(ksize, sigma)
    k = np.outer(g.ravel(), g.ravel())
    k /= k.sum()
    return k

def pad_to_shape(arr, shape):
    out = np.zeros(shape, dtype=arr.dtype)
    out[:arr.shape[0], :arr.shape[1]] = arr
    return out

def make_fft_operators(kernel, shape):
    H = fft2(kernel, shape)
    H_conj = np.conj(H)
    def A(x):
        return np.real(ifft2(fft2(x) * H))
    def At(x):
        return np.real(ifft2(fft2(x) * H_conj))
    return A, At, H, H_conj

def clip01(x):
    return np.clip(x, 0.0, 1.0)

def metrics(ref, recon):
    s = ssim(ref, recon, data_range=1.0)
    f = fsim(ref, recon)
    return s, f

# -----------------------------
# ISTA algorithm
# -----------------------------
def ista(A, At, b, lam=0.01, max_iter=200, L=1.0, tol=1e-6):
    x = np.zeros_like(b)
    hist = []
    for k in range(max_iter):
        grad = At(A(x) - b)
        x_new = np.sign(x - grad / L) * np.maximum(np.abs(x - grad / L) - lam / L, 0)
        hist.append(0.5 * norm(A(x_new) - b)**2)
        if norm(x_new - x) / (norm(x) + 1e-12) < tol:
            break
        x = x_new
    return clip01(x), np.array(hist)

# -----------------------------
# FISTA algorithm
# -----------------------------
def fista(A, At, b, lam=0.01, max_iter=200, L=1.0, tol=1e-6):
    x = np.zeros_like(b)
    y = x.copy()
    t = 1.0
    hist = []
    for k in range(max_iter):
        grad = At(A(y) - b)
        z = y - grad / L
        x_new = np.sign(z) * np.maximum(np.abs(z) - lam / L, 0)
        t_new = (1 + np.sqrt(1 + 4 * t**2)) / 2.0
        y = x_new + ((t - 1) / t_new) * (x_new - x)
        x = x_new
        t = t_new
        hist.append(0.5 * norm(A(x) - b)**2)
        if norm(x - y) / (norm(x) + 1e-12) < tol:
            break
    return clip01(x), np.array(hist)

# -----------------------------
# PnP-FISTA with TV denoiser
# -----------------------------
def pnp_fista(A, At, b, denoiser, L=1.0, max_iter=200, tol=1e-6):
    x = np.zeros_like(b)
    y = x.copy()
    t = 1.0
    hist = []
    for k in range(max_iter):
        grad = At(A(y) - b)
        z = y - (1.0 / L) * grad
        x_new = denoiser(z)
        t_new = (1 + np.sqrt(1 + 4 * t**2)) / 2.0
        y = x_new + ((t - 1) / t_new) * (x_new - x)
        x = x_new
        t = t_new
        hist.append(0.5 * norm(A(x) - b)**2)
        if k > 3 and norm(x - y) / (norm(x) + 1e-12) < tol:
            break
    return clip01(x), np.array(hist)

def denoiser_tv(z, weight=0.05):
    return denoise_tv_chambolle(z, weight=weight, channel_axis=None)

# -----------------------------
# Degrade Image
# -----------------------------
def degrade_image(img, kernel, noise_sigma=0.01):
    blurred = fftconvolve(img, kernel, mode='same')
    noisy = blurred + np.random.randn(*blurred.shape) * noise_sigma
    return clip01(noisy), blurred

# -----------------------------
# Evaluation
# -----------------------------
def evaluate_all(img, kernel, noise_sigma=0.01, max_iter=200):
    shape = img.shape
    kernel_pad = pad_to_shape(kernel, shape)
    A, At, H, H_conj = make_fft_operators(kernel_pad, shape)
    b_noisy, _ = degrade_image(img, kernel, noise_sigma)

    methods = {}
    histories = {}

    print("Running ISTA...")
    ista_res, hist_ista = ista(A, At, b_noisy, lam=0.01, max_iter=max_iter, L=1.0)
    methods['ISTA'] = ista_res
    histories['ISTA'] = hist_ista

    print("Running FISTA...")
    fista_res, hist_fista = fista(A, At, b_noisy, lam=0.01, max_iter=max_iter, L=1.0)
    methods['FISTA'] = fista_res
    histories['FISTA'] = hist_fista

    print("Running PnP-FISTA (TV denoiser)...")
    pnp_tv, hist_tv = pnp_fista(A, At, b_noisy, lambda z: denoiser_tv(z, weight=0.03), L=1.0, max_iter=max_iter)
    methods['PnP-FISTA'] = pnp_tv
    histories['PnP-FISTA'] = hist_tv

    # Compute metrics
    metrics_table = {}
    for name, rec in methods.items():
        rec_clip = clip01(rec)
        s, f = metrics(img, rec_clip)
        metrics_table[name] = {'SSIM': s, 'FSIM': f}

    return b_noisy, methods, metrics_table, histories

# -----------------------------
# Plotting
# -----------------------------
def plot_results(img, b_noisy, methods, metrics_table, histories=None, out_prefix=None):
    n = 2 + len(methods)
    cols = 3
    rows = int(np.ceil(n / cols))
    plt.figure(figsize=(4*cols, 3*rows))
    idx = 1
    plt.subplot(rows, cols, idx); idx += 1
    plt.title("Original"); plt.imshow(img, cmap='gray'); plt.axis('off')
    plt.subplot(rows, cols, idx); idx += 1
    plt.title("Blurred + Noisy"); plt.imshow(b_noisy, cmap='gray'); plt.axis('off')

    for name, rec in methods.items():
        plt.subplot(rows, cols, idx); idx += 1
        rec = clip01(rec)
        s, f = metrics_table[name]['SSIM'], metrics_table[name]['FSIM']
        plt.title(f"{name}\nSSIM {s:.3f}  FSIM {f:.3f}")
        plt.imshow(rec, cmap='gray')
        plt.axis('off')

    plt.tight_layout()
    plt.show()

# -----------------------------
# Main Function
# -----------------------------
def main(image_path=None):
    print("Loading image...")
    img = load_image_safe(image_path, as_gray=True)
    print("Image shape:", img.shape)

    kernel = build_gaussian_kernel(ksize=21, sigma=3.0)
    b_noisy, methods, metrics_table, histories = evaluate_all(img, kernel, noise_sigma=0.01, max_iter=120)

    print("\nResults (SSIM, FSIM):")
    for name, m in metrics_table.items():
        print(f"{name:10s}  SSIM: {m['SSIM']:.3f}  FSIM: {m['FSIM']:.3f}")

    plot_results(img, b_noisy, methods, metrics_table, histories=histories)

if __name__ == "__main__":
    main()
    