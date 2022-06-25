import sys
import cv2
import os
import argparse
import numpy as np

def import_open_pose():
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '/openpose/bin/python/openpose/Release');
        os.environ['PATH'] = os.environ['PATH'] + ';' + dir_path + '/../x64/Release;' + dir_path + './openpose/bin'
        import pyopenpose as op
        return op
    except ImportError as e:
        print(
            'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e



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


        # Process Image
        datum = op.Datum()
        imageToProcess = cv2.imread(args[0].image_path)
        datum.cvInputData = imageToProcess
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))

        # Display Image
        print("Body keypoints: \n" + str(datum.poseKeypoints))
        #cv2.imshow("OpenPose Only", datum.cvOutputData)
        cv2.imwrite("./TEMP_FILES/" + str(saving_path), datum.cvOutputData)
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

def run_YOLO(image_path, saving_path, classes, COLORS, net):
    # read input image
    image = cv2.imread(image_path)


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
    print("Indices: " + str(indices))

    # go through the detections remaining
    # after nms and draw bounding box
    for i in indices:
        # i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]

        draw_bounding_box(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h), classes = classes, COLORS = COLORS)

    # display output image
    #cv2.imshow("YOLO", image)
    # wait until any key is pressed
    #cv2.waitKey()
    # save output image to disk
    cv2.imwrite("./TEMP_FILES/" + str(saving_path), image)
    # release resources
    cv2.destroyAllWindows()


def load_packages_classes_etc():
    op = import_open_pose()
    classes, COLORS = YOLO_get_classes_and_colors()
    return op, classes, COLORS

#Saving in temporary files
def process_a_frame(op, classes, COLORS, image_path, save_path):
    run_open_pose(image_path=image_path, op=op, saving_path="test.jpg")
    run_YOLO(image_path="./TEMP_FILES/test.jpg", saving_path="test.jpg", classes=classes, COLORS=COLORS)

def process_a_frame_Video(op, classes, COLORS, image_path, save_path, net):
    run_open_pose(image_path=image_path, op=op, saving_path=save_path)
    run_YOLO(image_path=image_path, saving_path=save_path, classes=classes, COLORS=COLORS, net = net)


if __name__ == "__main__":
    image_path = "Data/Example/OHMC_kitchen1.jpg"
    #image_path = "Data/Example/broccoli_man2.jpg"

    op, classes, COLORS = load_packages_classes_etc()
    process_a_frame(op, classes, COLORS, image_path)