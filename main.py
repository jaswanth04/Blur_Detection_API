
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, status


import numpy as np
import cv2

from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from blur_detection import detect_blur_fft, detect_blur_lap

from logger import logger
from helpers import convert_pdf_to_image
from codes import ResponseCode, BlurnessDetector
from config import Settings


class RequestData(BaseModel):
    file: UploadFile = File(...)
    return_score: bool = False
    

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:5501",
    "http://127.0.0.1:8000"
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


settings = Settings(_env_file='.env')
logger.info("Parsing the settings is completed !!")

@app.get("/info")
def info():
    return settings.model_dump()

@app.get("/ping")
def ping():
    return {"ping": "Successful - Turnstile API"}


@app.post("/check_blur", status_code=status.HTTP_200_OK)
async def check_blur(file: UploadFile = File(...), return_score: bool = True):

    logger.info(f'File sent through Http Request: {file.filename}, return_score value: {return_score}')

    if file.filename != "":
        extension = file.filename.split(".")[-1]

        if extension == settings.pdf_extension:
            img = convert_pdf_to_image(await file.read(), settings.pdf_image_dpi)
        elif extension in settings.image_extensions_allowed_list:
            img = np.frombuffer(await file.read(), np.uint8)
            img = cv2.imdecode(img, -1)
        else:
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=ResponseCode.Format_Error.value)
    else:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=ResponseCode.Format_Error.value)

        
    img = cv2.resize(img, (500, 500))
    
    try:
        if settings.detection_type == BlurnessDetector.Laplace:
            mean, blurry = detect_blur_lap(img, settings.laplace_blur_threshold)
        elif settings.detection_type == BlurnessDetector.FFT:
            mean, blurry = detect_blur_fft(image=img, size=settings.fft_mean_shift, thresh=settings.blur_acceptance_threshold)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseCode.API_ERROR.value)

        logger.info(f'Blurness result: {blurry}, Score: {mean}')

        score = mean if return_score else 0

        logger.info(f'Return score is: {return_score}, so value of score is set to: {score}')

        if blurry:
            result = ResponseCode.Rejected_Blurred_Image
        else:
            result = ResponseCode.Approved
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ResponseCode.API_ERROR.value)

    return {"result": result, "score": score}
    
    
    