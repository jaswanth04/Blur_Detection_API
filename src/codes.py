from enum import Enum

class BlurnessDetector(Enum):
    FFT = "FFT"
    Laplace = "Laplace"

class ResponseCode(Enum):
    Approved = "Not Blurred"
    Rejected_Blurred_Image = "Blurred"
    Format_Error = "File Type not supported"
    API_ERROR = "API Error"