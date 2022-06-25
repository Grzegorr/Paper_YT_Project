import glob
import sys
import cv2
import os
import argparse
import numpy as np
from os.path import exists
import json

def get_empty_openPose_data():
    data = [[[0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0]
    ]]
    return data

def convert_rec(x):
    if isinstance(x, list):
        #print(x)
        return list(map(convert_rec, x))
    else:
        return float(x)

def import_open_pose():
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + './openpose/bin/python/openpose/Release');
        os.environ['PATH'] = os.environ['PATH'] + ';' + dir_path + '/../x64/Release;' + dir_path + './openpose/bin'
        import pyopenpose as op
        return op
    except ImportError as e:
        print(
            'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

def openpose(op, opWrapper, image_path,saving_path):
    # Process Image
    datum = op.Datum()
    imageToProcess = cv2.imread(image_path)

    #Print Image Info
    height, width, channels = imageToProcess.shape
    print("Image width: " + str(width) + ".")
    print("Image height: " + str(height) + ".")

    datum.cvInputData = imageToProcess
    opWrapper.emplaceAndPop(op.VectorDatum([datum]))

    # Display Image and Save Image
    #print("Body keypoints: \n" + str(datum.poseKeypoints))
    # cv2.imshow("OpenPose Only", datum.cvOutputData)
    cv2.imwrite("./TEMP_FILES_2/" + str(saving_path), datum.cvOutputData)
    openPosedImage = datum.cvOutputData
    # cv2.waitKey(0)

#################################################################################################
#    #Test code to test what the positions of the joints are
#   # Circle in joint 4 and 7
#    x = datum.poseKeypoints[0][4][0]
#    y = datum.poseKeypoints[0][4][1]
#    center_coordinates = (int(x), int(y))
#    radius = 20
#    color = (255, 0, 0)
#    # Line thickness of 2 px
#    thickness = 5
#
#    # Using cv2.circle() method
#    # Draw a circle with blue line borders of thickness of 2 px
#    image = cv2.circle(openPosedImage, center_coordinates, radius, color, thickness)
#
#    x = datum.poseKeypoints[0][7][0]
#    y = datum.poseKeypoints[0][7][1]
#    center_coordinates = (int(x), int(y))
#    radius = 20
#    color = (255, 0, 0)
#    # Line thickness of 2 px
#    thickness = 5
#
#    # Using cv2.circle() method
#    # Draw a circle with blue line borders of thickness of 2 px
#    image = cv2.circle(openPosedImage, center_coordinates, radius, color, thickness)
#    cv2.imwrite("./TEMP_FILES_2/" + str(saving_path), image)
###################################################################################################

    #Return
    return datum

def run_open_pose(image_path, op, saving_path):
    try:
        # Flags
        parser = argparse.ArgumentParser()
        # parser.add_argument("--image_path", default="../examples/media/COCO_val2014_000000000192.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
        parser.add_argument("--image_path", default=image_path,
                            help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
        args = parser.parse_known_args()

        # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        params = dict()
        params["model_folder"] = "./openpose/models/"

        # Add others in path?
        for i in range(0, len(args[1])):
            curr_item = args[1][i]
            if i != len(args[1]) - 1:
                next_item = args[1][i + 1]
            else:
                next_item = "1"
            if "--" in curr_item and "--" in next_item:
                key = curr_item.replace('-', '')
                if key not in params:  params[key] = "1"
            elif "--" in curr_item and "--" not in next_item:
                key = curr_item.replace('-', '')
                if key not in params: params[key] = next_item

        print("Args: " + str(args))
        print("Params: " + str(params))

        # Construct it from system arguments
        # op.init_argv(args[1])
        # oppython = op.OpenposePython()

        # Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()
        return opWrapper


        # Process Image
        #datum = op.Datum()
        #imageToProcess = cv2.imread(image_path)
        #datum.cvInputData = imageToProcess
        #opWrapper.emplaceAndPop(op.VectorDatum([datum]))

        # Display Image
        #print("Body keypoints: \n" + str(datum.poseKeypoints))
        #cv2.imshow("OpenPose Only", datum.cvOutputData)
        #cv2.imwrite("./TEMP_FILES/" + str(saving_path), datum.cvOutputData)
        openPosedImage = datum.cvOutputData
        #cv2.waitKey(0)
    except Exception as e:
        print(e)
        sys.exit(-1)

def YOLO_get_classes_and_colors():
    # read class names from text file
    classes = None
    with open("Data/Classes/All_Classes.txt", 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    print("Class list:\n")
    for r in range(len(classes)):
        print("Class no " + str(r) + ": " + str(classes[r]))

    # generate different colors for different classes
    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

    return classes, COLORS


# function to draw bounding box on the detected object with class name
def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h, classes, COLORS):

    label = str(classes[class_id])
    color = COLORS[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def read_pre_trained_YOLO():
    # read pre-trained model and config file
    net = cv2.dnn.readNet("Data/Weight_and_Config/YOLOv3_608/yolov3.weights", "Data/Weight_and_Config/YOLOv3_608/yolov3.cfg")
    return net

def run_YOLO(image_path, image_path_2, saving_path, classes, COLORS, net):
    # read input image
    image = cv2.imread(image_path)
    image_to_draw_on = cv2.imread(image_path_2)


    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    # read class names from text file
    #classes = None
    #with open("Data/Classes/All_Classes.txt", 'r') as f:
    #    classes = [line.strip() for line in f.readlines()]
    #
    # generate different colors for different classes
    #COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

    # read pre-trained model and config file
    #net = cv2.dnn.readNet("Data/Weight_and_Config/YOLOv3_608/yolov3.weights", "Data/Weight_and_Config/YOLOv3_608/yolov3.cfg")

    # create input blob
    blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)

    # set input blob for the network
    net.setInput(blob)

    # run inference through the network
    # and gather predictions from output layers
    # outs = net.forward(get_output_layers(net))

    outs = net.forward(net.getUnconnectedOutLayersNames())

    # initialization
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    # for each detetion from each output layer
    # get the confidence, class id, bounding box params
    # and ignore weak detections (confidence < 0.5)
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    # apply non-max suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    #print("Indices: " + str(indices))

    # go through the detections remaining
    # after nms and draw bounding box
    for i in indices:
        # i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]

        draw_bounding_box(image_to_draw_on, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h), classes = classes, COLORS = COLORS)

    # display output image
    #cv2.imshow("YOLO", image)
    # wait until any key is pressed
    #cv2.waitKey()
    # save output image to disk
    cv2.imwrite("./TEMP_FILES_3/" + str(saving_path), image_to_draw_on)
    # release resources
    cv2.destroyAllWindows()
    return boxes, class_ids, confidences


def load_packages_classes_etc():
    op = import_open_pose()
    classes, COLORS = YOLO_get_classes_and_colors()
    return op, classes, COLORS

#Saving in temporary files
def process_a_frame(op, classes, COLORS, image_path, save_path):
    run_open_pose(image_path=image_path, op=op, saving_path="test.jpg")
    run_YOLO(image_path="./TEMP_FILES/test.jpg", saving_path="test.jpg", classes=classes, COLORS=COLORS)

def process_a_frame_Video(op, classes, COLORS, image_path, image_path_2,save_path, net,opWrapper, if_print = False):
    #run_open_pose(image_path=image_path, op=op, saving_path=save_path)
    datum = openpose(op, opWrapper, image_path,save_path)
    detection_boxes, class_ids, confidences = run_YOLO(image_path=image_path,image_path_2 = image_path_2, saving_path=save_path, classes=classes, COLORS=COLORS, net = net)
    if if_print:
        print("Body keypoints: \n" + str(datum.poseKeypoints))
        #print("Body keypoints: \n" + str(datum.pose_keypoints_2d))
        print("Class IDs: \n" + str(class_ids))
        print("Object Boxes: \n" + str(detection_boxes))

    YOLO_data = [detection_boxes,class_ids, confidences]
    if datum.poseKeypoints is None:
        print("The empty array was found!")
        openpose_data = get_empty_openPose_data()
    else:
        openpose_data = np.ndarray.tolist(datum.poseKeypoints)

    YOLO_data = convert_rec(YOLO_data)
    openpose_data = convert_rec(openpose_data)

    single_frame_data = [YOLO_data, openpose_data]
    #print(single_frame_data)
    return single_frame_data

    #return [YOLO_data]

def clean_temp_files():
    files = glob.glob("./TEMP_FILES/*")
    for f in files:
        os.remove(f)

    files = glob.glob("./TEMP_FILES_2/*")
    for f in files:
        os.remove(f)

    files = glob.glob("./TEMP_FILES_3/*")
    for f in files:
        os.remove(f)

def video_into_temporary_frames(video_path):
    print("Video path: " + str(video_path))
    capture = cv2.VideoCapture(video_path)
    frameNr = 0
    while (True):
        success, frame = capture.read()
        if success:
            cv2.imwrite(f'./TEMP_FILES/frame_{frameNr}.jpg', frame)
        else:
            break
        frameNr = frameNr + 1
        #print(frameNr)
    capture.release()

def stitch_frames_into_video(processed_video_name):
    image_folder = 'TEMP_FILES_3'
    video_name = processed_video_name

    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    images_sorted = []
    for r in range(len(images)):
        images_sorted.append("frame_" + str(r) + ".jpg")
        #print("Sorting Frames: " +str(r))
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_name, fourcc, 30, (width, height))

    for image in images_sorted:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

import_open_pose()


if __name__ == "__main__":

    video_path = "Data/Example_Video/Video_115.mp4"
    processed_video_name = "Video_115.mp4"
    dest_file = "Data/JSON_FILES/Video_115.json"

    #########################################################################
    ############# Code to run a video through the algorithm #################
    #########################################################################
    if True:
        print("I am running a whole video! TEMP WILL BE CLEANED!")

        #video_path = "Data/Example_Video/Video_113.mp4"
        #processed_video_name = "Video_113.mp4"
        #dest_file = "Data/JSON_FILES/Video_113.json"
        #print(os.listdir("TEMP_FILES_3"))

        clean_temp_files()
        video_into_temporary_frames(video_path = video_path)
        net = read_pre_trained_YOLO()
        op, classes, COLORS = load_packages_classes_etc()
        opWrapper = run_open_pose(image_path="image_path", op=op, saving_path="save_path")

        files = glob.glob("./TEMP_FILES/*")
        for i in range(len(files)):
            print("\nProcessing a frame no: " + str(i) + "\n")
            image_path = "./TEMP_FILES/frame_" + str(i) + ".jpg"
            image_path_2 = "./TEMP_FILES_2/frame_" + str(i) + ".jpg"
            save_path = "frame_" + str(i) + ".jpg"
            single_frame_data = process_a_frame_Video(op, classes, COLORS, image_path, image_path_2, save_path = save_path, net= net, opWrapper=opWrapper, if_print=False)
            #print(single_frame_data)
            #### SAVING DATA ####
            if not exists(dest_file):
                output_file = open(dest_file, 'w', encoding='utf-8')
                json.dump([single_frame_data], output_file)
                #json.dump([0,0,0,0,0], output_file)
                output_file.close()
            else:
                f = open(dest_file, 'r', encoding='utf-8')
                all_data = json.load(f)
                f.close()
                all_data.append(single_frame_data)
                output_file = open(dest_file, 'w', encoding='utf-8')
                json.dump(all_data, output_file)
                #output_file.write("\n")
                output_file.close()



        stitch_frames_into_video(processed_video_name)

    if False:
        print("Experimenting on a single frame.")

        net = read_pre_trained_YOLO()
        op, classes, COLORS = load_packages_classes_etc()
        opWrapper = run_open_pose(image_path="image_path", op=op, saving_path="save_path")

        ## Frame Number
        i = 9999
        print("\nProcessing a frame no: " + str(i) + "\n")
        image_path = "./TEMP_FILES/frame_" + str(i) + ".jpg"
        image_path_2 = "./TEMP_FILES_2/frame_" + str(i) + ".jpg"
        save_path = "frame_" + str(i) + ".jpg"
        process_a_frame_Video(op, classes, COLORS, image_path, image_path_2, save_path = save_path, net= net, opWrapper=opWrapper, if_print = True)

    if False:
        stitch_frames_into_video(processed_video_name)










