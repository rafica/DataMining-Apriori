# -*- coding: utf-8 -*-

import itertools
accountKey = ''

def main():
    """
    if len(sys.argv) != 4:
        print 'Running command is python main.py <bing account key> <precision> \'<query>\''
        sys.exit()
    """
    minSupport = 0.1
    minConfidence = 0.5
    fileName = "integrated.csv"
    global accountKey
    accountKey = "JsV9AIVwzY0l654YiaIXAppMcpvpm7lvkcYdmzJrNcs"
    """
    try:
        minSupport = float(minSupport)
        if targetPrec<=0.0 or targetPrec>1.0:
            print 'Please enter a valid precision value (0-1)'
            sys.exit()
    except ValueError:
        print 'Please enter a valid precision value (0-1)'
        sys.exit()
    """
    a_priori(fileName, minSupport, minConfidence)


def getLargeSets(fileName, minSupport):
    f = open(fileName)
    supportDict = {}
    first = 1
    typeNames = []
    transactionNum = 0
    for line in f:
        basket_items = line.split(',')
        if first:
            first = 0
            for i in range(len(basket_items)):
                typeNames.append(basket_items[i].strip())
            continue

        transactionNum = transactionNum + 1

        for i in range(len(basket_items)):
            key = typeNames[i] + '|' + basket_items[i].strip()

            if key in supportDict:
                supportDict[key] = supportDict[key]+1
            else:
                supportDict[key] = 1
    f.close()
    itemNum = len(supportDict.keys())

    for item in supportDict.keys():
        if float(supportDict[item])/float(transactionNum) < minSupport:
            del supportDict[item]
    
    return supportDict.keys()



def a_priori(filename, min_sup, min_conf):
    
    k = 1

    Large1 = getLargeSets(filename, min_sup)
    
    LargeSets = []
    for element in Large1:
        li = []
        li.append(element)
        LargeSets.append(li)
    while LargeSets:
        k = k + 1
        Ck = aprioriGen(LargeSets, k) #generates candidates
        break



def aprioriGen(LargeItemSets, k):
    lastIndex = k-2
    Candidates =[]
    for i in range(len(LargeItemSets)):
        for j in range(i+1,len(LargeItemSets)):
            fail = 0
            for x in range(lastIndex-1):
                if LargeItemSets[i][x] != LargeItemSets[j][x]:
                    fail = 1
                    break
            if not fail:
                if LargeItemSets[i][lastIndex] < LargeItemSets[j][lastIndex]:
                    newItemSet = LargeItemSets[i][:]
                    newItemSet.append(LargeItemSets[j][lastIndex])
                    Candidates.append(newItemSet)

    #pruning
    #test this on higher k values
    for j in range(len(Candidates)):
        for i in itertools.combinations(Candidates[j], len(Candidates[j])-1):
            #print list(i) not in LargeItemSets
            if list(i) not in LargeItemSets:
                Candidates.pop(j)
                break    
        
    return Candidates










if __name__ == "__main__":
    main()
