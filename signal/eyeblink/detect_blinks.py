# USAGE
# python detect_blinks.py --shape-predictor shape_predictor_68_face_landmarks.dat --video blink_detection_demo.mp4
# python detect_blinks.py --shape-predictor shape_predictor_68_face_landmarks.dat
# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import argparse
import imutils
import time
import dlib
import cv2


# compute the Eye Aspect Ratio (ear),
# which is a relation of the average vertical distance between eye landmarks to the horizontal distance
def eye_aspect_ratio(eye):
    vertical_dist = dist.euclidean(eye[1], eye[5]) + dist.euclidean(eye[2], eye[4])
    horizontal_dist = dist.euclidean(eye[0], eye[3])
    return vertical_dist / (2.0 * horizontal_dist)


BLINK_THRESHOLD = 0.23  # the threshold of the ear below which we assume that the eye is closed
CONSEC_FRAMES_NUMBER = 1  # minimal number of consecutive frames with a low enough ear value for a blink to be detected

# get arguments from a command line
ap = argparse.ArgumentParser(description='Eye blink detection')
ap.add_argument("-p", "--shape-predictor", required=True, help="path to facial landmark predictor")
ap.add_argument("-v", "--video", type=str, default="", help="path to input video file")
args = vars(ap.parse_args())

# initialize dlib's face detector (HOG-based) and facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# choose indexes for the left and right eye
(left_s, left_e) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(right_s, right_e) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# start the video stream or video reading from the file
video_path = args["video"]
if video_path == "":
    vs = VideoStream(src=0).start()
    print("[INFO] starting video stream from built-in webcam...")
    fileStream = False
else:
    vs = FileVideoStream(video_path).start()
    print("[INFO] starting video stream from a file...")
    fileStream = True
time.sleep(1.0)

counter = 0
total = 0
alert = False
start_time = 0
last_blink = 0
double_blink = 0
frame = vs.read()

# loop over the frames of video stream:
# grab the frame, resize it, convert it to grayscale
# and detect faces in the grayscale frame
while (not fileStream) or (frame is not None):
    frame = imutils.resize(frame, width=640)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray_frame, 0)
    ear = 0
    # loop over the face detections:
    # determine the facial landmarks,
    # convert the facial landmark (x, y)-coordinates to a numpy array,
    # then extract the left and right eye coordinates,
    # and use them to compute the average eye aspect ratio for both eyes
    for rect in rects:
        shape = predictor(gray_frame, rect)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[left_s:left_e]
        rightEye = shape[right_s:right_e]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        # visualize each of the eyes
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        # if the eye aspect ratio is below the threshold, increment counter
        # if the eyes are closed longer than for 2 secs, raise an alert
        if ear < BLINK_THRESHOLD:
            counter += 1
            if start_time == 0:
                start_time = time.time()
                last_blink = time.time()
            else:
                end_time = time.time()
                if end_time - start_time > 4:
                    alert = True
        else:
            if counter >= CONSEC_FRAMES_NUMBER:
                total += 1
                # if last blink happened within 0.6s ago, it's a double blink
                if time.time()-last_blink <= 0.6:
                    last_blink = time.time()
                    double_blink += 1
                else:
                    last_blink = time.time()
            counter = 0
            start_time = 0
            alert = False

    # draw the total number of blinks and EAR value
    cv2.putText(frame, "Blinks: {}".format(total), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, "EAR: {:.2f}".format(ear), (500, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, "Double Blinks: {}".format(double_blink), (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    # this part is redundant
    """
    if alert:
        cv2.putText(frame, "ALERT!", (150, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    """
    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed or closing eye for 4s, break from the loop
    if key == ord("q") or alert:
        break
    frame = vs.read()

cv2.destroyAllWindows()
vs.stop()
