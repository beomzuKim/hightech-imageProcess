# 2022.08.01 画像読み込みおよびデータ処理
# 2022.08.02 
# 2022.08.04 hard coding (detect maximal value, minimal value)
# 2022.08.05 calculate contrast

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks


# plt.close("all")
####################### parameter 
limit = 150
blurLevel = 3


####################### parameter 


# 1. open image & define parameter
def readImage(fileName):
    global ImageArray
    global height, width

    # int2str fileName and numbering
    if fileName < 10:
        fileNo = "00000000" + str(fileName)
    elif fileName < 100:
        fileNo = "0000000" + str(fileName)
    elif fileName < 1000:
        fileNo = "000000" + str(fileName)
    else:
        fileNo = "00000" + str(fileName)

    # open image
    filePath = "C:/Users/kim-beomzu/Desktop/python_test/" + fileNo + "/"+ fileNo + "HDU001.tif"
    ImageArray = cv.imread(filePath, cv.IMREAD_GRAYSCALE)

    # define parameter
    height, width  = ImageArray.shape


# 2. smoothing
def smoothingImage(blurCount):
    global ImageArray_smoothing
    ImageArray_smoothing = cv.blur(ImageArray, (blurLevel,blurLevel))
    for i in range(0,blurCount):
        ImageArray_smoothing = cv.blur(ImageArray_smoothing, (blurLevel,blurLevel))


# 3. average distribution
def average():
    global result_original
    global result_smoothing
    
    result_original = []
    result_smoothing = []
    for i in range(0,512):
        sum_original = sum(ImageArray[:,i]) / len(ImageArray)
        result_original.append(sum_original)
        sum_smoothing = sum(ImageArray_smoothing[:,i]) / len(ImageArray_smoothing)
        result_smoothing.append(sum_smoothing)
    


# 4. detect each peak
def peak():
    global peakMaximum, peakMinimum
    global maxMin
    r = [-1] * len(result_smoothing)
    result_smoothing_re = [0] * len(result_smoothing)

    for i in range(0,512):
        result_smoothing_re[i] = result_smoothing[i] * r[i]

    # find peak
    peakMaximum, _ = find_peaks(result_smoothing)
    peakMinimum, _ = find_peaks(result_smoothing_re)

    # concatenate peak and sorting
    maxMin = peakMaximum.tolist() + peakMinimum.tolist()
    maxMin.sort()


# 5. cutData between each data and remove data
def cutData():
    limitGL = limit
    global maxMin_cut
    count = 0
    maxMin_cut = maxMin[:]

    # cutting front data
    while result_smoothing[maxMin[count]] < limit:  
        maxMin_cut.remove(maxMin[count])
        count += 1

    # cutting back data
    count = -1
    while result_smoothing[maxMin[count]] < limit:
        maxMin_cut.remove(maxMin[count])
        count -= 1
    #print(maxMin_cut)


def defineValue():
    global A,B,C
    global A_array, B_array, C_array
    global contrast, difference
    global contrast_array, difference_array

    # devide 1,0
    check = [0] * len(maxMin_cut)
    for i in range(0, len(maxMin_cut)):
        if result_smoothing[maxMin_cut[i]] > 150:
            check[i] = 1         
    #print(check)

    # count zeros
    count = 0
    countZeros = [0] * len(check)
    for i in range(0, len(check)):
        if check[i] == 0:
            count += 1
            #print("0 검출, count값:", count)
        else:
            count = 0
            #print("1 검출, count값:", count)
        countZeros[i] = count
    #print(countZeros)
    
    
    # detect data A, B, C, contrast, difference
    A_array = [0] * len(countZeros)
    B_array = [0] * len(countZeros)
    C_array = [0] * len(countZeros)
    contrast_array = [0] * len(countZeros)
    difference_array = [0] * len(countZeros)

    for i in range(0, len(countZeros)):
        if countZeros[i] == 0 and countZeros[i-1] == 3:
            # define data
            A = result_smoothing[maxMin_cut[i-3]]
            B = result_smoothing[maxMin_cut[i-2]]
            C = result_smoothing[maxMin_cut[i-1]]
            contrast = B - 0.5 * (A + C)
            difference = abs(A - C)

            # insert data type:array
            A_array[i] = A
            B_array[i] = B
            C_array[i] = C
            contrast_array[i] = contrast
            difference_array[i] = difference

    # remove 0
    A_array = [i for i in A_array if i != 0]
    B_array = [i for i in B_array if i != 0]
    C_array = [i for i in C_array if i != 0]
    contrast_array = [i for i in contrast_array if i != 0]
    difference_array = [i for i in difference_array if i != 0]

    # resize array
    while len(contrast_array) < 8:
        contrast_array.append(0)
    
    while len(difference_array) < 8:
        difference_array.append(0)
    
    print("contrast:", contrast_array)
    print("difference:", difference_array)
    

def matrix_result():
    global matrix_contrast
    global matrix_difference
    #matrix_contrast = np.array([[0]*8 for i in range(1,5)])
    #matrix_difference = np.array([[0]*8 for i in range(1,5)])
    #matrix_contrast = np.vstack([matrix_contrast, contrast_array])
    #matrix_difference = np.vstack([matrix_difference, difference_array])
    #print(matrix_contrast)
    #print(contrast_array)
    #print(difference_array)
        

    #print("contrast:", contrast_array)
    

# data table 
def matrix_menu():
    menu = ["no.", "wafer_x", "wafer_y", "point", \
        "value1", "value2", "value3", "value4", "value5", "value6", "value7", "value8"]
    matrix = [[0]*11 for i in range(1,1625)]
    
    # no
    no = np.arange(1,1625 + 1).reshape(1625, 1)
    
    # wafer_x
    wafer_x = [ "-5",\
                "-4","-4","-4","-4","-4",\
                "-3","-3","-3","-3","-3","-3","-3",\
                "-2","-2","-2","-2","-2","-2","-2",\
                "-1","-1","-1","-1","-1","-1","-1","-1",\
                "0","0","0","0","0","0","0","0","0",\
                "1","1","1","1","1","1","1","1",\
                "2","2","2","2","2","2","2",\
                "3","3","3","3","3","3","3",\
                "4","4","4","4","4",\
                "5"]
    wafer_x = np.repeat(wafer_x, 25)
    wafer_x = wafer_x.reshape(1625,1)

    # wafer_y            
    wafer_y = [ "0",\
                "-2","-1","0","1","2",\
                "-3","-2","-1","0","1","2","3",\
                "-3","-2","-1","0","1","2","3",\
                "-4","-3","-2","-1","0","1","2","3",\
                "-4","-3","-2","-1","0","1","2","3","4",\
                "-4","-3","-2","-1","0","1","2","3",\
                "-3","-2","-1","0","1","2","3",\
                "-3","-2","-1","0","1","2","3",\
                "-2","-1","0","1","2",\
                "0"]
    wafer_y = np.repeat(wafer_y, 25)
    wafer_y = wafer_y.reshape(1625,1)

    # point
    point = np.array(range(1,26)).tolist() * int(1625/25)
    point = np.array(point)
    point = point.reshape(1625,1)

    
    #print(point)
    matrix = np.hstack([no, wafer_x, wafer_y, point])
    #print(matrix)



# appendix.change dataframe of ImageArray and save file
def array2csv():
    matrix_difference.tolist
    df = pd.DataFrame(matrix_difference)
    df.to_csv('sample1.csv', index = False)


# main
if __name__ == "__main__":
    for j in range(1, 20):
        readImage(j)
        smoothingImage(1)
        average() # << 
        peak()    # <<
        cutData()
        defineValue()
        matrix_result()


    #array2csv()
    matrix_menu()


  


"""
    plt.figure(1)
    plt.imshow(ImageArray_smoothing, cmap='gray')
    for i in range(0, len(peakMaximum)):
        plt.axvline(peakMaximum[i], color = 'white', linestyle = '--')
    for i in range(0, len(peakMinimum)):
        plt.axvline(peakMinimum[i], color = 'orange')
    plt.plot(result_smoothing, color = "yellow", marker = '')
    plt.show()
"""


"""
    plt.figure(2)
    plt.imshow(ImageArray, cmap='gray')
    for i in range(0, len(peakMaximum)):
        plt.axvline(peakMaximum[i], color = 'white', linestyle = '--')
    for i in range(0, len(peakMinimum)):
        plt.axvline(peakMinimum[i], color = 'orange')
    plt.plot(result_original, color = "yellow", marker = '')
""" 



