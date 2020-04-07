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

    #ghi file
    log_file.write(str(nrow - 1) + '\n')
    log_file.write(str(ncol) + '\n')

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

    #cau i - SUMMARY
    def summary():            
        #ghi ra file log
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
            for x in range(1, nrow):
                if (data[x][col] != '?'):
                    sum += float(data[x][col])
            return sum/ncol
        elif (check == 0): #tim xuat hien nhieu nhat trong cot
            return xuatHienNhieuNhat(col)

    #cau ii - REPLACE
    def replace():
        #ghi ra file log
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
        #write body
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

#main
if option in ("summary"): 
    summary()

elif option in ("replace"): 
    replace() 

elif option in ("discretize"): 
    print ("Cau iii. Chia gio mot hoac nhieu thuoc tinh numeric") 

elif option in ("normalize"): 
    print ("Cau iv. Chuan hoa cac thuoc tinh co kieu numeric") 
