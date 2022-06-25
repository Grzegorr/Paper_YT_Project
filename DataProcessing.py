import json
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

#left and right hand are indexes 4 and 7

#data = [frame_0, frame_1, .....]
#frame_0 = [YOLO_data, openpose_data]
#YOLO_data = [boxes, classes, confidence]
#boxes = [box_0, box_1, ....]
#box = [x,y,w,h]
#openpose_data = [person1, person2, .....]

"""
Class no 0: person
Class no 1: bicycle
Class no 2: car
Class no 3: motorcycle
Class no 4: airplane
Class no 5: bus
Class no 6: train
Class no 7: truck
Class no 8: boat
Class no 9: traffic light
Class no 10: fire hydrant
Class no 11: stop sign
Class no 12: parking meter
Class no 13: bench
Class no 14: bird
Class no 15: cat
Class no 16: dog
Class no 17: horse
Class no 18: sheep
Class no 19: cow
Class no 20: elephant
Class no 21: bear
Class no 22: zebra
Class no 23: giraffe
Class no 24: backpack
Class no 25: umbrella
Class no 26: handbag
Class no 27: tie
Class no 28: suitcase
Class no 29: frisbee
Class no 30: skis
Class no 31: snowboard
Class no 32: sports ball
Class no 33: kite
Class no 34: baseball bat
Class no 35: baseball glove
Class no 36: skateboard
Class no 37: surfboard
Class no 38: tennis racket
Class no 39: bottle
Class no 40: wine glass
Class no 41: cup
Class no 42: fork
Class no 43: knife
Class no 44: spoon
Class no 45: bowl
Class no 46: banana
Class no 47: apple
Class no 48: sandwich
Class no 49: orange
Class no 50: broccoli
Class no 51: carrot
Class no 52: hot dog
Class no 53: pizza
Class no 54: donut
Class no 55: cake
Class no 56: chair
Class no 57: couch
Class no 58: potted plant
Class no 59: bed
Class no 60: dining table
Class no 61: toilet
Class no 62: tv
Class no 63: laptop
Class no 64: mouse
Class no 65: remote
Class no 66: keyboard
Class no 67: cell phone
Class no 68: microwave
Class no 69: oven
Class no 70: toaster
Class no 71: sink
Class no 72: refrigerator
Class no 73: book
Class no 74: clock
Class no 75: vase
Class no 76: scissors
Class no 77: teddy bear
Class no 78: hair drier
Class no 79: toothbrush
"""




#Deleting low confidence boxes
#TO BE DONE
#pop function can be used
def remove_low_confidence(all_data):
    for frame_no in range(len(all_data)):
        #print("Frame: " + str(frame_no))
        for r in range(len(all_data[frame_no][0][2])):
            #print(r)
            if all_data[frame_no][0][2][r] < 0.5:
                print(all_data[frame_no][0][2][r])



def add_a_path_to_a_Video(Video_name, color, path):
    video_path = "Data/Video_Adding_Path/Video_107.mp4"
    processed_video_name = "Data/Video_Adding_Path/Video_107_path.mp4"


def replace_padding_with_prevous_value_hands(JSON_path, output_JSON_path):
    f = open(JSON_path, 'r', encoding='utf-8')
    all_data = json.load(f)
    f.close()

    #For both hands
    for frame_no in range(len(all_data)):
        if frame_no > 0:
            #pad right hand with actual value
            if all_data[frame_no][1][0][4][0] == 0:
                print("I did something!")
                all_data[frame_no][1][0][4][0] = all_data[frame_no-1][1][0][4][0]
            if all_data[frame_no][1][0][4][1] == 0:
                print("I did something!")
                all_data[frame_no][1][0][4][1] = all_data[frame_no-1][1][0][4][1]
            # pad left hand with actual value
            if all_data[frame_no][1][0][7][0] == 0:
                print("I did something!")
                all_data[frame_no][1][0][7][0] = all_data[frame_no-1][1][0][7][0]
            if all_data[frame_no][1][0][7][1] == 0:
                print("I did something!")
                all_data[frame_no][1][0][7][1] = all_data[frame_no-1][1][0][7][1]

    output_file = open(output_JSON_path, 'w', encoding='utf-8')
    json.dump(all_data, output_file)
    output_file.close()




if __name__ == "__main__":
    JSON_path = "Data/JSON_FILES/Video_115.json"
    output_JSON_path = "Data/JSON_FILES/Video_115.json"

    replace_padding_with_prevous_value_hands(JSON_path, output_JSON_path)