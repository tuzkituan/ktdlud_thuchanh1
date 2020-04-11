import sys, csv

#read cac tham so trong command line   
option = sys.argv[1]
inputfile = sys.argv[2]
outputfile = sys.argv[3]
logfile = sys.argv[4]
  
# cac file de write
log_file = open(logfile,"w")
output_file = open(outputfile,'w')

#read csv
with open(inputfile, 'r') as csvFile:
    #so cot
    first_line = csvFile.readline()
    csvFile.seek(0)
    ncol = first_line.count(',') + 1 
    
    #read file ra bien data
    data = [row for row in csv.reader(csvFile)]   

    #get so dong
    nrow = len(data)
    #xac dinh mot gia tri s la so hay khong?
    def is_number(s):
        try:
            complex(s) # for int, long, float and complex
        except ValueError:
            return False
        return True

    #kiem tra kieu du lieu cua 1 cot
    def checkDataTypeOfCol(col):
        datatype = 'numeric' #0 la nominal, 1 la numeric
        for x in range(1, nrow):
            if (is_number(data[x][col]) == False and data[x][col] != '?'):
                datatype = 'nominal'
        return datatype

    #CAU 1 - SUMMARY -------------------------------------------------
    def summary():            
        #ghi ra file log
        log_file.write(str(nrow - 1) + '\n')
        log_file.write(str(ncol) + '\n')
        for y in range(0, ncol):
            log_file.write('Thuoc tinh ' + str(y+1) + ': ' + data[0][y])  
            if (checkDataTypeOfCol(y) == 'nominal'):
                log_file.write(', nominal\n')
            else:
                log_file.write(', numeric\n')

    #dem so gia tri thieu trong 1 cot, gia tri thieu la dau cham hoi '?'
    def countMissingValues(col):
        missingvalues = 0
        for x in range(1, nrow):
            if (data[x][col] == '?'):
                missingvalues += 1 
        return missingvalues

    #dem so lan xuat hien cua 1 text trong cot
    def countSoLanXuatHien(value,col):
        count = 0
        for x in range(1, nrow):
            if (data[x][col] == value):
                count += 1
        return count

    #text xuat hien nhieu nhat trong cot
    def xuatHienNhieuNhat(col):
        max = countSoLanXuatHien(data[1][col],col)
        result = data[1][col]
        for x in range(2, nrow):
            if (countSoLanXuatHien(data[x][col],col) > max):
                result = data[x][col]
        return result

    #xac dinh du lieu thay vao '?' la nominal hay numeric
    #neu la nominal thi tim gia tri xuat hien nhieu nhat
    #neu la numeric thi tim gia tri trung binh cua cot
    def dataToReplace(col, check):
        if (check == 1): #tinh trung binh cua cot
            sum = 0
            a = nrow
            for x in range(1, nrow):
                if (data[x][col] != '?'):
                    sum += float(data[x][col])
                    a -= 1
            return sum/(nrow-a)
        elif (check == 0): #tim xuat hien nhieu nhat trong cot
            return xuatHienNhieuNhat(col)

    #CAU 2- REPLACE  -------------------------------------------------
    def replace():
        #ghi ra file log
        log_file.write(str(nrow - 1) + '\n')
        log_file.write(str(ncol) + '\n')
        for y in range(0, ncol):
            log_file.write('Thuoc tinh ' + str(y+1) + ': ' + data[0][y] + ', ')
            log_file.write(str(countMissingValues(y)))
            if (countMissingValues(y) != 0):
                if (checkDataTypeOfCol(y) == 'nominal'):
                    mostText = dataToReplace(y,0)
                    log_file.write(", " + str(mostText) + '\n')
                else:
                    avg = dataToReplace(y,1)
                    log_file.write(", " + str(avg) + '\n')
            else:
                log_file.write('\n')

        #ghi ra file output
        for x in range(nrow):
            for y in range(ncol):
                if (data[x][y]=='?'):
                    if (checkDataTypeOfCol(y) == 'nominal'):
                        mostText = dataToReplace(y,0)
                        output_file.write(str(mostText))
                    else:
                        avg = dataToReplace(y,1)
                        output_file.write(str(avg))
                    if (y < ncol - 1):
                            output_file.write(',')
                else:
                    output_file.write(data[x][y])
                    if (y < ncol - 1):
                        output_file.write(',')
            output_file.write('\n')

    #CAU III - CHIA GIO ----------------------------------------------
    
    def Minx(col):
        min = float(data[1][col])
        for x in range(1, nrow):
            if (float(data[x][col]) < min):
                min = float(data[x][col])
        return int(min)

    def Maxx(col):
        max = float(data[1][col])
        for x in range(1, nrow):
            if (float(data[x][col])> max):
                max = float(data[x][col])
        return int(max)

    #CHIA GIO THEO CHIEU RONG ----------------------------------------
    #kiem tra 1 gia tri trong cot co trong 1 gio xac dinh hay khong
    def checkLineInGioTheoChieuRong(value, col, giaTriDau, giaTriCuoi):
        if (float(value) >= float(giaTriDau) and float(value) < float(giaTriCuoi)):
            return True
        return False

    #dem so dong cung 1 gio xac dinh [giaTriDau, giaTriCuoi)
    def countRowsCungGioTheoChieuRong(col, giaTriDau, giaTriCuoi):
        count = 0
        #dem gia tri = max
        if (float(giaTriCuoi) == float(Maxx(col))):
            count += 1
        #dem gia tri != max
        for x in range(1, nrow):
            if (checkLineInGioTheoChieuRong(data[x][col], col, giaTriDau, giaTriCuoi)):
                count += 1
        return count

    #chia gio cho 1 cot, return 1 list cac gio cua cot do
    def chiaGioChieuRong(sogio, col):
        lengio = int((Maxx(col) - Minx(col))/sogio)
        #do rong cua gio = 0, gan = 1
        if (lengio == 0): 
            lengio = 1

        min = Minx(col)
        max = Maxx(col)

        #gioList chua danh sach cac gio da chia
        #vi du gioList=[[2,4],[4,6]]
        gioList = []

        firstValue = min
        count = 0
        #chia gio
        for x in range(0, sogio):
            count += 1 # dem so gio da chia
            if (count == sogio):
                gioListChild = [firstValue, max]
                gioList.append(gioListChild)
            else:
                gioListChild = [firstValue, firstValue + lengio]
                gioList.append(gioListChild)
                firstValue += lengio
        return gioList

    def writeLogTheoChieuRong(sogio):
        #ghi file log
        for col in range(0,ncol):
            if (checkDataTypeOfCol(col) == 'numeric'):  
                gioList = chiaGioChieuRong(sogio, col)
                log_file.write('Thuoc tinh: ' + data[0][col] + ', ')
                for x in range(0, sogio):
                    firstvalue = gioList[x][0]
                    lastvalue = gioList[x][1]
                    count = countRowsCungGioTheoChieuRong(col, firstvalue, lastvalue)
                    log_file.write('[' + str(firstvalue) + ', ' + str(lastvalue) + '): ' + str(count))
                    if (x < sogio - 1):
                        log_file.write(', ')
                    else:
                        log_file.write('\n')

    #lay ra MIEN GIA TRI cua 1 gia tri bat ky trong bang
    def getGioOf1CellTheoChieuRong(sogio, col, value):
        gioList = chiaGioChieuRong(sogio, col)
        for x in range(0, sogio):
            firstvalue = gioList[x][0]
            lastvalue = gioList[x][1]
            if (float(value) >= float(firstvalue) and float(value) <= float(lastvalue)):
                return (firstvalue, lastvalue)
        return 0

    def writeOutputTheoChieuRong(sogio):
        for y in range(0,ncol):
            output_file.write(data[0][y])
            if (y < ncol - 1):
                output_file.write(',')
        output_file.write('\n')
        for x in range(1,nrow):
            for y in range(0,ncol):
                if (checkDataTypeOfCol(y) == 'numeric'):
                    firstvalue, lastvalue = getGioOf1CellTheoChieuRong(sogio, y, data[x][y])
                    output_file.write('[' + str(firstvalue) + ',' + str(lastvalue) + '),')
                else:
                    output_file.write(data[x][y])
                    if (y < ncol - 1):
                        output_file.write(',')
            output_file.write('\n')


    #MAIN CHIA GIO ---------------------------------------------------
    def discretize(): 
        print ("Nhap so gio va phuong phap chia: ")
        print ("(1 la chia theo chieu rong, 2 la chia theo chieu sau.)") 
        sogio = int(input('Nhap so gio: '))
        pp = int(input('Phuong phap: '))
        if (pp == 1):
            writeOutputTheoChieuRong(sogio)
            writeLogTheoChieuRong(sogio)
            
            
            
#main ----------------------------------------------------------------
if option in ("summary"): 
    summary()

elif option in ("replace"): 
    replace() 

elif option in ("discretize"): 
    discretize()

elif option in ("normalize"): 
    print ("Cau iv. Chuan hoa cac thuoc tinh co kieu numeric") 
