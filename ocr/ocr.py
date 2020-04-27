import cv2
import pytesseract

def get_text(path_to_image):
    '''
    takes a single file as input (preprocessed earlier by the image 
    segmentation module) and returns the text present in it. Straightforward
    external interface
    '''
    image = cv2.imread(path_to_image)
    text = pytesseract.image_to_string(image).strip()

    return text
