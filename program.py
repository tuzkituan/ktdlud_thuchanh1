import sys, getopt, csv

#read cac tham so command line   
option = sys.argv[1]
inputfile = sys.argv[2]
outputfile = sys.argv[3]
logfile = sys.argv[4]
  
def is_number(s):
    try:
        complex(s) # for int, long, float and complex
    except ValueError:
        return False
    return True

#cau i
def summary():
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
        nrow = len(data) - 1

        #ghi file
        log_file.write(str(nrow) + '\n')
        log_file.write(str(ncol) + '\n')
        
        #check thuoc tinh va kieu du lieu
        for y in range(0, ncol):
            check = 0
            log_file.write('Thuoc tinh ' + str(y+1) + ': ' + data[0][y])  
            for x in range(1, nrow + 1):
                if (is_number(data[x][y]) == False):
                    log_file.write(' nominal\n')
                    check = 1
                    break
            if (check == 0):
                log_file.write(' numeric\n')
            print('\n')
               

#main
if option in ("summary"): 
    summary()

elif option in ("replace"): 
    print ("Cau ii. Dien gia tri bi thieu cho tat ca cac thuoc tinh") 

elif option in ("discretize"): 
    print ("Cau iii. Chia gio mot hoac nhieu thuoc tinh numeric") 

elif option in ("normalize"): 
    print ("Cau iv. Chuan hoa cac thuoc tinh co kieu numeric") 
