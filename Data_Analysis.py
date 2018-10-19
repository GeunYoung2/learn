## 영상 처리 및 데이터 분석 툴
from tkinter import *;
import os.path;
import math
from tkinter.filedialog import *
from tkinter.simpledialog import *
import struct;
import threading
import matplotlib.pyplot as plt
import xlwt
import xlsxwriter
import pymysql
import csv
import sqlite3
import xlrd
import xlwt

## 함수 선언부
###################Menu 1 (파일메뉴)############################
def loadImage(fname):
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    fsize = os.path.getsize(fname)
    inH = inW = int(math.sqrt(fsize))
    inImage = []
    tmpList = []
    for i in range(inH):
        tmpList = []
        for k in range(inW):
            tmpList.append(0)
        inImage.append(tmpList)

    fp = open(fname, 'rb')
    for i in range(inH):
        for k in range(inW):
            inImage[i][k] = int(ord(fp.read(1)))
    fp.close()


def openFile():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    filename = askopenfilename(parent=window,
                               filetypes=(("RAW파일", "*.raw"), ("모든파일", "*.*")))
    loadImage(filename)
    equal()


def saveFile():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    saveFp = asksaveasfile(parent=window, mode='wb',
                           defaultextension="*.raw", filetypes=(("RAW파일", "*.raw"), ("모든파일", "*.*")))
    for i in range(outW):
        for k in range(outH):
            saveFp.write(struct.pack('B', outImage[i][k]))

    saveFp.close()


def exitFile():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    pass


def display():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    if canvas != None:
        canvas.destroy()

    VIEW_X, VIEW_Y = 256, 256
    if VIEW_X >= outW or VIEW_Y >= outH:
        VIEW_X = outW
        VIEW_Y = outH
        step = 1
    else:
        step = int(outW / VIEW_X)

    window.geometry(str(VIEW_X * 2) + 'x' + str(VIEW_Y * 2))
    canvas = Canvas(window, width=VIEW_X, height=VIEW_Y)
    paper = PhotoImage(width=VIEW_X, height=VIEW_Y)
    canvas.create_image((VIEW_X / 2, VIEW_X / 2), image=paper, state='normal')

    def putPixel():
        for i in range(0, outH, step):
            for k in range(0, outW, step):
                data = outImage[i][k]
                paper.put('#%02x%02x%02x' % (data, data, data),
                          (int(k / step), int(i / step)))

    threading.Thread(target=putPixel).start()
    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))

#################################################################################


#####################Menu2(화소점처리)############################################################
def equal():  # 동일 영상 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    outW = inW;
    outH = inH;
    outImage = [];
    tmpList = []
    for i in range(outH):
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)

    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k]

    display()


def addImage():  # 밝게하기
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    outW = inW;
    outH = inH;
    outImage = [];
    tmpList = []
    for i in range(outH):
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    value = askinteger('밝게하기', '밝게할 값-->', minvalue=1, maxvalue=255)
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] + value > 255:
                outImage[i][k] = 255
            else:
                outImage[i][k] = inImage[i][k] + value
    display()

def multiplyImage() : # 영상 곱하기 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    outW = inW; outH = inH;
    for i in range(outH) :
        tmpList=[]
        for k in range(outW) :
            tmpList.append(0)
        outImage.append(tmpList)
    value = askinteger('밝게 곱하기', '밝게할 값-->', minvalue=1, maxvalue=255)
    for i in range(inH) :
        for k in range(inW):
            if inImage [i][k] * value > 255 :
                outImage[i][k] = 255
            elif inImage[i][k] * value < 0 :
                outImage[i][k] = 0
            else :
                outImage[i][k] = inImage[i][k] * value
    display()

def decreaseImage() :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    outW = inW; outH = inH;
    for i in range(outH) :
        tmpList=[]
        for k in range(outW) :
            tmpList.append(0)
        outImage.append(tmpList)

    value = askinteger('어둡게빼기', '어둡게할 값-->', minvalue=1, maxvalue=255)
    for i in range(inH) :
        for k in range(inW):
            if inImage[i][k] - value < 0 :
                outImage[i][k] = 0
            else :
                outImage[i][k] = inImage[i][k] - value

def divisionImage() : # 영상 나누기 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    outW = inW; outH = inH;
    for i in range(outH) :
        tmpList=[]
        for k in range(outW) :
            tmpList.append(0)
        outImage.append(tmpList)

    value = askinteger('어둡게나누기', '어둡게할 값-->', minvalue=1, maxvalue=255)
    for i in range(inH) :
        for k in range(inW):

            if inImage[i][k] // value > 255:
                outImage[i][k] = 255
            elif inImage[i][k] // value < 0:
                  outImage[i][k] = 0
            else:
                outImage[i][k] = inImage[i][k] // value

    display()

def morphing():  # 합성하기
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    outW = inW
    outH = inH

    filename2 = askopenfilename(parent=window,
                                filetypes=(("RAW파일", "*.raw"), ("모든파일", "*.*")))
    if filename2 == '' or filename2 == None:
        return
    inImage2 = []
    fsize2 = os.path.getsize(filename2)
    inH2 = inW2 = int(math.sqrt(fsize2))
    if inH2 != inH:
        return
    fp2 = open(filename2, 'rb')
    for i in range(inH2):
        tmpList = []
        for k in range(inW2):
            data = int(ord(fp2.read(1)))
            tmpList.append(data)
        inImage2.append(tmpList)
    fp2.close()

    outImage = [];
    tmpList = []
    for i in range(outH):
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)

    value = askinteger('합성비율', '두번째 영상의 가중치%-->', minvalue=1, maxvalue=99)
    w1 = 1 - (value / 100)
    w2 = 1 - w1
    for i in range(inH):
        for k in range(inW):
            data = int(inImage[i][k] * w1 + inImage2[i][k] * w2)
            if data > 255:
                data = 255
            elif data < 0:
                data = 0
            outImage[i][k] = data

    display()
##################################################################

#####################Menu2(화소영역처리 )############################################################
def embossing():  # 화소영역 - 엠보싱 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    outW = inW;outH = inH;outImage = []; tmpList = []
    for i in range(outH):
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    MSIZE = 3
    mask = [[-1, 0, 0], [0, 0, 0], [0, 0, 1]]
    tmpInImage = []
    for i in range(inH + 2):
        tmpList = []
        for k in range(inW + 2):
            tmpList.append(128)
        tmpInImage.append(tmpList)
    tmpOutImage = []
    for i in range(outH):
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        tmpOutImage.append(tmpList)

    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]

    for i in range(1, inH):
        for k in range(1, inW):

            S = 0.0
            for m in range(0, MSIZE):
                for n in range(0, MSIZE):
                    S += mask[m][n] * tmpInImage[i + (m - 1)][k + (n - 1)]
            tmpOutImage[i - 1][k - 1] = S

    for i in range(outW):
        for k in range(outH):
            tmpOutImage[i][k] += 127

    for i in range(outW):
        for k in range(outH):
            value = int(tmpOutImage[i][k])
            if value > 255:
                value = 255
            elif value < 0:
                value = 0
            outImage[i][k] = value

    display()

def blurr() :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    outW = inW;outH = inH;outImage = [];tmpList = []
    for i in range(outH):
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)

    mSize = 3
    mask = [[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]]

    tmpInImage = []
    for i in range(0, inW + 2):
        tmpList = []
        for k in range(0, inH + 2):
            tmpList.append(127)
        tmpInImage.append(tmpList)

    tmpOutImage = []
    for i in range(0, outW):
        tmpList = []
        for k in range(0, outH):
            tmpList.append(0)
        tmpOutImage.append(tmpList)

    for i in range(0, inW):
        for k in range(0, inH):
            tmpInImage[i + 1][k + 1] = inImage[i][k]

    for i in range(1, inW):
        for k in range(1, inH):

            s = 0.0
            for m in range(0, mSize):
                for n in range(0, mSize):
                    s += mask[m][n] * tmpInImage[i + m][k + n]
            tmpOutImage[i - 1][k - 1] = s


    for i in range(0, outW):
        for k in range(0, outH):
            if tmpOutImage[i][k] < 0:
                outImage[i][k] = 0
            elif tmpOutImage[i][k] > 255:
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])

    display()



def sharp() :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    outW = inW;outH = inH;outImage = [];tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)

    mSize = 3
    mask = [[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]
    mask = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]

    tmpInImage = []
    for i in range(0, inW + 2):
        tmpList = []
        for k in range(0, inH + 2):
            tmpList.append(127)
        tmpInImage.append(tmpList)

    tmpOutImage = []
    for i in range(0, outW):
        tmpList = []
        for k in range(0, outH):
            tmpList.append(0)
        tmpOutImage.append(tmpList)

    for i in range(0, inW):
        for k in range(0, inH):
            tmpInImage[i + 1][k + 1] = inImage[i][k]

    for i in range(1, inW):
        for k in range(1, inH):
            s = 0.0
            for m in range(0, mSize):
                for n in range(0, mSize):
                    s += mask[m][n] * tmpInImage[i + m][k + n]
            tmpOutImage[i - 1][k - 1] = s

    for i in range(0, outW):
        for k in range(0, outH):
            if tmpOutImage[i][k] < 0:
                outImage[i][k] = 0
            elif tmpOutImage[i][k] > 255:
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])

    display()


def edge1() :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    # 중요! 출력메모리의 크기를 결정
    outW = inW;
    outH = inH;
    outImage = [];
    tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    mSize = 3
    mask = [[-1/9, -1/9, -1/9], [-1/9, 8/9, -1/9], [-1/9, -1/9, -1/9]]
    #####################
    # 임시 입력 영상 + 2
    tmpInImage = []
    for i in range(0, inW + 2):
        tmpList = []
        for k in range(0, inH + 2):
            tmpList.append(127)
        tmpInImage.append(tmpList)
    # 임시 출력 영상
    tmpOutImage = []
    for i in range(0, outW):
        tmpList = []
        for k in range(0, outH):
            tmpList.append(0)
        tmpOutImage.append(tmpList)
    # 입력 ==> 임시 입력
    for i in range(0, inW):
        for k in range(0, inH):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선 연산.
    for i in range(1, inW):
        for k in range(1, inH):
            # 1점에 대해서 3x3마스크 연산 --> 모두 곱해서 더하기.
            s = 0.0
            for m in range(0, mSize):
                for n in range(0, mSize):
                    s += mask[m][n] * tmpInImage[i + m][k + n]
            tmpOutImage[i - 1][k - 1] = s

    # 결과값 처리 (0<, 255>, mask합계가 0이면 어두워)
    # for i in range(0, outW):
    #     for k in range(0, outH):
    #         tmpOutImage[i][k] += 127.0

    # 임시 출력 --> 출력
    for i in range(0, outW):
        for k in range(0, outH):
            if tmpOutImage[i][k] < 0:
                outImage[i][k] = 0
            elif tmpOutImage[i][k] > 255:
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])

    display()


def edge2() :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    outW = inW;outH = inH;outImage = [];
    tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)

    mSize = 3
    mask = [[0, 0, 0], [-1, 1, 0], [0, 0, 0]]

    tmpInImage = []
    for i in range(0, inW + 2):
        tmpList = []
        for k in range(0, inH + 2):
            tmpList.append(127)
        tmpInImage.append(tmpList)
    # 임시 출력 영상
    tmpOutImage = []
    for i in range(0, outW):
        tmpList = []
        for k in range(0, outH):
            tmpList.append(0)
        tmpOutImage.append(tmpList)
    # 입력 ==> 임시 입력
    for i in range(0, inW):
        for k in range(0, inH):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선 연산.
    for i in range(1, inW):
        for k in range(1, inH):

            s = 0.0
            for m in range(0, mSize):
                for n in range(0, mSize):
                    s += mask[m][n] * tmpInImage[i + m][k + n]
            tmpOutImage[i - 1][k - 1] = s

    for i in range(0, outW):
        for k in range(0, outH):
            if tmpOutImage[i][k] < 0:
                outImage[i][k] = 0
            elif tmpOutImage[i][k] > 255:
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])

    display()


def edge3() :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    # 중요! 출력메모리의 크기를 결정
    outW = inW; outH = inH;outImage = [];tmpList = []
    for i in range(outH):
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)

    mSize = 3
    mask = [[0, -1, 0], [0, 1, 0], [0, 0, 0]]

    tmpInImage = []
    for i in range(0, inW + 2):
        tmpList = []
        for k in range(0, inH + 2):
            tmpList.append(127)
        tmpInImage.append(tmpList)

    tmpOutImage = []
    for i in range(0, outW):
        tmpList = []
        for k in range(0, outH):
            tmpList.append(0)
        tmpOutImage.append(tmpList)

    for i in range(0, inW):
        for k in range(0, inH):
            tmpInImage[i + 1][k + 1] = inImage[i][k]

    for i in range(1, inW):
        for k in range(1, inH):

            s = 0.0
            for m in range(0, mSize):
                for n in range(0, mSize):
                    s += mask[m][n] * tmpInImage[i + m][k + n]
            tmpOutImage[i - 1][k - 1] = s


    for i in range(0, outW):
        for k in range(0, outH):
            if tmpOutImage[i][k] < 0:
                outImage[i][k] = 0
            elif tmpOutImage[i][k] > 255:
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])

    display()
######################Menu3 기하학처리##############################

def upDown():  # 상하 반전 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    outW = inW;outH = inH;outImage = [];tmpList = []
    for i in range(outH):
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)

    for i in range(inH):
        for k in range(inW):
            outImage[outW - 1 - i][k] = inImage[i][k]

    display()

def leftRight() :  #좌우  반전 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    outW = inW;  outH = inH;
    for i in range(outH):
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    for  i  in  range(inH) :
        for  k  in  range(inW) :
            outImage[i][outW-1-k] = inImage[i][k]
    display()

def panImage():
    global panYN
    panYN = True


def mouseClick(event):
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global sx, sy, ex, ey, panYN
    if not panYN:
        return
    sx = event.x;
    sy = event.y;


def mouseDrop(event):
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global sx, sy, ex, ey, panYN
    if not panYN:
        return
    ex = event.x;
    ey = event.y;
    my = sx - ex;
    mx = sy - ey

    outW = inW;
    outH = inH;
    outImage = [];
    tmpList = []
    for i in range(outH):
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    for i in range(inH):
        for k in range(inW):
            if 0 <= i - mx < outH and 0 <= k - my < outW:
                outImage[i - mx][k - my] = inImage[i][k]
    panYN = False
    display()


def zoomOut():  # 축소하기 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    scale = askinteger('축소하기', '축소할 배수-->', minvalue=2, maxvalue=32)
    outW = int(inW / scale);outH = int(inH / scale); outImage = [];tmpList = []
    for i in range(outH):
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)

    for i in range(inH):
        for k in range(inW):
            outImage[int(i / scale)][int(k / scale)] = inImage[i][k]
    display()

def zoomIn() :  # 확대하기 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    scale = askinteger('확대하기', '확대할 배수-->', minvalue=2, maxvalue=32)
    outW = int(inW*scale);  outH = int(inH*scale);
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)

    for  i  in  range(inH) :
        for  k  in  range(inW) :
             outImage[int(i*scale)][int(k*scale)] = inImage[i][k]

    display()

def rotate1():
    global inImage, outImage, inH, inW, outH, outW, window, canvas, paper, filename
    degree = askinteger('각도', '값 입력', minvalue=0, maxvalue=360)
    # 출력 파일의 크기 결정.
    outW = inW;
    outH = inH
    # 출력 영상 메모리 확보
    outImage = []
    for i in range(0, inW):
        tmpList = []
        for k in range(0, inH):
            tmpList.append(0)
        outImage.append(tmpList)
    ### 진짜 영상 처리 알고리즘 ###
    radian = degree * 3.141592 / 180.0
    for i in range(0, inW):
        for k in range(0, inH):
            xs = i;
            ys = k
            xd = int(math.cos(radian) * xs - math.sin(radian) * ys)
            yd = int(math.sin(radian) * xs + math.cos(radian) * ys)
            if 0 <= xd < outW and 0 <= yd < outH:
                outImage[xd][yd] = inImage[xs][ys]
    ###############################
    display()


def rotate2():
    global inImage, outImage, inH, inW, outH, outW, window, canvas, paper, filename
    degree = askinteger('각도', '값 입력', minvalue=0, maxvalue=360)
    # 출력 파일의 크기 결정.
    outW = inW;
    outH = inH
    # 출력 영상 메모리 확보
    outImage = []
    for i in range(0, inW):
        tmpList = []
        for k in range(0, inH):
            tmpList.append(0)
        outImage.append(tmpList)
    ### 진짜 영상 처리 알고리즘 ###
    radian = degree * 3.141592 / 180.0
    cx = int(inW / 2);
    cy = int(inH / 2)
    for i in range(0, outW):
        for k in range(0, outH):
            xs = i;
            ys = k
            xd = int(math.cos(radian) * (xs - cx)
                     - math.sin(radian) * (ys - cy)) + cx
            yd = int(math.sin(radian) * (xs - cx)
                     + math.cos(radian) * (ys - cy)) + cy
            if 0 <= xd < outW and 0 <= yd < outH:
                outImage[xs][ys] = inImage[xd][yd]
            else:
                outImage[xs][ys] = 255
    display()


def rotate3():
    global inImage, outImage, inH, inW, outH, outW, window, canvas, paper, filename
    degree = askinteger('각도', '값 입력', minvalue=0, maxvalue=360)

    radian90 = (90 - degree) * 3.141592 / 180.0
    radian = degree * 3.141592 / 180.0

    outW = int(inH * math.cos(radian90) + inW * math.cos(radian))
    outH = int(inH * math.cos(radian) + inW * math.cos(radian90))

    outImage = []
    for i in range(0, outW):
        tmpList = []
        for k in range(0, outH):
            tmpList.append(0)
        outImage.append(tmpList)

    inImage2 = []
    for i in range(0, outW):
        tmpList = []
        for k in range(0, outH):
            tmpList.append(255)
        inImage2.append(tmpList)

    # inImage --> inImage2의 중앙으로
    gap = int((outW - inW) / 2)
    for i in range(0, inW):
        for k in range(0, inH):
            inImage2[i + gap][k + gap] = inImage[i][k]


    cx = int(outW / 2);
    cy = int(outH / 2)

    for i in range(0, outW):
        for k in range(0, outH):
            xs = i;
            ys = k
            xd = int(math.cos(radian) * (xs - cx)
                     - math.sin(radian) * (ys - cy)) + cx
            yd = int(math.sin(radian) * (xs - cx)
                     + math.cos(radian) * (ys - cy)) + cy

            if 0 <= xd < outW and 0 <= yd < outH:
                outImage[xs][ys] = inImage2[xd][yd]
            else:
                outImage[xs][ys] = 255
    ###############################
    display()



########################################


############MEnu(데이터분석)###########
def a_average():  # 입출력 영상의 평균값
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    rawSum = 0
    for i in range(inH):
        for k in range(inW):
            rawSum += inImage[i][k]
    inRawAvg = int(rawSum / (inH * inW))
    rawSum = 0
    for i in range(outH):
        for k in range(outW):
            rawSum += outImage[i][k]
    outRawAvg = int(rawSum / (outH * outW))
    subWindow = Toplevel(window)
    subWindow.geometry('200x100')
    label1 = Label(subWindow, text='입력영상 평균값 -->' + str(inRawAvg));
    label1.pack()
    label2 = Label(subWindow, text='출력영상 평균값 -->' + str(outRawAvg));
    label2.pack()
    subWindow.mainloop()


def a_histogram():  # 히스토 그램
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    countList = [0] * 256;
    normalList = [0] * 256

    for i in range(outH):
        for k in range(outW):
            value = outImage[i][k]
            countList[value] += 1

    # 정규화된값 =  (카운트값 - 최소값) * High  /  (최대값 - 최소값)
    maxVal = max(countList);
    minVal = min(countList)
    for i in range(len(countList)):
        normalList[i] = (countList[i] - minVal) * 256 / (maxVal - minVal)

    # 화면 출력
    subWindow = Toplevel(window)
    subWindow.geometry('256x256')
    subCanvas = Canvas(subWindow, width=256, height=256)
    subPaper = PhotoImage(width=256, height=256)
    subCanvas.create_image((256 / 2, 256 / 2), image=subPaper, state='normal')

    for i in range(0, 256):
        for k in range(0, int(normalList[i])):
            data = 0
            subPaper.put('#%02x%02x%02x' % (data, data, data), (i, 255 - k))

    subCanvas.pack(expand=1, anchor=CENTER)
    subWindow.mainloop()


def a_histogram2():  # 히스토 그램
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    countList = [0] * 256

    for i in range(outH):
        for k in range(outW):
            value = outImage[i][k]
            countList[value] += 1

    plt.plot(countList)
    plt.show()


def a_histoStretch():  # 히스토그램 스트래칭 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW;
    outH = inH;
    outImage = [];
    tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)

    maxVal, minVal, HIGH = 0, 255, 255
    for i in range(inH):
        for k in range(inW):
            data = inImage[i][k]
            if data > maxVal:
                maxVal = data
            if data < minVal:
                minVal = data
    # 히스토그램 스트래칭
    # OUT =  (IN - 최소값) * HIGH / (최대값 - 최소값)
    for i in range(inH):
        for k in range(inW):
            value = int((inImage[i][k] - minVal) * HIGH / (maxVal - minVal))
            if value < 0:
                value = 0
            elif value > 255:
                value = 255
            outImage[i][k] = value

    display()


def a_endInSearch():  # 엔드-인 탐색 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW;
    outH = inH;
    outImage = [];
    tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)

    maxVal, minVal, HIGH = 0, 255, 255
    for i in range(inH):
        for k in range(inW):
            data = inImage[i][k]
            if data > maxVal:
                maxVal = data
            if data < minVal:
                minVal = data
    limit = askinteger('엔드인', '상하 범위:', minvalue=1, maxvalue=127)
    maxVal -= limit
    minVal += limit
    # 히스토그램 스트래칭
    # OUT =  (IN - 최소값) * HIGH / (최대값 - 최소값)
    for i in range(inH):
        for k in range(inW):
            value = int((inImage[i][k] - minVal) * HIGH / (maxVal - minVal))
            if value < 0:
                value = 0
            elif value > 255:
                value = 255
            outImage[i][k] = value

    display()


def a_histoEqual():  # 히스토그램 평활화 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW;
    outH = inH;
    outImage = [];
    tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)

    histo = [0] * 255;
    sumHisto = [0] * 255;
    normalHisto = [0] * 255
    HIGH = 255
    # 히스토그램 작성
    for i in range(inH):
        for k in range(inW):
            value = inImage[i][k]
            histo[value] += 1
    # 누적 히스토그램 작성
    sVal = 0
    for i in range(len(histo)):
        sVal += histo[i]
        sumHisto[i] = sVal
    # 정규화된 누적 히스토그램 :  (누적합 / (행개수*열개수)) * HIGH
    for i in range(len(sumHisto)):
        normalHisto[i] = int(sumHisto[i] / (outW * outH) * HIGH)

    # 정규화된 값으로 출력하기
    for i in range(inH):
        for k in range(inW):
            index = inImage[i][k]
            outImage[i][k] = normalHisto[index]
    display()


########################################
##########menu(4)
def drawSheet(cList) :
    global cellList, input_file
    print(cellList)
    if cellList == None or cellList == [] :
        pass
    else :
        for row in cellList:
            for col in row:
                col.destroy()

    rowNum = len(cList)
    colNum = len(cList[0])
    cellList = []

    for i in range(0, rowNum):
        tmpList = []
        for k in range(0, colNum):
            ent = Entry(window, text='')
            tmpList.append(ent)
            ent.grid(row=i, column=k)
        cellList.append(tmpList)

    for i in range(0, rowNum):
        for k in range(0, colNum):
            cellList[i][k].insert(0, cList[i][k])

def saveCSV():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    output_file = asksaveasfile(parent=window, mode='w',
                                defaultextension="*.csv", filetypes=(("CSV파일", "*.csv"), ("모든파일", "*.*")))
    output_file = output_file.name

    header = ['Column', 'Row', 'Value']
    with open(output_file, 'w', newline='') as filewriter:
        csvWriter = csv.writer(filewriter)
        csvWriter.writerow(header)
        for row in range(outW):
            for col in range(outH):
                data = outImage[row][col]
                row_list = [row, col, data]
                csvWriter.writerow(row_list)

    print('OK!')


def saveShuffleCSV():
    pass


def loadCSV(fname):
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    fsize = -1
    fp = open(fname, 'r')
    for f in fp:
        fsize += 1
    fp.close()
    inH = inW = int(math.sqrt(fsize))
    inImage = [];
    tmpList = []
    for i in range(inH):
        tmpList = []
        for k in range(inW):
            tmpList.append(0)
        inImage.append(tmpList)

    fp = open(fname, 'r')
    csvFP = csv.reader(fp)
    next(csvFP)
    for row_list in csvFP:
        row = int(row_list[0])
        col = int(row_list[1])
        value = int(row_list[2])
        inImage[row][col] = value
    fp.close()


def openCSV():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    filename = askopenfilename(parent=window,
                               filetypes=(("CSV파일", "*.csv"), ("모든파일", "*.*")))
    loadCSV(filename)
    equal()



def saveSQLite():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global csvList, input_file
    con = sqlite3.connect('imageDB')
    cur = con.cursor()
    colList = []
    fname = os.path.basename(filename).split(".")[0]
    try:
        sql = "CREATE TABLE imageTable( filename CHAR(20), resolution smallint" + \
              ", row  smallint,  col  smallint, value  smallint)"
        cur.execute(sql)
    except:
        pass

    for i in range(inW):
        for k in range(inH):
            sql = "INSERT INTO imageTable VALUES('" + fname + "'," + str(inW) + \
                  "," + str(i) + "," + str(k) + "," + str(inImage[i][k]) + ")"
            cur.execute(sql)

    con.commit()

    cur.close()
    con.close()
    print('Ok!')

def openSQLite():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH,inImage,outImage
    global csvList, input_file
    con = sqlite3.connect('imageDB')
    cur = con.cursor()
    try:
        sql = "SELECT DISTINCT filename, resolution FROM imageTable"
        cur.execute(sql)
        tableNameList = []
        while True:
            row = cur.fetchone()
            if row == None:
                break
            tableNameList.append(row[0] + ':' + str(row[1]))

        ######## 내부 함수 (Inner Function) : 함수 안의 함수,지역함수 #######
        def selectTable():
            global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
            selectedIndex = listbox.curselection()[0]
            subWindow.destroy()
            fname, res = tableNameList[selectedIndex].split(':')
            filename = fname
            sql = "SELECT row, col, value FROM imageTable WHERE filename='" + \
                  fname + "' AND resolution=" + res
            print(sql)
            cur.execute(sql)

            inH = inW = int(res)
            inImage = []
            tmpList = []
            for i in range(inH):  # 입력메모리 확보(0으로 초기화)
                tmpList = []
                for k in range(inW):
                    tmpList.append(0)
                inImage.append(tmpList)

            while True:
                row_tuple = cur.fetchone()
                if row_tuple == None:
                    break
                row, col, value = row_tuple
                inImage[row][col] = value


            cur.close()
            con.close()
            equal()
            print("Ok! openSQLite")

        ################################################################

        subWindow = Toplevel(window)
        listbox = Listbox(subWindow)
        button = Button(subWindow, text='선택', command=selectTable)
        listbox.pack();
        button.pack()
        for sName in tableNameList:
            listbox.insert(END, sName)
        subWindow.lift()

    except:
        cur.close()
        con.close()
        print("Error! openSQLite")



def saveMySQL():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global csvList, input_file
    con = pymysql.connect(host='192.168.174.129', user='root',
                          password='1234', db='imageDB', charset='utf8')  # 데이터베이스 지정(또는 연결)
    cur = con.cursor()  # 연결 통로 생성 (쿼리문을 날릴 통로)
    # 열이름 리스트 만들기
    colList = []
    fname = os.path.basename(filename).split(".")[0]
    try:
        sql = "CREATE TABLE imageTable( filename CHAR(20), resolution smallint" + \
              ", row  smallint,  col  smallint, value  smallint)"
        cur.execute(sql)
    except:
        pass

    try:
        sql = "DELETE FROM imageTable WHERE filename='" + \
              fname + "' AND resolution=" + str(outW)
        cur.execute(sql)
        con.commit()
    except:
        pass

    for i in range(inW):
        for k in range(inH):
            sql = "INSERT INTO imageTable VALUES('" + fname + "'," + str(outW) + \
                  "," + str(i) + "," + str(k) + "," + str(outImage[i][k]) + ")"
            cur.execute(sql)

    con.commit()

    cur.close()
    con.close()  # 데이터베이스 연결 종료
    print('Ok! saveMySQL')


def openMySQL():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global csvList, input_file
    con = pymysql.connect(host='192.168.174.129', user='root',
                          password='1234', db='imageDB', charset='utf8')  # 데이터베이스 지정(또는 연결)
    cur = con.cursor()  # 연결 통로 생성 (쿼리문을 날릴 통로)
    try:
        sql = "SELECT DISTINCT filename, resolution FROM imageTable"
        cur.execute(sql)
        tableNameList = []  # ['강아지:128', '강아지:512' ....]
        while True:
            row = cur.fetchone()
            if row == None:
                break
            tableNameList.append(row[0] + ':' + str(row[1]))

        ######## 내부 함수 (Inner Function) : 함수 안의 함수,지역함수 #######
        def selectTable():
            global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
            selectedIndex = listbox.curselection()[0]
            subWindow.destroy()
            fname, res = tableNameList[selectedIndex].split(':')
            filename = fname
            sql = "SELECT row, col, value FROM imageTable WHERE filename='" + \
                  fname + "' AND resolution=" + res
            print(sql)
            cur.execute(sql)

            inH = inW = int(res)
            inImage = [];
            tmpList = []
            for i in range(inH):  # 입력메모리 확보(0으로 초기화)
                tmpList = []
                for k in range(inW):
                    tmpList.append(0)
                inImage.append(tmpList)
            while True:
                row_tuple = cur.fetchone()
                if row_tuple == None:
                    break
                row, col, value = row_tuple
                inImage[row][col] = value

            cur.close()
            con.close()
            equal()
            print("Ok! openMySQL")

        ################################################################

        subWindow = Toplevel(window)
        listbox = Listbox(subWindow)
        button = Button(subWindow, text='선택', command=selectTable)
        listbox.pack();
        button.pack()
        for sName in tableNameList:
            listbox.insert(END, sName)
        subWindow.lift()



    except:
        cur.close()
        con.close()
        print("Error! openMySQL")




## Excel
def saveExcel1():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    output_file = asksaveasfile(parent=window, mode='w',
                                defaultextension="*.xls", filetypes=(("XLS파일", "*.xls"), ("모든파일", "*.*")))
    output_file = output_file.name

    sheetName = os.path.basename(output_file).split(".")[0]
    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheetName)

    for rowNum in range(outH):
        for colNum in range(outW):
            data = outImage[rowNum][colNum]
            ws.write(rowNum, colNum, data)

    wb.save(output_file)
    print('OK! saveExcel1')



def saveExcel2():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    output_file = asksaveasfile(parent=window, mode='w',
                                defaultextension="*.xlsx", filetypes=(("XLSX파일", "*.xls"), ("모든파일", "*.*")))
    output_file = output_file.name

    sheetName = os.path.basename(output_file).split(".")[0]
    wb = xlsxwriter.Workbook(output_file)
    ws = wb.add_worksheet(sheetName)

    ws.set_column(0, outW, 1.0)  # 약 0.34 쯤
    for r in range(outH):
        ws.set_row(r, 9.5)  # 약 0.35 쯤
    for rowNum in range(outW):
        for colNum in range(outH):
            data = outImage[rowNum][colNum]
            # data 값으로 셀의 배경색을 조절 #000000~#FFFFFF
            if data > 15:
                hexStr = '#' + (hex(data)[2:]) * 3
            else:
                hexStr = '#' + ('0' + hex(data)[2:]) * 3

            # 셀의 포맷을 준비
            cell_format = wb.add_format()
            cell_format.set_bg_color(hexStr)

            ws.write(rowNum, colNum, '', cell_format)

    wb.close()
    print('OK! saveExcel2')

def  excelData() :
    global csvList, input_file
    csvList = []
    input_file = askopenfilename(parent=window,
      filetypes=(("엑셀파일", "*.xls;*.xlsx"), ("모든파일", "*.*")))
    workbook = xlrd.open_workbook(input_file)
    sheetCount = workbook.nsheets  # 속성
    for worksheet in workbook.sheets():
        sheetName = worksheet.name
        sRow = worksheet.nrows
        sCol = worksheet.ncols
        print(sheetName, sRow, sCol)


def  exDataone() :
    global csvList, input_file
    csvList = []
    input_file = askopenfilename(parent=window,
      filetypes=(("엑셀파일", "*.xls;*.xlsx"), ("모든파일", "*.*")))
    workbook = xlrd.open_workbook(input_file)
    sheetCount = workbook.nsheets  # 속성
    sheet1 = workbook.sheets()[0]
    sheetName = sheet1.name
    sRow = sheet1.nrows
    sCol = sheet1.ncols
    #print(sheetName, sRow, sCol)
    # Worksheet --> csvList
    for i  in range(sRow) :
        tmpList = []
        for k in range(sCol) :
            value = sheet1.cell_value(i,k)
            tmpList.append(value)
        csvList.append(tmpList)

    drawSheet(csvList)

def  exDataAll() :
    global csvList, input_file
    csvList = []
    input_file = askopenfilename(parent=window,
      filetypes=(("엑셀파일", "*.xls;*.xlsx"), ("모든파일", "*.*")))
    workbook = xlrd.open_workbook(input_file)
    sheetCount = workbook.nsheets  # 속성
    for worksheet in workbook.sheets():
        sRow = worksheet.nrows
        sCol = worksheet.ncols
        # Worksheet --> csvList
        for i  in range(sRow) :
            tmpList = []
            for k in range(sCol) :
                value = worksheet.cell_value(i,k)
                tmpList.append(value)
            csvList.append(tmpList)

    drawSheet(csvList)

def exDataSelect() :
    global csvList, input_file
    csvList = []
    input_file = askopenfilename(parent=window,
      filetypes=(("엑셀파일", "*.xls;*.xlsx"), ("모든파일", "*.*")))
    workbook = xlrd.open_workbook(input_file)
    sheetNameList = []
    for worksheet in workbook.sheets():
        sheetNameList.append(worksheet.name)

    ##################################
    def selectSheet() :
        selectedIndex = listbox.curselection()[0]
        subWindow.destroy()
        sheet1 = workbook.sheets()[selectedIndex]
        sRow = sheet1.nrows
        sCol = sheet1.ncols
        for i in range(sRow):
            tmpList = []
            for k in range(sCol):
                value = sheet1.cell_value(i, k)
                tmpList.append(value)
            csvList.append(tmpList)
        drawSheet(csvList)

    subWindow = Toplevel(window)  # window의 하위로 지정
    listbox = Listbox(subWindow)
    button = Button(subWindow, text='선택', command=selectSheet)
    listbox.pack(); button.pack()
    for  sName in sheetNameList :
        listbox.insert(END, sName)
    subWindow.lift()






## 전역 변수부
window, canvas, paper, filename = [None] * 4
inImage, outImage = [], [];
inW, inH, outW, outH = [0] * 4
panYN = False;
sx, sy, ex, ey = [0] * 4
VIEW_X, VIEW_Y = 128, 128
status = None

## 메인 코드부
window = Tk();
window.geometry('400x400');
window.title('영상 처리&데이터 분석 Ver 1.0 (Beta 2)')
window.bind("<Button-1>", mouseClick)
window.bind("<ButtonRelease-1>", mouseDrop)

status = Label(window, text='이미지 정보:', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

mainMenu = Menu(window);
window.config(menu=mainMenu)
fileMenu = Menu(mainMenu);
mainMenu.add_cascade(label='파일', menu=fileMenu)
fileMenu.add_command(label='열기', command=openFile)
fileMenu.add_command(label='저장', command=saveFile)
fileMenu.add_separator()
fileMenu.add_command(label='종료', command=exitFile)

pixelMenu = Menu(mainMenu);
mainMenu.add_cascade(label='화소점처리', menu=pixelMenu)
pixelMenu.add_command(label='동일영상', command=equal)
pixelMenu.add_command(label='밝게하기', command=addImage)
pixelMenu.add_command(label='밝게곱하기',command=multiplyImage)
pixelMenu.add_command(label='어둡게빼기',command= decreaseImage)
pixelMenu.add_command(label='어둡게나누기',command=multiplyImage)
pixelMenu.add_separator()
pixelMenu.add_command(label='영상합성', command=morphing)

areaMenu = Menu(mainMenu);
mainMenu.add_cascade(label='화소영역처리', menu=areaMenu)
areaMenu.add_command(label='엠보싱', command=embossing)
areaMenu.add_command(label='블러링', command=blurr)
areaMenu.add_command(label='샤프닝', command=sharp)
areaMenu.add_command(label='경계선추출(고주파)', command=edge1)
areaMenu.add_command(label='경계선추출(수직에지)', command=edge2)
areaMenu.add_command(label='경계선추출(수평에지)', command=edge3)

geoMenu = Menu(mainMenu);
mainMenu.add_cascade(label='기하학 처리', menu=geoMenu)
geoMenu.add_command(label='상하반전', command=upDown)
geoMenu.add_command(label='화면이동', command=panImage)
geoMenu.add_command(label='화면축소', command=zoomOut)
geoMenu.add_command(label='좌우반전',command=leftRight)
geoMenu.add_command(label='확대하기',command=zoomIn)
geoMenu.add_separator()
geoMenu.add_command(label='영상회전(포워딩)', command=rotate1)
geoMenu.add_command(label='영상회전(백워딩 및 중앙)', command=rotate2)
geoMenu.add_command(label='영상회전(확대)', command=rotate3)


analyzeMenu = Menu(mainMenu);
mainMenu.add_cascade(label='데이터분석', menu=analyzeMenu)
analyzeMenu.add_command(label='평균값', command=a_average)
analyzeMenu.add_command(label='히스토그램', command=a_histogram)
analyzeMenu.add_command(label='히스토그램(matplotlib)', command=a_histogram2)
analyzeMenu.add_separator()
analyzeMenu.add_command(label='히스토그램 스트래칭', command=a_histoStretch)
analyzeMenu.add_command(label='엔드-인 탐색', command=a_endInSearch)
analyzeMenu.add_command(label='히스토그램 평활화', command=a_histoEqual)

CSVMenu = Menu(mainMenu);
mainMenu.add_cascade(label='CSV 처리', menu=CSVMenu)
CSVMenu.add_command(label='CSV로 내보내기', command=saveCSV)
CSVMenu.add_command(label='CSV(셔플)로 내보내기', command=saveShuffleCSV)
CSVMenu.add_command(label='CSV 불러오기', command=openCSV)

SQLiteMenu = Menu(mainMenu);
mainMenu.add_cascade(label='SQLite 처리', menu=SQLiteMenu)
SQLiteMenu.add_command(label='SQLite로 내보내기', command=saveSQLite)
SQLiteMenu.add_command(label='SQLite에서 가져오기', command=openSQLite)


MySQLMenu = Menu(mainMenu);
mainMenu.add_cascade(label='MYSQL 처리', menu=MySQLMenu)
MySQLMenu.add_command(label='MySQL로 내보내기', command=saveMySQL)
MySQLMenu.add_command(label='MySQL에서 가져오기', command=openMySQL)

ExcelMenu = Menu(mainMenu);
mainMenu.add_cascade(label='Excel 처리', menu=ExcelMenu)
ExcelMenu.add_command(label='Excel로 내보내기(숫자)', command=saveExcel1)
ExcelMenu.add_command(label='Excel로 내보내기(음영)', command=saveExcel2)
analyzeMenu.add_separator()
ExcelMenu.add_command(label='Excel정보 보기', command=excelData)
ExcelMenu.add_command(label='Excel내용 보기 - 1st', command=exDataone )
ExcelMenu.add_command(label='Excel내용 보기 - All', command=exDataAll)
ExcelMenu.add_command(label='Excel내용 보기 - Select', command=exDataSelect)
window.mainloop()