# 🖼️ Image Restoration using ISTA, FISTA & PnP-FISTA

## 📌 Project Overview
This project implements advanced **image restoration techniques** using optimization algorithms to recover a clean image from a degraded one.

The system takes a **blurred and noisy image** and restores it using:

-  ISTA (Iterative Shrinkage Thresholding Algorithm)
-  FISTA (Fast ISTA)
-  PnP-FISTA (Plug-and-Play with TV Denoiser)

It then compares the performance of these algorithms using image quality metrics.

---

## 🎯 What This Project Does

In real-world scenarios, images often get degraded due to:
- Blur (camera motion, focus issues)
- Noise (low light, sensor errors)

👉 This project:
- Simulates image degradation (blur + noise)
- Applies different algorithms to restore the image
- Compares which method gives the best result

📌 In simple terms:
> This project cleans and improves low-quality images using mathematical optimization techniques.

---

## 🚀 Features

- 🧠 Multiple optimization algorithms (ISTA, FISTA, PnP-FISTA)
- 🔍 Image degradation simulation
- 📊 Quality evaluation using SSIM & FSIM
- 📈 Algorithm performance comparison
- 🖥️ Visualization of results

---

## ⚙️ Methodology

The project follows a structured pipeline for image restoration:

### 🔹 Step 1: Image Acquisition
- Load a grayscale image from dataset or local file
- Normalize pixel values for processing

---

### 🔹 Step 2: Image Degradation
- Apply **Gaussian blur** using convolution
- Add **random noise** to simulate real-world distortion
- Output: Blurred + noisy image

---

### 🔹 Step 3: Mathematical Modeling
- Represent degradation as:

  Image = Blur Operator + Noise

- Use **FFT-based convolution** for efficient computation

---

### 🔹 Step 4: Image Restoration Algorithms

####  ISTA
- Iterative optimization method
- Applies soft-thresholding to recover image

####  FISTA
- Improved version of ISTA
- Uses momentum for faster convergence

####  PnP-FISTA
- Combines optimization with denoising
- Uses **Total Variation (TV) denoiser**
- Produces higher quality results

---

### 🔹 Step 5: Evaluation

Each restored image is evaluated using:

- **SSIM (Structural Similarity Index)** → measures structural similarity  
- **FSIM (Feature Similarity Index)** → measures feature similarity  

---

### 🔹 Step 6: Visualization

- Display:
  - Original Image
  - Degraded Image
  - Restored Images (for all algorithms)
- Compare performance visually and numerically

---

## 🧠 Algorithms Used

- ISTA
- FISTA
- Plug-and-Play FISTA (TV Denoiser)
- FFT-based convolution
- Gradient-based optimization

---

## 📊 Evaluation Metrics

- **SSIM (Structural Similarity Index)**
- **FSIM (Feature Similarity Index)**



---

## 📊 Output

- Displays:
  - Original image
  - Blurred + noisy image
  - Restored images using different algorithms


---

## ⏱️ Time Complexity

- Iterative algorithms: **O(n²)**
- FFT improves computational efficiency

---

## ✅ Advantages

- Efficient image restoration
- Faster convergence using FISTA
- High-quality output using PnP methods
- Works on real-world degraded images



---

## 📌 Conclusion

This project demonstrates how **optimization algorithms** can be used for image restoration.

It compares different techniques and shows how advanced methods like **PnP-FISTA** can produce better results.

---

## 🔮 Future Scope

- Use deep learning models (CNN, GAN)
- Real-time image processing
- Color image restoration
- Integration with UI applications

---

