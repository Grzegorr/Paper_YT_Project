from Process_Video import *
from DataProcessing import *
from CorrelationExtraction import *
import tensorflow as tf

#########################################################################
########         Checking for available GPUs                        #####
#########################################################################
#print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
#gpus = tf.config.list_physical_devices('GPU')
#for gpu in gpus:
#    print("Name:", gpu.name, "  Type:", gpu.device_type)

name = "videoplayback_000"

video_path = "Data/FINAL_ALGORITHM/Dataset/" + name + ".mp4"
processed_video_name = name + ".mp4"
dest_file = "Data/JSON_FILES/" + name + ".json"
corr_dest_file = "Data/JSON_CORRS/" + name + ".json"


#########################################################################
############# Code to run a video through the algorithm #################
#########################################################################
if True:
    print("I am running a whole video! TEMP WILL BE CLEANED!")

    clean_temp_files()
    video_into_temporary_frames(video_path=video_path)
    net = read_pre_trained_YOLO()
    import_open_pose()
    op, classes, COLORS = load_packages_classes_etc()
    opWrapper = run_open_pose(image_path="image_path", op=op, saving_path="save_path")

    files = glob.glob("./TEMP_FILES/*")
    for i in range(len(files)):
        print("\nProcessing a frame no: " + str(i) + "\n")
        image_path = "./TEMP_FILES/frame_" + str(i) + ".jpg"
        image_path_2 = "./TEMP_FILES_2/frame_" + str(i) + ".jpg"
        save_path = "frame_" + str(i) + ".jpg"
        single_frame_data = process_a_frame_Video(op, classes, COLORS, image_path, image_path_2, save_path=save_path, net=net, opWrapper=opWrapper, if_print=False)
        # print(single_frame_data)
        #### SAVING DATA ####
        if not exists(dest_file):
            output_file = open(dest_file, 'w', encoding='utf-8')
            json.dump([single_frame_data], output_file)
            # json.dump([0,0,0,0,0], output_file)
            output_file.close()
        else:
            f = open(dest_file, 'r', encoding='utf-8')
            all_data = json.load(f)
            f.close()
            all_data.append(single_frame_data)
            output_file = open(dest_file, 'w', encoding='utf-8')
            json.dump(all_data, output_file)
            # output_file.write("\n")
            output_file.close()

    stitch_frames_into_video(processed_video_name)

    ###############################################
    #####      Now data processing     ###############
    #####   Smothing hand positions etc. #############

    replace_padding_with_prevous_value_hands(dest_file, dest_file)

    ###############################################
    #####    Extracting Correlations        #########
    ###############################################

    correlations = get_all_imprtant_correlations(dest_file)
    compute_scores(correlations)

    output_file = open(corr_dest_file, 'w', encoding='utf-8')
    json.dump(correlations, output_file)
    output_file.close()