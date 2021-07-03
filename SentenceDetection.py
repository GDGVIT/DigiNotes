import json
import sys

import cv2
import numpy as np
from utils.api import ocr_space_file
from utils.AvgHeight import AvgHeight
from utils.combine import combine


def underlined_sentences(img):
    if img is None:
        print("Error opening img: " + img)

    # Transform source img to gray if it is not already
    if len(img.shape) != 2:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    # A horizontal line kernel for line detection
    kernel = np.ones((1, 40), np.uint8)
    # Dilation followed by Erosion
    morphed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)

    line_removed = cv2.add(gray, (255 - morphed))  # Image without lines

    # Apply adaptiveThreshold at the bitwise_not of gray
    gray = cv2.bitwise_not(gray)
    # Binary Image
    bw = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2
    )

    # Create the image that will use to extract
    # the horizontal and vertical lines
    horizontal = np.copy(bw)

    # Specify size on horizontal axis
    cols = horizontal.shape[1]
    horizontal_size = cols / 20
    horizontal_size = int(horizontal_size)

    # Create structure element for extracting horizontal
    # lines through morphology operations
    horizontalStructure = cv2.getStructuringElement(
        cv2.MORPH_RECT, (horizontal_size, 1)
    )

    # Apply morphology operations
    horizontal = cv2.erode(horizontal, horizontalStructure)
    horizontal = cv2.dilate(horizontal, horizontalStructure)

    thresh = horizontal
    thresh2 = thresh.copy()

    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )  # Finding the Contours in the thresh image

    morphed = 255 - horizontal
    cv2.drawContours(morphed, contours, -1, (0, 0, 0), 3)  # draw all contours

    img = morphed  # We will be dealing the morphed picture going ahead.
    count = 0

    iss = []  # List of Column Numbers
    jss = []  # List of Row Numbers

    for i in contours:
        for j in i:
            for k in j:
                iss.append(k[0])
                jss.append(k[1])

    # Sorting the row and column numbers, to span across from top to bottom
    iss = sorted(iss)
    jss = sorted(jss)

    sections = []
    # A list containing row numbers of continuous lines of all sections

    each_section = []
    # A list containing row numbers of continuous lines of each section

    for i in range(0, len(jss) - 1):
        if abs(jss[i] - jss[i + 1]) < 20:
            each_section.append(jss[i])
            # If the difference of the row numbers of continuous lines is less
            # than 20 means they are a part of one section

        if abs(jss[i] - jss[i + 1]) > 20:
            sections.append(each_section)
            each_section = []

        if i == len(jss) - 2:
            sections.append(each_section)

    if len(sections) == 0:
        return []
    final_sections = []

    if len(final_sections) == 0:
        return []
    for i in sections:
        if len(i) > 35:
            final_sections.append(i)

    final_sections = combine(final_sections)

    final_messages = []
    for i in range(0, len(final_sections)):
        min_i = min(final_sections[i])  # Lower Row Number of a section
        max_i = max(final_sections[i])  # Upper Row Number of a section

        if min_i == 0 or max_i == 0:
            continue

        roi = line_removed[min_i - 40 : max_i, 0 : morphed.shape[1]]
        cv2.imwrite("cropped_img1.jpeg", roi)

        average_height = AvgHeight(filename1="cropped_img1.jpeg")
        # Used to calculate the average height of a sentences
        # for better ROI detection

        roi_true = line_removed[
            (min_i - average_height) : (max_i + average_height), 0 : morphed.shape[1]
        ]
        cv2.imwrite("cropped_img2.jpeg", roi_true)

        test_file = ocr_space_file(
            filename="cropped_img2.jpeg", overlay=True, language="eng"
        )

        test_file = json.loads(test_file)
        message = test_file["ParsedResults"][0]["ParsedText"]

        final_messages.append(message)

    print(final_messages)

    return {"Sentences": final_messages}
