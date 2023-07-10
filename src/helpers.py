import numpy as np
import pdf2image
import cv2

def convert_pdf_to_image(document, pdf_image_dpi):
    images = []

    pages = pdf2image.convert_from_bytes(document, pdf_image_dpi)

    first_page_image = cv2.cvtColor(np.asarray(pages[0]), code=cv2.COLOR_RGB2BGR)

    return first_page_image


def main():

    pdf_location = "test.pdf"

    img = convert_pdf_to_image(pdf_location)

    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
# if __name__ == "__main__":
#     main()