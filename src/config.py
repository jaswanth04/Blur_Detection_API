from pydantic_settings import BaseSettings
from typing import Any
from codes import BlurnessDetector

import os

def parse_list(x: str) -> list[str]:
    return x.split(',')

class Settings(BaseSettings):
    blur_acceptance_threshold: int #= 20
    fft_mean_shift: int #= 60
    pdf_image_dpi: int #= 500
    pdf_extension: str #= "pdf"
    laplace_blur_threshold: int
    detection_type: BlurnessDetector
    image_extensions_allowed_list: list[str] #= Field(env_parse=parse_list) #= ['jpg', 'jpeg', 'JPG', 'JPEG', 'png', 'PNG']

    class Config:
        @classmethod
        # env_file = ".env"
        def parse_list(cls, field_name: str, raw_val: str) -> Any:
            if field_name == 'image_extensions_allowed_list':
                return [ex for ex in raw_val.split(',')]
            
        @classmethod
        def parse_detection_method(cls, field_name: str, raw_val: str) -> Any:
            if field_name == "detection_type":
                return BlurnessDetector.FFT if raw_val.lower() == "fft" else BlurnessDetector.Laplace


if __name__ == "__main__":

    os.environ['env'] = "production"
    os.environ['image_extensions_allowed_list'] = '["jpg","jpeg","JPG","JPEG","png","PNG"]'
    settings = Settings(_env_file=".env")
    print(settings.dict())