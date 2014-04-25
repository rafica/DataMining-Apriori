'''
Created on Apr 23, 2014

@author: Abhinav Bajaj
'''

import sys

def main():
    if len(sys.argv) != 5:
        print 'Running command is python cleaningData.py <Path to WebExtract.txt> <Path to Cuisine.txt> <Path to Violation.txt> <INTEGRATED-DATASET output file path>'
        sys.exit()
    
    webExtractPath = sys.argv[1]
    cuisineFilePath = sys.argv[2]
    violationFilePath = sys.argv[3]
    IntegDataFilePath = sys.argv[4]
    mainDataFile = open(webExtractPath, "r")
    cuisineFile = open(cuisineFilePath, "r")
    violationFile = open(violationFilePath, "r")
    outputFile = open(IntegDataFilePath,'w')
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
    #print violation
    
    boroDict = {'"1"':'MANHATTAN', '"2"':'THE BRONX','"3"':'BROOKLYN','"4"':'QUEENS','"5"':'STATEN ISLAND'};
    outputFile.write('"BORO"'+','+'"ZIPCODE"'+','+'"CUISINE"'+','+'"VIOLATION"'+','+'"CURRENTGRADE"\n')
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