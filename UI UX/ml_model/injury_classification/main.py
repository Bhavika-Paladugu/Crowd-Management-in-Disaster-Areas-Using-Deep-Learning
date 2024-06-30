import cv2
import numpy as np
import face_detection.face_detection as face_detection
from person_detection_image import process_frame

TEMP_TUNER = 1.80
TEMP_TOLERENCE = 70.6
count = 0
flag = None


def pixel_to_temperature(pixel):
    temp_min = 60
    temp_max = 90

    # temp_min = 80
    # temp_max = 110

    pixel_max = 255
    pixel_min = 0
    temp_range = temp_max - temp_min
    temp = (((pixel - pixel_min) * temp_range) / (pixel_max - pixel_min)) + temp_min + 14
    # print('$$$$$$$$$$$$$$$$$')
    return temp


def only_face(video_path):
    global count, flag, injury_label
    cap = cv2.VideoCapture(video_path)
    face_detector = face_detection.FaceDetector()

    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            output = frame
            faces = face_detector.detect_with_no_confidence(frame)
            if faces == []:
                face = False
                flag = 0
            else:
                face = True

            for (x1, y1, x2, y2) in faces:
                if len(faces) > 1:
                    count += 1
                roi = output[y1:y2, x1:x2]
                try:
                    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
                except Exception as e:
                    print(e)
                    continue
                try:
                    if face == True:
                        if flag == 0:
                            count += len(faces)
                            flag = 1
                except ValueError:
                    continue

                # Mask is boolean type of matrix.
                mask = np.zeros_like(roi_gray)

                # Mean of only those pixels which are in blocks and not the whole rectangle selected
                mean = pixel_to_temperature(np.mean(roi_gray))

                # Colors for rectangles and textmin_area
                temperature = round(mean, 2)

                injury_label = "Not Severely Injured"
                # print(temperature)
                # Injury classification based on temperature threshold (adjust 89.06 if needed)
                if temperature < 89.06:
                    injury_label = "Severly Injured"

                color = (0, 255, 0) if temperature < 100 else (0, 0, 255)

                # Draw rectangles for visualisation
                output = cv2.rectangle(output, (x1, y1), (x2, y2), color, 2)
                cv2.putText(output, "{} F".format(temperature), (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2,
                            cv2.LINE_AA)
                if temperature > 100:
                    while face is True:
                        face = frame[y1 + 2:y2 - 1, x1 + 2:x2 - 1]
                        print("image captured")
            cv2.imshow('Thermal', output)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    print(injury_label)
    if injury_label == "Not Severely Injured":
        statement = "No severely injured person detected."
    else:
        statement = "Severely injured person detected."
    print(statement)
    cap.release()
    cv2.destroyAllWindows()



def classify_file_type(file_path):
    video_extensions = ['.mp4']
    image_extensions = ['.jpeg', '.jpg', '.png']
    file_extension = file_path[file_path.rfind('.'):].lower()

    if file_extension in video_extensions:
        return 'video'
    elif file_extension in image_extensions:
        return 'image'
    else:
        return 'unknown'


if __name__ == "__main__":
    file_path = input('Enter the path:  ')
    file_type = classify_file_type(file_path)

    if file_type == 'video':
        video_path = file_path
        only_face(video_path)

    elif file_type == 'image':
        image_path = file_path
        image = cv2.imread(image_path)
        processed_image, injury_label = process_frame(image)
        print(injury_label)
        if injury_label == "Not Severely Injured":
            statement = "No severely injured person detected."
        else:
            statement = "Severely injured person detected."
        print(statement)
        cv2.imshow('Processed Image', processed_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print(f"{file_path} is neither a video nor an image file.")
