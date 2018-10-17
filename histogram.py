## 영상 처## 영상 처리 및 데이터 분석 툴
from tkinter import *; import os.path ;import math
from  tkinter.filedialog import *
from  tkinter.simpledialog import *
## 함수 선언부
def loadImage(fname) :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    fsize = os.path.getsize(fname) # 파일 크기 확인
    inH = inW = int(math.sqrt(fsize))  # 입력메모리 크기 결정! (중요)
    inImage = []; tmpList = []
    for i in range(inH) :  # 입력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(inW) :
            tmpList.append(0)
        inImage.append(tmpList)
    # 파일 --> 메모리로 데이터 로딩
    fp = open(fname, 'rb') # 파일 열기(바이너리 모드)
    for  i  in range(inH) :
        for  k  in  range(inW) :
            inImage[i][k] =  int(ord(fp.read(1)))
    fp.close()

def openFile() :
    global window, canvas, paper, filename,inImage, outImage,inW, inH, outW, outH
    filename = askopenfilename(parent=window,
                               filetypes=(("RAW파일", "*.raw"), ("모든파일", "*.*")))
    loadImage(filename) # 파일 --> 입력메모리
    equal() # 입력메모리--> 출력메모리

import threading
def display() :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 기존에 캐버스 있으면 뜯어내기.
    if  canvas != None :
        canvas.destroy()
    # 화면 준비 (고정됨)
    VIEW_X, VIEW_Y = 256, 256
    if VIEW_X >= outW or VIEW_Y >= outH : # 영상이 128미만이면
        VIEW_X = outW
        VIEW_Y = outH
        step = 1  # 건너뛸숫자
    else :
        step = int(outW / VIEW_X)

    window.geometry(str(VIEW_X*2) + 'x' + str(VIEW_Y*2))
    canvas = Canvas(window, width=VIEW_X, height=VIEW_Y)
    paper = PhotoImage(width=VIEW_X, height=VIEW_Y)
    canvas.create_image((VIEW_X/2, VIEW_X/2), image=paper, state='normal')
    # 화면에 출력
    def putPixel() :
        for i in range(0, outH,step) :
            for k in range(0, outW,step) :
                data = outImage[i][k]
                paper.put('#%02x%02x%02x' % (data, data, data),
                          ( int(k/step),int(i/step)))

    threading.Thread(target=putPixel).start()
    canvas.pack(expand=1, anchor =CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH) )


def equal() :  # 동일 영상 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW;  outH = inH;
    outImage = [];   tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    for  i  in  range(inH) :
        for  k  in  range(inW) :
            outImage[i][k] = inImage[i][k]

    display()


def addImage() :  # 밝게하기 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW;  outH = inH;
    outImage = [];   tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    value = askinteger('밝게하기', '밝게할 값-->', minvalue=1, maxvalue=255)
    for  i  in  range(inH) :
        for  k  in  range(inW) :
            if inImage[i][k] + value > 255 :
                outImage[i][k] = 255
            else :
                outImage[i][k] = inImage[i][k] + value
    display()

def a_average() :  # 입출력 영상의 평균값
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    rawSum = 0
    for  i  in  range(inH) :
        for  k  in  range(inW) :
            rawSum += inImage[i][k]
    inRawAvg = int(rawSum / (inH*inW))

    rawSum = 0
    for  i  in  range(outH) :
        for  k  in  range(outW) :
            rawSum += outImage[i][k]
    outRawAvg = int(rawSum / (outH*outW))

    subWindow = Toplevel(window) # 부모(window)에 종속된 서브윈도
    subWindow.geometry('200x100')
    label1 = Label(subWindow, text='입력영상 평균값 -->' + str(inRawAvg) ); label1.pack()
    label2 = Label(subWindow, text='출력영상 평균값 -->' + str(outRawAvg)); label2.pack()
    subWindow.mainloop()

def a_histogram() :  # 히스토 그램
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    countList = [0] * 256;  normalList = [0] * 256

    for i in range(outH) :
        for k in range(outW) :
            value = outImage[i][k]
            countList[value] += 1

    # 정규화된값 =  (카운트값 - 최소값) * High  /  (최대값 - 최소값)
    maxVal  = max (countList);  minVal = min(countList)
    for i in range(len(countList)) :
        normalList[i] = (countList[i] - minVal) * 256 / (maxVal - minVal)

    # 화면 출력
    subWindow = Toplevel(window)
    subWindow.geometry('256x256')
    subCanvas = Canvas(subWindow, width=256, height=256)
    subPaper = PhotoImage(width=256, height=256)
    subCanvas.create_image((256/2,256/2), image=subPaper, state='normal')

    for i in range(0, 256) :
        for k in range(0, int(normalList[i])) :
            data = 0
            subPaper.put('#%02x%02x%02x' % (data, data, data), (i, 255-k))

    subCanvas.pack(expand=1, anchor=CENTER)
    subWindow.mainloop()

import matplotlib.pyplot as plt
def a_histogram2() :  # 히스토 그램
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    countList = [0] * 256

    for i in range(outH) :
        for k in range(outW) :
            value = outImage[i][k]
            countList[value] += 1

    plt.plot(countList)
    plt.show()


def upDown() :  # 상하 반전 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW;  outH = inH;
    outImage = [];   tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    for  i  in  range(inH) :
        for  k  in  range(inW) :
            outImage[outW-1-i][k] = inImage[i][k]

    display()

def panImage() :
    global  panYN
    panYN = True

def mouseClick(event) :  # 동일 영상 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global sx, sy, ex, ey, panYN
    if not panYN :
        return
    sx = event.x;  sy = event.y;

def mouseDrop(event):  # 동일 영상 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global sx, sy, ex, ey, panYN
    if not panYN:
        return
    ex = event.x; ey = event.y;
    my = sx - ex ; mx = sy - ey

    # 중요! 출력메모리의 크기를 결정
    outW = inW;  outH = inH;
    outImage = [];   tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    for  i  in  range(inH) :
        for  k  in  range(inW) :
            if 0<= i-mx <outH and 0<= k-my < outW :
                outImage[i-mx][k-my] = inImage[i][k]
    panYN = False
    display()


def zoomOut() :  # 축소하기 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    scale = askinteger('축소하기', '축소할 배수-->', minvalue=2, maxvalue=32)
    outW = int(inW/scale);  outH = int(inH/scale);
    outImage = [];   tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    for  i  in  range(inH) :
        for  k  in  range(inW) :
             outImage[int(i/scale)][int(k/scale)] = inImage[i][k]
    display()

import struct
def saveFile() :
    global window, canvas, paper, filename,inImage, outImage,inW, inH, outW, outH
    saveFp = asksaveasfile(parent=window, mode='wb',
                               defaultextension="*.raw", filetypes=(("RAW파일", "*.raw"), ("모든파일", "*.*")))
    for i in range(outW):
        for k in range(outH):
            saveFp.write( struct.pack('B',outImage[i][k]))

    saveFp.close()

def exitFile() :
    global window, canvas, paper, filename,inImage, outImage,inW, inH, outW, outH
    pass

import csv
def saveCSV() :
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

def saveShuffleCSV() :
    pass

def loadCSV(fname) :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    fsize = -1
    fp = open(fname, 'r')
    for  f  in fp :
        fsize += 1
    fp.close()
    inH = inW = int(math.sqrt(fsize))  # 입력메모리 크기 결정! (중요)
    inImage = []; tmpList = []
    for i in range(inH) :  # 입력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(inW) :
            tmpList.append(0)
        inImage.append(tmpList)
    # 파일 --> 메모리로 데이터 로딩
    fp = open(fname, 'r') # 파일 열기(바이너리 모드)
    csvFP = csv.reader(fp)
    next(csvFP)
    for row_list in csvFP :
        row= int(row_list[0]) ; col = int(row_list[1]) ; value=int(row_list[2])
        inImage[row][col] = value
    fp.close()

def openCSV() :
    global window, canvas, paper, filename,inImage, outImage,inW, inH, outW, outH
    filename = askopenfilename(parent=window,
                               filetypes=(("CSV파일", "*.csv"), ("모든파일", "*.*")))
    loadCSV(filename) # 파일 --> 입력메모리
    equal() # 입력메모리--> 출력메모리

import sqlite3
def saveSQLite() :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global csvList, input_file
    con = sqlite3.connect('imageDB')  # 데이터베이스 지정(또는 연결)
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

    for i in range(inW) :
        for k in range(inH) :
            sql = "INSERT INTO imageTable VALUES('" + fname + "'," + str(inW) + \
                "," + str(i) + "," + str(k) + "," + str(inImage[i][k]) +")"
            cur.execute(sql)

    con.commit()

    cur.close()
    con.close()  # 데이터베이스 연결 종료
    print('Ok!')

def openSQLite() :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global csvList, input_file
    con = sqlite3.connect('imageDB')  # 데이터베이스 지정(또는 연결)
    cur = con.cursor()  # 연결 통로 생성 (쿼리문을 날릴 통로)
    try :
        sql = "SELECT DISTINCT filename, resolution FROM imageTable"
        cur.execute(sql)
        tableNameList = [] # ['강아지:128', '강아지:512' ....]
        while True :
            row = cur.fetchone()
            if row == None :
                break
            tableNameList.append( row[0] + ':' + str(row[1]) )

        ######## 내부 함수 (Inner Function) : 함수 안의 함수,지역함수 #######
        def selectTable() :
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
            inImage = [];  tmpList = []
            for i in range(inH):  # 입력메모리 확보(0으로 초기화)
                tmpList = []
                for k in range(inW):
                    tmpList.append(0)
                inImage.append(tmpList)
            while True :
                row_tuple = cur.fetchone()
                if row_tuple == None :
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
        listbox.pack(); button.pack()
        for sName in tableNameList :
            listbox.insert(END, sName)
        subWindow.lift()



    except :
        cur.close()
        con.close()
        print("Error! openSQLite")

import pymysql
def saveMySQL() :
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

    for i in range(inW) :
        for k in range(inH) :
            sql = "INSERT INTO imageTable VALUES('" + fname + "'," + str(outW) + \
                "," + str(i) + "," + str(k) + "," + str(outImage[i][k]) +")"
            cur.execute(sql)

    con.commit()

    cur.close()
    con.close()  # 데이터베이스 연결 종료
    print('Ok! saveMySQL')

def openMySQL() :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global csvList, input_file
    con = pymysql.connect(host='192.168.174.129', user='root',
                          password='1234', db='imageDB', charset='utf8')  # 데이터베이스 지정(또는 연결)
    cur = con.cursor()  # 연결 통로 생성 (쿼리문을 날릴 통로)
    try :
        sql = "SELECT DISTINCT filename, resolution FROM imageTable"
        cur.execute(sql)
        tableNameList = [] # ['강아지:128', '강아지:512' ....]
        while True :
            row = cur.fetchone()
            if row == None :
                break
            tableNameList.append( row[0] + ':' + str(row[1]) )

        ######## 내부 함수 (Inner Function) : 함수 안의 함수,지역함수 #######
        def selectTable() :
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
            inImage = [];  tmpList = []
            for i in range(inH):  # 입력메모리 확보(0으로 초기화)
                tmpList = []
                for k in range(inW):
                    tmpList.append(0)
                inImage.append(tmpList)
            while True :
                row_tuple = cur.fetchone()
                if row_tuple == None :
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
        listbox.pack(); button.pack()
        for sName in tableNameList :
            listbox.insert(END, sName)
        subWindow.lift()



    except :
        cur.close()
        con.close()
        print("Error! openMySQL")

import xlwt
def saveExcel1() :
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

import xlsxwriter
def saveExcel2() :
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
    for  rowNum in range(outW) :
        for colNum in range(outH) :
            data = outImage[rowNum][colNum]
            # data 값으로 셀의 배경색을 조절 #000000~#FFFFFF
            if data > 15 :
                hexStr = '#' + (hex(data)[2:])*3
            else :
                hexStr = '#' + ('0' + hex(data)[2:]) * 3

            # 셀의 포맷을 준비
            cell_format = wb.add_format()
            cell_format.set_bg_color(hexStr)

            ws.write(rowNum, colNum, '', cell_format)

    wb.close()
    print('OK! saveExcel2')

def a_histoStretch() :  # 히스토그램 스트래칭 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW;  outH = inH;
    outImage = [];   tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    maxVal, minVal, HIGH = 0, 255, 255
    for  i  in  range(inH) :
        for  k  in  range(inW) :
            data = inImage[i][k]
            if  data > maxVal :
                maxVal = data
            if  data < minVal :
                minVal = data
    # 히스토그램 스트래칭
    # OUT =  (IN - 최소값) * HIGH / (최대값 - 최소값)
    for  i  in  range(inH) :
        for  k  in  range(inW) :
            value = int( (inImage[i][k] - minVal) * HIGH / ( maxVal - minVal) )
            if value < 0 :
                value = 0
            elif value > 255 :
                value = 255
            outImage[i][k] = value

    display()


def a_endInSearch() :  # 엔드-인 탐색 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW;  outH = inH;
    outImage = [];   tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    maxVal, minVal, HIGH = 0, 255, 255
    for  i  in  range(inH) :
        for  k  in  range(inW) :
            data = inImage[i][k]
            if  data > maxVal :
                maxVal = data
            if  data < minVal :
                minVal = data
    limit = askinteger('엔드인', '상하 범위:', minvalue=1, maxvalue=127)
    maxVal -= limit
    minVal += limit
    # 히스토그램 스트래칭
    # OUT =  (IN - 최소값) * HIGH / (최대값 - 최소값)
    for  i  in  range(inH) :
        for  k  in  range(inW) :
            value = int( (inImage[i][k] - minVal) * HIGH / ( maxVal - minVal) )
            if value < 0 :
                value = 0
            elif value > 255 :
                value = 255
            outImage[i][k] = value

    display()


def a_histoEqual() :  # 히스토그램 평활화 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW;  outH = inH;
    outImage = [];   tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    histo = [0] * 255;  sumHisto = [0] * 255; normalHisto=[0] * 255
    HIGH = 255
    # 히스토그램 작성
    for  i  in  range(inH) :
        for  k  in  range(inW) :
            value = inImage[i][k]
            histo[value] += 1
    # 누적 히스토그램 작성
    sVal = 0
    for  i  in  range(len(histo)) :
        sVal += histo[i]
        sumHisto[i] = sVal
    # 정규화된 누적 히스토그램 :  (누적합 / (행개수*열개수)) * HIGH
    for i in range(len(sumHisto)) :
        normalHisto[i] = int(sumHisto[i] / (outW * outH) * HIGH)

    # 정규화된 값으로 출력하기
    for  i  in  range(inH) :
        for  k  in  range(inW) :
            index = inImage[i][k]
            outImage[i][k] = normalHisto[index]
    display()


######
# 엠보싱할 때  : inputImage, inputImage2(tmpinputImage), outputImage,outputImage2(tmpoutputimage)
# 4개로 만드는데 이유는 인풋만 두개를 만들어서 바로 아웃풋에 넣는것 보다는 아웃풋 새로운것에 넣어서 처음 데이터와 마지막 데이터 손상을 줄인다.
def embossing() :  # 화소영역 - 엠보싱 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW;  outH = inH;
    outImage = [];   tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    MSIZE=3
    mask = [ [-1, 0, 0], [0, 0, 0], [0, 0, 1]  ]
    # 임시 입력 영상 = inImage보다 2열이 큰...
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
    # 원래입력 --> 임시입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i+1][k+1] = inImage[i][k]
            #tmp가 크기 때문에 +1 을 하나씩 더해 줘야 딱 맞게 들어감
            # 왜냐면 위와 아래 행으로 하나씩 증가하기 때문


    # 회선연산하기. 마스크로 쭉 긁으면서 계산하기...
    # 회선연산하기 마스크로 쭉 긁으면서 계산하기 픽셀크기만큼 돌려야됨.
    for i in range(1, inH):
        # 왜냐면 1,1 부터 시작을 해야되기 때문에 1을 지정해서 해줘야함 0부터 시작하면 추가된 (0,0)으로 가기때문
        #한 점에 대해서 (3*3)을 반복해서 처리 .  마스크 연산 들어감
        for k in range(1, inW):
            # 1점을 처리하되, 3x3 반복해서 처리: 마스크 연산 : 모두 곱해서더하기
            S = 0.0
            for  m in range(0,MSIZE) :
                for n in range(0,MSIZE) :
                    S += mask[m][n]*tmpInImage[i+(m-1)][k+(n-1)]
            tmpOutImage[i-1][k-1] = S
            #tmpimage는 하나씩 빼줘야됨. (0,0)으로 되어야 하니까. 그런데 뒤에는 계속 값이 바꿔야 되니까 i k 값들어감. 이 계산한걸 tmpoutput에 넣어줌
            #대신 아웃풋은 하나씩 빠지니까 -1 해줌.
    # 127 더해주기 (마스크의 합계가 0인 경우)
    #output의 합계가 0이기 때문에 어둡게 나옴 그러므로 좀 밝게 해줄려면 더해줘야함
    #127,128정도 더해주기(마스크의 합계가 0인 경우에만 해줌)
    tmpOutImage [i][k] +=127
    for i in range(outW):
        for k in range(outH):
            tmpOutImage[i][k] += 127

    # 임시 출력 --> 원래출력
    for i in range(outW) :
        for k in range(outH) :
            value = int(tmpOutImage[i][k])
            if value > 255 :
                value = 255
            elif value < 0 :
                value = 0
            outImage[i][k] = value

    display()

def blurr():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW; outH = inH; outImage = [];
    tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    MSIZE = 3
    mask = [[1./9., 1./9., 1./9.],[1./9., 1./9., 1./9.], [1./9., 1./9., 1./9.]]
    # 임시 입력 영상 = inImage보다 2열이 큰...
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
    # 원래입력 --> 임시입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선연산하기. 마스크로 쭉 긁으면서 계산하기...
    for i in range(1, inH):
        for k in range(1, inW):
            # 1점을 처리하되, 3x3 반복해서 처리: 마스크 연산 : 모두 곱해서더하기
            S = 0.0
            for m in range(0, MSIZE):
                for n in range(0, MSIZE):
                    S += mask[m][n] * tmpInImage[i + (m - 1)][k + (n - 1)]
            tmpOutImage[i - 1][k - 1] = S
    # # 127 더해주기 (마스크의 합계가 0인 경우)
    # for i in range(outW):
    #     for k in range(outH):
    #         tmpOutImage[i][k] += 127

    # 임시 출력 --> 원래출력
    for i in range(outW):
        for k in range(outH):
            value = int(tmpOutImage[i][k])
            if value > 255:
                value = 255
            elif value < 0:
                value = 0
            outImage[i][k] = value

    display()

def GaussianFilter():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW; outH = inH; outImage = [];
    tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    MSIZE = 3
    mask = [[1./16., 1./8., 1./16.],[1./8., 1./4., 1./8.], [1./16., 1./8., 1./16.]]
    # 임시 입력 영상 = inImage보다 2열이 큰...
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
    # 원래입력 --> 임시입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선연산하기. 마스크로 쭉 긁으면서 계산하기...
    for i in range(1, inH):
        for k in range(1, inW):
            # 1점을 처리하되, 3x3 반복해서 처리: 마스크 연산 : 모두 곱해서더하기
            S = 0.0
            for m in range(0, MSIZE):
                for n in range(0, MSIZE):
                    S += mask[m][n] * tmpInImage[i + (m - 1)][k + (n - 1)]
            tmpOutImage[i - 1][k - 1] = S
    # # 127 더해주기 (마스크의 합계가 0인 경우)
    # for i in range(outW):
    #     for k in range(outH):
    #         tmpOutImage[i][k] += 127

    # 임시 출력 --> 원래출력
    for i in range(outW):
        for k in range(outH):
            value = int(tmpOutImage[i][k])
            if value > 255:
                value = 255
            elif value < 0:
                value = 0
            outImage[i][k] = value

    display()

def Sharpening():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW; outH = inH; outImage = [];
    tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    MSIZE = 3
    mask = [[-1., -1., -1.],[-1, 9., -1.], [-1., -1., -1.]]
    # 임시 입력 영상 = inImage보다 2열이 큰...
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
    # 원래입력 --> 임시입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선연산하기. 마스크로 쭉 긁으면서 계산하기...
    for i in range(1, inH):
        for k in range(1, inW):
            # 1점을 처리하되, 3x3 반복해서 처리: 마스크 연산 : 모두 곱해서더하기
            S = 0.0
            for m in range(0, MSIZE):
                for n in range(0, MSIZE):
                    S += mask[m][n] * tmpInImage[i + (m - 1)][k + (n - 1)]
            tmpOutImage[i - 1][k - 1] = S
    # # 127 더해주기 (마스크의 합계가 0인 경우)
    # for i in range(outW):
    #     for k in range(outH):
    #         tmpOutImage[i][k] += 127

    # 임시 출력 --> 원래출력
    for i in range(outW):
        for k in range(outH):
            value = int(tmpOutImage[i][k])
            if value > 255:
                value = 255
            elif value < 0:
                value = 0
            outImage[i][k] = value

    display()

def HpSharp():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW; outH = inH; outImage = [];
    tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    MSIZE = 3
    mask = [[-1./9., -1./9., -1./9.],[-1./9., 8./9., -1./9.], [-1./9., -1./9., -1./9.]]
    # 임시 입력 영상 = inImage보다 2열이 큰...
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
    # 원래입력 --> 임시입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선연산하기. 마스크로 쭉 긁으면서 계산하기...
    for i in range(1, inH):
        for k in range(1, inW):
            # 1점을 처리하되, 3x3 반복해서 처리: 마스크 연산 : 모두 곱해서더하기
            S = 0.0
            for m in range(0, MSIZE):
                for n in range(0, MSIZE):
                    S += mask[m][n] * tmpInImage[i + (m - 1)][k + (n - 1)]
            tmpOutImage[i - 1][k - 1] = S
    # 127 더해주기 (마스크의 합계가 0인 경우)
    for i in range(outW):
        for k in range(outH):
            tmpOutImage[i][k] += 127

    # 임시 출력 --> 원래출력
    for i in range(outW):
        for k in range(outH):
            value = int(tmpOutImage[i][k])
            if value > 255:
                value = 255
            elif value < 0:
                value = 0
            outImage[i][k] = value

    display()


def LpfSharp():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW; outH = inH; outImage = [];
    tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    MSIZE = 3
    mask = [[1./9., 1./9., 1./9.],[1./9., 1./9., 1./9.], [1./9., 1./9., 1./9.]]
    # 임시 입력 영상 = inImage보다 2열이 큰...
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
    # 원래입력 --> 임시입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선연산하기. 마스크로 쭉 긁으면서 계산하기...
    for i in range(1, inH):
        for k in range(1, inW):
            # 1점을 처리하되, 3x3 반복해서 처리: 마스크 연산 : 모두 곱해서더하기
            S = 0.0
            for m in range(0, MSIZE):
                for n in range(0, MSIZE):
                    S += mask[m][n] * tmpInImage[i + (m - 1)][k + (n - 1)]
            tmpOutImage[i - 1][k - 1] = S
    # 127 더해주기 (마스크의 합계가 0인 경우)
    # for i in range(outW):
    #     for k in range(outH):
    #         tmpOutImage[i][k] += 127

    # 임시 출력 --> 원래출력
    for i in range(outW):
        for k in range(outH):
            value = int(tmpOutImage[i][k])
            if value > 255:
                value = 255
            elif value < 0:
                value = 0
            outImage[i][k] = value

    display()

## 전역 변수부
window, canvas, paper, filename = [None] * 4
inImage, outImage = [], []; inW, inH, outW, outH = [0] * 4
panYN = False;  sx, sy, ex, ey = [0] * 4
VIEW_X, VIEW_Y = 128, 128
status = None

## 메인 코드부
window = Tk();  window.geometry('400x400');
window.title('영상 처리&데이터 분석 Ver 1.0 (Beta 1)')
window.bind("<Button-1>", mouseClick)
window.bind("<ButtonRelease-1>", mouseDrop)

status = Label(window, text='이미지 정보:', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)


mainMenu = Menu(window);window.config(menu=mainMenu)
fileMenu = Menu(mainMenu);mainMenu.add_cascade(label='파일', menu=fileMenu)
fileMenu.add_command(label='열기', command=openFile)
fileMenu.add_command(label='저장', command=saveFile)
fileMenu.add_separator()
fileMenu.add_command(label='종료', command=exitFile)

pixelMenu = Menu(mainMenu);mainMenu.add_cascade(label='화소점처리', menu=pixelMenu)
pixelMenu.add_command(label='동일영상', command=equal)
pixelMenu.add_command(label='밝게하기', command=addImage)

areaMenu = Menu(mainMenu);mainMenu.add_cascade(label='화소영역처리', menu=areaMenu)
areaMenu.add_command(label='엠보싱', command=embossing)
areaMenu.add_command(label='블러링', command=blurr)
areaMenu.add_command(label='가우시안필터처리', command=GaussianFilter)
areaMenu.add_command(label='샤프닝', command=Sharpening)
areaMenu.add_command(label='고주파필터 샤프닝처리', command=HpSharp)
areaMenu.add_command(label='저주파필터 샤프닝처리', command=LpfSharp)


geoMenu = Menu(mainMenu);mainMenu.add_cascade(label='기하학 처리', menu=geoMenu)
geoMenu.add_command(label='상하반전', command=upDown)
geoMenu.add_command(label='화면이동', command=panImage)
geoMenu.add_command(label='화면축소', command=zoomOut)

analyzeMenu = Menu(mainMenu);mainMenu.add_cascade(label='데이터분석', menu=analyzeMenu)
analyzeMenu.add_command(label='평균값', command=a_average)
analyzeMenu.add_command(label='히스토그램', command=a_histogram)
analyzeMenu.add_command(label='히스토그램(matplotlib)', command=a_histogram2)
analyzeMenu.add_separator()
analyzeMenu.add_command(label='히스토그램 스트래칭', command=a_histoStretch)
analyzeMenu.add_command(label='엔드-인 탐색', command=a_endInSearch)
analyzeMenu.add_command(label='히스토그램 평활화', command=a_histoEqual)

otherMenu = Menu(mainMenu);mainMenu.add_cascade(label='다른 포맷 처리', menu=otherMenu)
otherMenu.add_command(label='CSV로 내보내기', command=saveCSV)
otherMenu.add_command(label='CSV(셔플)로 내보내기', command=saveShuffleCSV)
otherMenu.add_command(label='CSV 불러오기', command=openCSV)
otherMenu.add_separator()
otherMenu.add_command(label='SQLite로 내보내기', command=saveSQLite)
otherMenu.add_command(label='SQLite에서 가져오기', command=openSQLite)
otherMenu.add_separator()
otherMenu.add_command(label='MySQL로 내보내기', command=saveMySQL)
otherMenu.add_command(label='MySQL에서 가져오기', command=openMySQL)
otherMenu.add_separator()
otherMenu.add_command(label='Excel로 내보내기(숫자)', command=saveExcel1)
otherMenu.add_command(label='Excel로 내보내기(음영)', command=saveExcel2)

window.mainloop()