# 2022.08.01 画像読み込みおよびデータ処理
# 2022.08.02 
# 2022.08.04 hard coding (detect maximal value, minimal value)
# 2022.08.05 calculate contrast
# 2022.08.08 data type, size, reshape etc..

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks

####################### parameter 
# 1 : Bottom GL
# 2 : contrast 
# 3 : difference
output = 3 # <<<<<<<< ここの値を修正して、検出値を変えることができる。
blurCount = 1
analysisCount = 35 
limit = 150
blurLevel = 3
point_no =  25
chip_no = 65 # <<<<<<<<<< 레이어가 바뀌면 여기 조정
num = point_no * chip_no 

for i in range (0, 10):
    matrix_contrast =  np.zeros((num,8))
    matrix_difference = np.zeros((num,8))
    matrix_BCD = np.zeros((num,8))
####################### parameter 


# 1. open image & define parameter
def readImage(fileName):
    global ImageArray
    global height, width
    
    fileNo = '{0:09}'.format(fileName)
    
    # open image
    filePath = "C:/Users/kim-beomzu/Desktop/python_test/" + fileNo + "/"+ fileNo + "HDU001.tif"
    ImageArray = cv.imread(filePath, cv.IMREAD_GRAYSCALE)


# 2. smoothing
def smoothingImage():
    global ImageArray_smoothing
    ImageArray_smoothing = cv.blur(ImageArray, (blurLevel, blurLevel))
    for i in range(0,blurCount):
        ImageArray_smoothing = cv.blur(ImageArray_smoothing, (blurLevel, blurLevel))


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

# 6. define value of each contrast
def defineValue():
    global A,B,C
    global A_array, B_array, C_array
    global contrast, difference
    global contrast_array, difference_array, BGL_array

    # devide 1,0
    check = [0] * len(maxMin_cut)
    for i in range(0, len(maxMin_cut)):
        if result_smoothing[maxMin_cut[i]] > 150:
            check[i] = 1         

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
    BGL_array = [i for i in B_array if i != 0]

    # show result 
    if output == 1:
        print(A_array)
    elif output == 2:
        print(contrast_array)
    elif output == 3:
        print(difference_array)
    else:
        print("error :: press Shift + f5")

    # resize array
    while len(contrast_array) < 8:
        contrast_array.append(0)
    
    while len(difference_array) < 8:
        difference_array.append(0)

    while len(BGL_array) < 8:
        BGL_array.append(0)
    
# 7. matrix result
def matrix_result():
    matrix_contrast[j-1,:] = contrast_array
    matrix_difference[j-1,:] = difference_array
    matrix_BCD[j-1,:] = BGL_array

# data table 
def table_data():
    global matrix_A, matrix_B, matrix_C
    menu = ["no.", "wafer_x", "wafer_y", "point", \
            "value1", "value2", "value3", "value4", "value5", "value6", "value7", "value8"]
    
    # no
    no = np.arange(1,num + 1).reshape(num, 1)
    
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
                "5"] #<<<<<<<<<< 레이어가 바뀌면 여기 조정
    wafer_x = np.repeat(wafer_x, 25)
    wafer_x = wafer_x.reshape(num,1)

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
                "0"] #<<<<<<<<<< 레이어가 바뀌면 여기 조정

    wafer_y = np.repeat(wafer_y, 25)
    wafer_y = wafer_y.reshape(num,1)

    # point
    point = np.array(range(1,26)).tolist() * int(num/25)
    point = np.array(point)
    point = point.reshape(num,1)

    # matrix (A = BottomContrast, B = contrast, C = contrast)
    table_data = np.hstack([no, wafer_x, wafer_y, point])
    matrix_A = np.hstack([table_data, matrix_BCD])
    matrix_A = np.vstack([menu, matrix_A])
    matrix_B = np.hstack([table_data, matrix_contrast])
    matrix_B = np.vstack([menu, matrix_B])
    matrix_C = np.hstack([table_data, matrix_difference])
    matrix_C = np.vstack([menu, matrix_C])
    

# appendix.change dataframe of ImageArray and save file
def array2csv():
    if output == 1:
        #matrix_A.tolist
        df = pd.DataFrame(matrix_A)
        df.to_csv('B_value.csv', index = False)
    elif output == 2:
        #matrix_B.tolist
        df = pd.DataFrame(matrix_B)
        df.to_csv('contrast.csv', index = False)
    elif output == 3:
        #matrix_C.tolist
        df = pd.DataFrame(matrix_C)
        df.to_csv('difference.csv', index = False)
    else:
        print("error :: press Shift + f5")



def graph():
    plt.figure(1)
    plt.imshow(ImageArray_smoothing, cmap='gray')
    for i in range(0, len(peakMaximum)):
        plt.axvline(peakMaximum[i], color = 'white', linestyle = '--')
    for i in range(0, len(peakMinimum)):
        plt.axvline(peakMinimum[i], color = 'orange')
    plt.plot(result_smoothing, color = "yellow", marker = '')
    plt.show()


    plt.figure(2)
    plt.imshow(ImageArray, cmap='gray')
    for i in range(0, len(peakMaximum)):
        plt.axvline(peakMaximum[i], color = 'white', linestyle = '--')
    for i in range(0, len(peakMinimum)):
        plt.axvline(peakMinimum[i], color = 'orange')
    plt.plot(result_original, color = "yellow", marker = '')



# main
if __name__ == "__main__":
    for j in range(1, analysisCount + 1):
        readImage(j)
        smoothingImage()
        average()
        peak()
        cutData()
        defineValue()
        matrix_result()
    table_data()
    # graph()
    array2csv()

