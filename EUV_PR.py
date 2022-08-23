# 2022.08.22 EUV PR -> make new image for testing
# 2022.08.23 

from multiprocessing.dummy import Array
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd

# parameter
cropSize: int = 150
GL_limit = 60
imageNo = 10
result = []


# partial_sum
def partial_sum(arr, a, b):
    arr = arr.tolist()
    arr = [0] + arr
    partial_sum = [0] * len(arr)
    for i in range(1, len(arr)):
        partial_sum[i] = partial_sum[i-1] + arr[i]

    partial_sum = partial_sum[1:]

    if a == 0:
        return partial_sum[b]
    else: 
        return partial_sum[b] - partial_sum[a-1]
    

# main
if __name__ == "__main__":
    for i in range(1,imageNo):
        fileNo = '{0:09}'.format(i)

        # open image
        filePath = "C:/Users/kim-beomzu/Desktop/python_test/EUV_PR_histogram/EVU_PR_test.tif" # << file name 바꿔주면 완료
        imageArray = cv.imread(filePath, cv.IMREAD_GRAYSCALE)

        # image crop
        width, height = imageArray.shape
        imageArray_crop = imageArray[cropSize : width, cropSize : height]
        width_crop, height_crop = imageArray_crop.shape

        # reshape crop image
        imageArray_crop_reshape = np.reshape(imageArray_crop, (1, width_crop * height_crop))
        counts, bins = np.histogram(imageArray_crop_reshape, bins = 2**8)

        # histogram data
        hist = imageArray_crop_reshape[0] #<< numeric data
        
        holeArea = partial_sum(counts, 0, GL_limit)
        result.append(holeArea)
        
        # figure1
        plt.figure(1)
        plt.imshow(imageArray, cmap = 'gray')
        ax = plt.gca()

        rect = patches.Rectangle(
            (cropSize, cropSize),
        width-cropSize-1,
        height-cropSize-1,
        linewidth=2,
        edgecolor='r',
        facecolor='none')
        ax.add_patch(rect)
        # plt.show()
        plt.savefig("C:/Users/kim-beomzu/Desktop/python_test/EUV_PR_histogram/area/" + fileNo + "_1.png") # << file name 바꿔주면 완료
        
        # figure2
        plt.figure(2)
        plt.hist(hist, bins = 2**8, color = 'blue')
        plt.axvline(x = GL_limit, color='r', linewidth=1)
        # plt.show()
        plt.savefig("C:/Users/kim-beomzu/Desktop/python_test/EUV_PR_histogram/hist/" + fileNo + "_2.png") # << file name 바꿔주면 완료



    result = np.array(result)
    result = result.T
    
    print(result)

    # save data
    df = pd.DataFrame(result)
    df.to_csv("test_EUV_PR.csv", index = False)


    print("Done!!")
    print("Done!!")
    print("Done!!")
    print("Done!!")
    
    

    


