import json
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


#position is 0 , 0 if cup not found
def get_cup_position_list(all_data):
    x = []
    y = []

    for frame_no in range(len(all_data)):
        #get middle of the cup box
        boxes = all_data[frame_no][0][0]
        classes = all_data[frame_no][0][1]

        #flags
        flag_cup_found = 0

        #find index where a cup is
        for r in range(len(classes)):
            if classes[r] == 41:
                #print("Classes: " + str(classes))
                #print("Boxes: " + str(boxes))
                cup_box_index = r
                #print("Got it at position: " + str(r))
                #print("Box: " + str(boxes[cup_box_index]))
                flag_cup_found = 1

        #gET box but only if found
        if flag_cup_found != 0:
            #get the box itself
            #print("Box: " + str(boxes[cup_box_index]))
            box = boxes[cup_box_index]
            middle_box_x = box[0] + box[2]
            middle_box_y = box[1] + box[3]


        #Checks
        if flag_cup_found == 0:
            print("Cup not found!")
            x.append(0)
            y.append(0)
        else:
            x.append(middle_box_x)
            y.append(middle_box_y)

    return [x, y]

def get_item_of_class_position(all_data, class_no):
    x = []
    y = []

    for frame_no in range(len(all_data)):
        #get middle of the cup box
        boxes = all_data[frame_no][0][0]
        classes = all_data[frame_no][0][1]

        #flags
        flag_cup_found = 0

        #find index where a cup is
        for r in range(len(classes)):
            if classes[r] == class_no:
                #print("Classes: " + str(classes))
                #print("Boxes: " + str(boxes))
                cup_box_index = r
                #print("Got it at position: " + str(r))
                #print("Box: " + str(boxes[cup_box_index]))
                flag_cup_found = 1

        #gET box but only if found
        if flag_cup_found != 0:
            #get the box itself
            #print("Box: " + str(boxes[cup_box_index]))
            box = boxes[cup_box_index]
            middle_box_x = box[0] + box[2]
            middle_box_y = box[1] + box[3]


        #Checks
        if flag_cup_found == 0:
            print("Item of class number " +str(class_no) + " not found.")
            if frame_no == 0:
                x.append(0)
                y.append(0)
            else:
                x.append(x[-1])
                y.append(y[-1])
        else:
            x.append(middle_box_x)
            y.append(middle_box_y)

    return [x, y]


def get_right_hand_position(all_data):
    x = []
    y = []
    for frame_no in range(len(all_data)):
        first_person_data = all_data[frame_no][1][0]
        #print(first_person_data)
        right_hand = first_person_data[4]
        #print(right_hand)
        x.append(right_hand[0])
        y.append(right_hand[1])

    return [x,y]

def get_left_hand_position(all_data):
    x = []
    y = []
    for frame_no in range(len(all_data)):
        first_person_data = all_data[frame_no][1][0]
        #print(first_person_data)
        left_hand = first_person_data[7]
        #print(right_hand)
        x.append(left_hand[0])
        y.append(left_hand[1])

    return [x,y]

def draw_a_correlation_matrix(paths, labels, title):
    n = len(paths)
    multi_corr = np.corrcoef(paths, paths)
    reduced_corr_matrix = multi_corr[0:n,0:n]
    print(reduced_corr_matrix)
    plt.figure(figsize=(12, 8))
    plt.title(title)
    sns.heatmap(reduced_corr_matrix, annot = True, xticklabels = labels, yticklabels = labels)
    plt.tick_params(axis='both', which='major', labelsize=10, labelbottom=False, bottom=False, top=False, labeltop=True)
    plt.show()
    return reduced_corr_matrix


def draw_a_multiplied_correlation_matrix(paths_x, paths_y, labels, title, if_show_plot = True):
    try:
        n = len(paths)
    except:
        n = 2
    multi_corr_x = np.corrcoef(paths_x, paths_x)
    reduced_corr_matrix_x = multi_corr_x[0:n,0:n]
    multi_corr_y = np.corrcoef(paths_y, paths_y)
    reduced_corr_matrix_y = multi_corr_y[0:n, 0:n]
    XY_corr = [abs(a * b) for a, b in zip(reduced_corr_matrix_x, reduced_corr_matrix_y)]
    #print(XY_corr)

    n = len(XY_corr)
    m = len(XY_corr[0])

    #print(n)
    #print(m)

    for a in range(n):
        for b in range(m):
            if XY_corr[a][b] != XY_corr[a][b]:
                XY_corr[a][b] = 0


    #print(XY_corr)

    if if_show_plot:
        plt.figure(figsize=(12, 8))
        plt.title(title)
        sns.heatmap(XY_corr, annot = True, xticklabels = labels, yticklabels = labels)
        plt.tick_params(axis='both', which='major', labelsize=10, labelbottom=False, bottom=False, top=False, labeltop=True)
        plt.show()
    return XY_corr

def get_all_imprtant_correlations(datafile):
    #open the datafile
    f = open(datafile, 'r', encoding='utf-8')
    all_data = json.load(f)
    f.close()

    ##Basic Paths
    chair_path = get_item_of_class_position(all_data, class_no = 56)
    person_path = get_item_of_class_position(all_data, class_no = 0)
    laptop_path = get_item_of_class_position(all_data, class_no = 63)

    #Hands
    hand_path = get_right_hand_position(all_data)
    hand2_path = get_left_hand_position(all_data)

    ####Foods Paths####
    banana_path = get_item_of_class_position(all_data, class_no=46)
    apple_path = get_item_of_class_position(all_data, class_no=47)
    sandwich_path = get_item_of_class_position(all_data, class_no=48)
    orange_path = get_item_of_class_position(all_data, class_no=49)
    broccoli_path = get_item_of_class_position(all_data, class_no=50)
    carrot_path = get_item_of_class_position(all_data, class_no=51)

    ####Cutlery Paths####
    knife_path = get_item_of_class_position(all_data, class_no = 43)
    spoon_path = get_item_of_class_position(all_data, class_no = 44)
    fork_path = get_item_of_class_position(all_data, class_no = 42)

    ####Tableware Paths####
    bottle_path = get_item_of_class_position(all_data, class_no=39)
    wine_glass_path = get_item_of_class_position(all_data, class_no=40)
    cup_path = get_item_of_class_position(all_data, class_no=41)
    bowl_path = get_item_of_class_position(all_data, class_no=45)

    path_length = len(hand_path[0])

    ###################################################################
    #######             Vorrelations to right hand               ######
    #################################################################
    hand1_corrs = []
    corr = []
    corr_window = 50
    for path in [hand2_path, banana_path, apple_path,sandwich_path, orange_path, broccoli_path, carrot_path, knife_path, spoon_path, fork_path, bottle_path, wine_glass_path, cup_path, bowl_path]:
        corr = []
        for r in range(path_length // corr_window):
            paths = [hand_path[0][r * corr_window:(r + 1) * corr_window], path[0][r * corr_window:(r + 1) * corr_window]]
            paths2 = [hand_path[1][r * corr_window:(r + 1) * corr_window], path[1][r * corr_window:(r + 1) * corr_window]]
            corr_matrix = draw_a_multiplied_correlation_matrix(paths_x=paths, paths_y=paths2, labels=["A","B"], title="Title",if_show_plot=False)
            #print(corr_matrix)
            corr.append(corr_matrix[0][1])
        hand1_corrs.append(corr)

    ####Give names to correlations
    hand_to_hand_corr = hand1_corrs[0]
    hand_to_banana_corr = hand1_corrs[1]
    hand_to_apple_corr = hand1_corrs[2]
    hand_to_sandwich_corr = hand1_corrs[3]
    hand_to_bottle_corr = hand1_corrs[10]
    hand_to_cup_corr = hand1_corrs[12]
    hand_to_bowl_corr = hand1_corrs[13]

    plt.plot(hand_to_hand_corr, "b-", label="Hand to Hand Corr")
    plt.plot(hand_to_banana_corr, "b--", label="Hand to Banana Corr")
    plt.plot(hand_to_apple_corr, "g-", label="Hand to Apple Corr")
    plt.plot(hand_to_sandwich_corr, "g--", label="Hand to Sandwich Corr")
    plt.plot(hand_to_bottle_corr, "c-", label="Hand to Bottle Corr")
    plt.plot(hand_to_cup_corr, "r-", label="Hand to Cup Corr")
    plt.plot(hand_to_bowl_corr, "r--", label="Hand to Bowl Corr")

    plt.ylabel('Correlation Value')
    plt.xlabel("Frame Number")
    plt.title("Correlations between object pairs computed for short windows.")
    plt.legend()
    plt.show()

    return hand1_corrs

def compute_scores(correlations):
    score = 0
    for correlation in correlations:
        for n in range(len(correlation)):
            if n == 0:
                if correlation[0] > 0.8:
                    score = score + 1
            if n == 1:
                if correlation[n] > 0.8:
                    score = score + 1
                if correlation[n-1] > 0.8:
                    score = score + 1
            if n >= 2:
                if correlation[n] > 0.8:
                    score = score + 1
                if correlation[n-1] > 0.8:
                    score = score + 1
                if correlation[n-2] > 0.8:
                    score = score + 1
    print("Videa's score is " + str(score) + ".")
    return score





if __name__ == "__main__":
    data_file = "Data/JSON_FILES/Video_114.json"

    if True:
        get_all_imprtant_correlations(data_file)

    if False:
        f = open(data_file, 'r', encoding='utf-8')
        all_data = json.load(f)
        f.close()

        hand_path = get_right_hand_position(all_data)
        hand2_path = get_left_hand_position(all_data)
        chair_path = get_item_of_class_position(all_data, class_no = 56)
        person_path = get_item_of_class_position(all_data, class_no = 0)
        laptop_path = get_item_of_class_position(all_data, class_no = 63)

        ####Foods Paths####
        apple_path = get_item_of_class_position(all_data, class_no=47)

        ####Cutlery Paths####
        knife_path = get_item_of_class_position(all_data, class_no = 43)
        spoon_path = get_item_of_class_position(all_data, class_no = 44)
        fork_path = get_item_of_class_position(all_data, class_no = 42)

        ####Tableware Paths####
        cup_path = get_item_of_class_position(all_data, class_no=41)


        path_length = len(hand_path[0])
        print("Path length: " + str(path_length))

        plt.plot(cup_path[0])
        plt.plot(chair_path[0])
        plt.plot(hand_path[0])
        plt.plot(laptop_path[0])
        plt.ylabel('some numbers')
        plt.show()

        ####Corrlelations:
        corr1 = np.corrcoef(cup_path[0], chair_path[0])
        print(corr1)
        corr2 = np.corrcoef(cup_path[0], hand_path[0])
        print(corr2)
        corr3 = np.corrcoef(cup_path[0], person_path[0])
        print(corr3)
        corr4 = np.corrcoef(cup_path[0], hand2_path[0])
        print(corr4)
        corr5 = np.corrcoef(chair_path[0], hand2_path[0])
        print(corr5)
        corr6 = np.corrcoef(chair_path[0], person_path[0])
        print(corr6)

        plt.plot(person_path[0])
        plt.plot(chair_path[0])
        plt.plot(hand2_path[0])
        plt.ylabel('some numbers')
        plt.show()

        ##### Try the matrix ######
        title = "Correlation between items' positions (X)"
        title2 = "Correlation between items' positions (Y)"
        title3 = "Correlation between items' positions (Multiplied)"
        paths = [cup_path[0], hand_path[0], laptop_path[0], hand2_path[0]]
        paths2 = [cup_path[1], hand_path[1], laptop_path[1], hand2_path[1]]
        labels_list = ["Cup", "Right Hand", "Laptop", "Left Hand"]

        #X_Y_XY correlation plots
        #draw_a_correlation_matrix(paths, labels = labels_list, title=title)
        #draw_a_multiplied_correlation_matrix(paths_x = paths, paths_y = paths2, labels = labels_list, title=title3)


        #Try for shorter time windows
    #    pathsA = [cup_path[0][0:100], hand_path[0][0:100], chair_path[0][0:100], hand2_path[0][0:100]]
    #    paths2A = [cup_path[1][0:100], hand_path[1][0:100], chair_path[1][0:100], hand2_path[1][0:100]]
    #    pathsB = [cup_path[0][100:200], hand_path[0][100:200], chair_path[0][100:200], hand2_path[0][100:200]]
    #    paths2B = [cup_path[1][100:200], hand_path[1][100:200], chair_path[1][100:200], hand2_path[1][100:200]]
    #    pathsC = [cup_path[0][200:300], hand_path[0][200:300], chair_path[0][200:300], hand2_path[0][200:300]]
    #    paths2C = [cup_path[1][200:300], hand_path[1][200:300], chair_path[1][200:300], hand2_path[1][200:300]]
    #
    #    draw_a_multiplied_correlation_matrix(paths_x=pathsA, paths_y=paths2A, labels=labels_list, title=title3)
    #    draw_a_multiplied_correlation_matrix(paths_x=pathsB, paths_y=paths2B, labels=labels_list, title=title3)
    #    draw_a_multiplied_correlation_matrix(paths_x=pathsC, paths_y=paths2C, labels=labels_list, title=title3)

        labels_list = ["Cup", "Right Hand", "Laptop", "Left Hand", "Apple", "Chair", "Knife", "Spoon", "Fork"]
        corr_window = 50
        corrs = []
        for r in range(path_length//corr_window):
            paths = [cup_path[0][r*corr_window:(r+1)*corr_window], hand_path[0][r*corr_window:(r+1)*corr_window], laptop_path[0][r*corr_window:(r+1)*corr_window], hand2_path[0][r*corr_window:(r+1)*corr_window], apple_path[0][r*corr_window:(r+1)*corr_window], chair_path[0][r*corr_window:(r+1)*corr_window], knife_path[0][r*corr_window:(r+1)*corr_window], spoon_path[0][r*corr_window:(r+1)*corr_window], fork_path[0][r*corr_window:(r+1)*corr_window]]
            paths2 = [cup_path[1][r*corr_window:(r+1)*corr_window], hand_path[1][r*corr_window:(r+1)*corr_window], laptop_path[1][r*corr_window:(r+1)*corr_window], hand2_path[1][r*corr_window:(r+1)*corr_window], apple_path[1][r*corr_window:(r+1)*corr_window], chair_path[1][r*corr_window:(r+1)*corr_window], knife_path[1][r*corr_window:(r+1)*corr_window], spoon_path[1][r*corr_window:(r+1)*corr_window], fork_path[1][r*corr_window:(r+1)*corr_window]]
            corr_matrix = draw_a_multiplied_correlation_matrix(paths_x=paths, paths_y=paths2, labels=labels_list, title=title3 + " Frames: " + str(r*corr_window) + "-" + str((r+1)*corr_window), if_show_plot=False)
            corrs.append(corr_matrix)

        cup_hand_corr = []
        laptop_hand_corr = []
        apple_hand_corr = []
        for q in range(len(corrs)):
            print(q)
            for i in range(corr_window):
                cup_hand_corr.append(corrs[q][0][1])
                laptop_hand_corr.append(corrs[q][2][1])
                apple_hand_corr.append(corrs[q][4][1])


        plt.plot(cup_path[0], "b--")
        plt.plot(hand_path[0], "r--")
        plt.plot(laptop_path[0], "g--")

        plt.plot(cup_path[1], "b-")
        plt.plot(hand_path[1], "r-")
        plt.plot(laptop_path[1], "g-")

        plt.ylabel('Frame Number')
        plt.xlabel("Positions in pixels")
        plt.title("X-paths, Y-paths.")
        plt.show()


        plt.plot(cup_hand_corr, "b-", label = "Cup to Hand Corr")
        plt.plot(laptop_hand_corr, "g-", label = "Laptop to Hand Corr")
        plt.plot(apple_hand_corr, "r-", label="Apple to Hand Corr")

        plt.ylabel('Correlation Value')
        plt.xlabel("Frame Number")
        plt.title("Correlations between object pairs computed for short windows.")
        plt.legend()
        plt.show()

        #print(chair_path[0])


