'''
Created on Apr 23, 2014

@author: Abhinav Bajaj
'''

def main():
    mainDataFile = open('E:/D drive/Course Material/ADB/Assignments/dohmh_restaurant-inspections_002/WebExtract.csv', "r")
    cuisineFile = open('E:/D drive/Course Material/ADB/Assignments/dohmh_restaurant-inspections_002/Cuisine.txt', "r")
    violationFile = open('E:/D drive/Course Material/ADB/Assignments/dohmh_restaurant-inspections_002/Violation.txt', "r")
    outputFile = open('E:/D drive/Course Material/ADB/Assignments/dohmh_restaurant-inspections_002/INTEGRATED-DATASET.csv','w')
    # load cuisine mapping
    cuisine = {}
    for line in cuisineFile:
        lineParts = line.strip().split(',')
        cuisCode = lineParts[0].replace('"','')
        codeDesc = ''.join(lineParts[1:]).replace('"','')
        cuisine[cuisCode] = codeDesc
    
    # load voilationcode mapping
    violation = {}
    for line in violationFile:
        lineParts = line.strip().split('","')
        vioCode = lineParts[3].replace('"','')
        vioDesc = ''.join(lineParts[4:])
        vioDesc = '"' + vioDesc
        violation[vioCode] = vioDesc
    print violation
    
    boroDict = {'"1"':'MANHATTAN', '"2"':'THE BRONX','"3"':'BROOKLYN','"4"':'QUEENS','"5"':'STATEN ISLAND'};
    outputFile.write("BORO"+','+"ZIPCODE"+','+"CUISINE"+','+"VIOLCODE"+','+"CURRENTGRADE\n")
    lineCount = 0;
    for line in mainDataFile:
        lineCount = lineCount + 1
        if lineCount == 1:
            continue
        skipLine = False
        lineParts = line.strip().split('","')
        #print lineParts
        for j in range(len(lineParts)):
            if j==2 or j==7 or j==5 or j==10 or j==12:
                if lineParts[j] is None or lineParts[j] =='#N/A' or lineParts[j] == '' or lineParts[j] =='0':
                    skipLine = True
                    break
        if skipLine == True:
            continue 
        boroCodeKey = '"' + lineParts[2]+'"'
        cuisineCodeKey = lineParts[7]
    
        outputFile.write('"'+boroDict[boroCodeKey]+'"'+','+'"'+lineParts[5]+'"'+','+'"'+cuisine[cuisineCodeKey]+'"'+','+violation[lineParts[10]]+','+'"'+lineParts[12]+'"\n')
    outputFile.close()

if __name__ == "__main__":
    main()