import sys, getopt, csv

#read cac tham so command line   
option = sys.argv[1]
inputfile = sys.argv[2]
outputfile = sys.argv[3]
logfile = sys.argv[4]
  
# initializing the titles and rows list 
log_file = open(logfile,"w")

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

    def is_number(s):
        try:
            complex(s) # for int, long, float and complex
        except ValueError:
            return False
        return True

    #cau i
    def summary():            
        #check thuoc tinh va kieu du lieu
        for y in range(0, ncol):
            check = 0
            log_file.write('Thuoc tinh ' + str(y+1) + ': ' + data[0][y])  
            for x in range(1, nrow):
                if (is_number(data[x][y]) == False):
                    log_file.write(', nominal\n')
                    check = 1
                    break
            if (check == 0):
                log_file.write(', numeric\n')
    
    def countMissingValues(col):
        missingvalues = 0
        for x in range(1, nrow):
            if (data[x][col] == '?'):
                missingvalues += 1 
        return missingvalues

    def countSoLanXuatHien(value,col):
        count = 0
        for x in range(1, nrow):
            if (data[x][col] == value):
                count += 1
        return count

    def xuatHienNhieuNhat(col):
        max = countSoLanXuatHien(data[1][col],col)
        result = data[1][col]
        for x in range(2, nrow):
            if (countSoLanXuatHien(data[x][col],col) > max):
                result = data[x][col]
        return result

    def dataToReplace(col, check):
        if (check == 1):
            sum = 0
            for x in range(1, nrow):
                sum += float(data[x][col])
            return sum
        elif (check == 0):
            return xuatHienNhieuNhat(col)

    #cau ii
    def replace():
        #check thuoc tinh va kieu du lieu
        for y in range(0, ncol):
            check = 0
            log_file.write('Thuoc tinh ' + str(y+1) + ': ' + data[0][y] + ', ')
            log_file.write(str(countMissingValues(y)))
            if (countMissingValues(y) != 0):
                for x in range(1, nrow):
                    if (is_number(data[x][y]) == False):
                        mostText = dataToReplace(y,0)
                        log_file.write(", " + str(mostText) + '\n')
                        check = 1
                        break
                if (check == 0):
                    avg = dataToReplace(y,1)
                    log_file.write(", " + str(avg) + '\n')
            else:
                log_file.write('\n')
                
#main
if option in ("summary"): 
    summary()

elif option in ("replace"): 
    replace() 

elif option in ("discretize"): 
    print ("Cau iii. Chia gio mot hoac nhieu thuoc tinh numeric") 

elif option in ("normalize"): 
    print ("Cau iv. Chuan hoa cac thuoc tinh co kieu numeric") 
