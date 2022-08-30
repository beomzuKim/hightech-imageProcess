# 2022.08.22 EUV PR -> make new image for testing
# 2022.08.23 

import numpy as np
import cv2 as cv

# SEQUENCE 
''' 
* 1. 취득한 화상에서 이진처리를 통해 Hole 부분 추적
* 2. Dummy hole 캔슬링 (현시점에서 어떻게 해야하는지 모름 - 질문)
* 3. Smoothing 필터로 노이즈 완화
* 4. 각 Hole(약 25개의 홀)마다 최댓값을 검출후 O(NlogN)복잡도를 가진 알고리즘으로 list 정렬
* 5. 중앙값(mid = lower + upper //2)으로 정의하여 histogram 산출 (중앙값을 가지는 ROI 범위설정 및 histogram 산출)
* 6. 복수 plotting을 통해 exposure power 별로 그래프를 그려냄
'''

# main
if __name__ == "__main__":
    # open image
    filePath = "C:/Users/kim-beomzu/Desktop/python_test/EUV_PR_histogram/EVU_PR_test2.tif" # << file name 바꿔주면 완료
    imageOrigin = cv.imread(filePath, cv.IMREAD_GRAYSCALE)
    imageOrigin_blur = cv.GaussianBlur(imageOrigin,(3,3),5)

    edges = cv.Canny(imageOrigin_blur, 70,180)

    # cv.imshow("origin", imageOrigin)
    # cv.imshow("canny", edges)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    # # binary image
    # dst = cv.inRange(imageOrigin, 0,70)
    # kernel = cv.getStructuringElement(cv.MORPH_RECT,(10,10))
    # dilation = cv.dilate(dst, kernel, iterations = 1)

    # # detect circles
    circles = cv.HoughCircles(edges,
                              cv.HOUGH_GRADIENT,
                              1, 30, 
                              param1 = 100, 
                              param2 = 20,
                              minRadius= 0,
                              maxRadius= 30)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            cv.circle(imageOrigin_blur, (i[0], i[1]), i[2], (255,0,0),2)
            cv.circle(imageOrigin_blur, (i[0], i[1]), 2, (255,0,0),1)
        
        print(circles[0,:])
           
    # result
        cv.imshow("Origin", imageOrigin_blur)
        cv.imshow("Canny", edges)
        cv.waitKey()
        cv.destroyAllWindows()


    # cv.imwrite('C:/Users/kim-beomzu/Desktop/python_test/EUV_PR_histogram/Test_gray.tif', test)

