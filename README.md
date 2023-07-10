# Blur Detection API

A REST API for detecting blurness in the image

## Introduction

Detecting blurness in the image is a very important task. There are multiple methods of blurness detection. 

1. Lapalacian Method - Here we convolve the image with a laplacian kernel, and finally get one blur map. Obtain the variance of the blur map, and if it is less than a chosen threshold, we mark it as blur
2. FFT Method - We take a Fourier Transformation of the image, shift the image by a pre determined size, perform inverse tranformation, and take the absolute mean of the image. The final value obtained is the score, which is compared against a threshold to determine the final result

## Starting the API 

### Using python

Use the following commands

```
pip install -r requirements.txt
export PYTHONPATH = echo `pwd`/src:$PYTHONPATH
uvicorn main:app
```

The api will be pointing to http://127.0.0.1:8000

### Using Docker

Build command

```
docker build -t blur .
```

Run command

```
docker run -p 9030:9030 blur
```

The api will be poiting to http://localhost:9030/

## Usage and Endpoints

We have the following endpoints:

GET /info - Provides the settings
GET /ping - Provides the health
POST /check_blur - Parameters - file (Type is file) - Select the image file to be given as input; return_score: Boolean value to say whether score needs to be returned or not

## Configuration

The configuration is present in .env file. Please modify it to use the desired config

1. BLUR_ACCEPTANCE_THRESHOLD = Threshold in case of FFT. Below this threshold, the image is blurred.
2. LAPLACE_BLUR_THRESHOLD Threshold in case of Laplace. Below this threshold, the image is blurred. 
3. FFT_MEAN_SHIFT = The value with which image is shifted post fft transformation
4. PDF_IMAGE_DPI = DPI to be used for pdf to image conversion
5. PDF_EXTENSION = The extension of a pdf file. Default is "pdf"
6. DETECTION_TYPE = Type of detection. Use "FFT" for Fast Fourier Transform. Use "Laplace" for Laplacian transform
7. IMAGE_EXTENSIONS_ALLOWED_LIST= The list of the extensions allowed. Default is '["jpg","jpeg","JPG","JPEG","png","PNG"]'


