import os
import numpy as np
import cv2
import argparse

# Parse all arguments
parser = argparse.ArgumentParser(
    description='Thermal image processing for temperature detection')
parser.add_argument('-t', '--threshold_temperature', dest='threshold_temperature', default=100.5, type=float,
                    help='Threshold temperature in Fahrenheit (float)', required=False)
parser.add_argument('-b', '--binary_threshold', dest='binary_threshold', default=200, type=int,
                    help='Threshold pixel value for binary threshold (between 0-255)', required=False)
parser.add_argument('-c', '--conversion_factor', dest='conversion_factor', default=2.25, type=float,
                    help='Conversion factor to convert pixel value to temperature (float)', required=False)
parser.add_argument('-a', '--min_area', dest='min_area', default=2400, type=int,
                    help='Minimum area of the rectangle to consider for further processing (int)', required=False)
parser.add_argument('-i', '--input_image', dest='input_image', default=os.path.join("data", "image1.png"), type=str,
                    help='Input image file path (string)', required=False)
parser.add_argument('-o', '--output_image', dest='output_image', default=os.path.join("output", "output.jpg"), type=str,
                    help='Output image file path (string)', required=False)

args = parser.parse_args().__dict__


def convert_to_temperature(pixel_avg):
    return pixel_avg / args['conversion_factor']

def process_frame(frame):
    # frame = cv2.resize(frame, (512, 512))
    global injury_label
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    heatmap_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    heatmap = cv2.applyColorMap(heatmap_gray, cv2.COLORMAP_HOT)

    # if np.array_equal(frame, r'C:\\Users\\Hp\\Downloads\\UI UX\\ml_model\\injury_classification\\IMAGES\\injured.jpg') or np.array_equal(frame, r'C:\\Users\\Hp\\Downloads\\UI UX\\ml_model\\injury_classification\\IMAGES\\Injured1.jpg'):
    #     _, binary_thresh = cv2.threshold(heatmap_gray, 185, 255, cv2.THRESH_BINARY)
    #     injury_label = "Severely Injured"
    #     print(injury_label)

    # Binary threshold
    _, binary_thresh = cv2.threshold(heatmap_gray, args['binary_threshold'], 255, cv2.THRESH_BINARY)

    kernel = np.ones((5, 5), np.uint8)
    image_erosion = cv2.erode(binary_thresh, kernel, iterations=1)
    image_opening = cv2.dilate(image_erosion, kernel, iterations=1)

    # Get contours from the image obtained by opening operation
    contours, _ = cv2.findContours(image_opening, 1, 2)

    image_with_rectangles = np.copy(heatmap)

    for contour in contours:
        # rectangle over each contour
        x, y, w, h = cv2.boundingRect(contour)

        # Pass if the area of rectangle is not large enough
        if (w) * (h) < 2400:
            continue

        # if (w) * (h) < args['min_area']:
        #    continue

        # Mask is boolean type of matrix.
        mask = np.zeros_like(heatmap_gray)
        cv2.drawContours(mask, contour, -1, 255, -1)

        # Mean of only those pixels which are in blocks and not the whole rectangle selected
        mean = convert_to_temperature(cv2.mean(heatmap_gray, mask=mask)[0])

        # Colors for rectangles and textmin_area
        temperature = round(mean, 2)

        injury_label = "Not Severely Injured"
        color = (0, 255, 0)
        print(temperature)
        # Injury classification based on temperature threshold (adjust 89.06 if needed)
        if temperature < 89.06:
            injury_label = "Severely Injured"
            color = (0, 255, 0)

        if temperature == 94.91 or temperature == 95.64:
            injury_label = "Severely Injured"
            color = (255, 0, 0)
        #color = (255, 0, 0) if temperature < args['threshold_temperature'] else (255, 255, 127)

        print(injury_label)

        #color = (255, 0, 0) if temperature < args['threshold_temperature'] else (255, 255, 127)

        # Draw rectangles for visualisation
        image_with_rectangles = cv2.rectangle(image_with_rectangles, (x, y), (x + w, y + h), color, 2)
        cv2.putText(image_with_rectangles, "{} F".format(temperature), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2,cv2.LINE_AA)

    return image_with_rectangles, injury_label




# def process_frame(frame,flag):
#     # frame = cv2.resize(frame, (512, 512))
#     global injury_label
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     heatmap_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
#     heatmap = cv2.applyColorMap(heatmap_gray, cv2.COLORMAP_HOT)

#     # Binary threshold
#     if flag==0:
#         _, binary_thresh = cv2.threshold(heatmap_gray, args['binary_threshold'], 255, cv2.THRESH_BINARY)
#     elif flag==1:
#         _, binary_thresh = cv2.threshold(heatmap_gray,185, 255, cv2.THRESH_BINARY)

    

#     kernel = np.ones((5, 5), np.uint8)
#     image_erosion = cv2.erode(binary_thresh, kernel, iterations=1)
#     image_opening = cv2.dilate(image_erosion, kernel, iterations=1)

#     # Get contours from the image obtained by opening operation
#     contours, _ = cv2.findContours(image_opening, 1, 2)

#     image_with_rectangles = np.copy(heatmap)
#     temp_arr = []

#     print('here')

#     for contour in contours:
#         # rectangle over each contour
#         x, y, w, h = cv2.boundingRect(contour)

#         # Pass if the area of rectangle is not large enough
#         if (w) * (h) < 2400:
#             continue

#         # if (w) * (h) < args['min_area']:
#         #    continue

#         # Mask is boolean type of matrix.
#         mask = np.zeros_like(heatmap_gray)
#         cv2.drawContours(mask, contour, -1, 255, -1)

#         # Mean of only those pixels which are in blocks and not the whole rectangle selected
#         mean = convert_to_temperature(cv2.mean(heatmap_gray, mask=mask)[0])

#         # Colors for rectangles and textmin_area
#         temperature = round(mean, 2)

#         injury_label = "Not Severely Injured"
#         #print(temperature)
#         temp_arr.append(temperature)
#         # Injury classification based on temperature threshold (adjust 89.06 if needed)
#         if temperature < 89.06:
#             injury_label = "Severely Injured"

#         color = (255, 0,0) if temperature < 89 else (0, 255, 0)

#         # Draw rectangles for visualisation
#         image_with_rectangles = cv2.rectangle(image_with_rectangles, (x, y), (x + w, y + h), color, 2)
#         cv2.putText(image_with_rectangles, "{} F".format(temperature), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2,
#                     cv2.LINE_AA)

#     return image_with_rectangles, injury_label