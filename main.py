import numpy as np
import json


if __name__ == '__main__':
    if False:
        arr1 = [1.0,1.01,1.1,1.05,1.1]
        arr2 = [5.0, 5.05, 5.5, 5.25, 5.5]
        arr3 = [6.0, 6.05, 6.5, 6.25, 6.5]
        print(arr1)
        print(np.corrcoef(arr1,arr1))
        print(np.corrcoef(arr1,arr2))
        print(np.corrcoef(arr1, arr3))

    if False:
        array = [0, 1]
        if array == [0]:
            print("It works!")

    if True:
        JSON_path = "Data/JSON_FILES/Video_115.json"
        f = open(JSON_path, 'r', encoding='utf-8')
        all_data = json.load(f)
        f.close()

        example_open_pose = all_data[0][1]
        print(len(example_open_pose[0]))
        print(example_open_pose)


    if True:
        JSON_path = "Data/JSON_FILES/videoplayback_000.json"
        f = open(JSON_path, 'r', encoding='utf-8')
        all_data = json.load(f)
        f.close()

        example_open_pose = all_data[0][1]
        print(len(example_open_pose[0]))
        print(example_open_pose)

