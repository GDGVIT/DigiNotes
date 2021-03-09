from utils.api import *
import json

def AvgHeight(filename1):
    """
    A function used to calculate the average height of sentences for better ROI extraction.
    """

    test_file = ocr_space_file(filename = filename1, overlay = True, language = 'eng')
    test_file = json.loads(test_file)

    message = test_file['ParsedResults'][0]['TextOverlay']['Lines']

    heights = []
    for i in range(0, len(message)):
        heights.append(message[i]['MaxHeight'])

    return int(sum(heights)/ len(heights))
