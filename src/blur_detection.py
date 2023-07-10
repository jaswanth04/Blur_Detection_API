
import cv2
import numpy as np
from logger import logger

def detect_blur_lap(image, threshold = 100):
    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur_map = cv2.Laplacian(image, cv2.CV_64F)
    score = np.var(blur_map)
    return score, bool(score < threshold)

def detect_blur_fft(image, size=60, thresh=10):
    logger.info(f'In FFT blur detection, Image shape: {image.shape}')
    h, w, _ = image.shape
    cX, cY = int(w/2), int(h/2)

    fft = np.fft.fft2(image)
    fftShift = np.fft.fftshift(fft)

    fftShift[cY - size: cY + size, cX - size:cX + size] = 0
    fftShift = np.fft.ifftshift(fftShift)

    recon = np.fft.ifft2(fftShift)

    magnitude = 20 * np.log(np.abs(recon))
    mean = np.mean(magnitude)

    return mean, mean <= thresh

def main():
    img_path = "test_image.JPEG"

    img = cv2.imread(img_path)
    img = cv2.resize(img, (500, 500))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    mean, blurry = detect_blur_fft(gray, 60, 20, False)

    print(mean, blurry)


if __name__ == '__main__':
    main()
