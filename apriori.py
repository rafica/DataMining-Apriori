#!/usr/bin/env python
# -*- coding: utf-8 -*-
from copy import deepcopy
import itertools
import operator
import sys

support = {}
transactionNum = 0
total_support= {}
def main():
    #if len(sys.argv) != 4:
    #    print 'Running command is python <path to INTEGRATED-DATASET.csv> <min_sup> <min_conf>'
    #    sys.exit()
    
    #fileName = sys.argv[1]
    #minSupport = float(sys.argv[2])
    #minConfidence = float(sys.argv[3])
    #outputFile = open("output.txt",'w')

    fileName = 'INTEGRATED-DATASET.csv'
    minSupport = 0.005
    minConfidence = 0.5
    outputFile = open("output.txt",'w')
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
    a_priori(fileName, minSupport, minConfidence, outputFile)
    #print total_support

    printConfidence(minConfidence,outputFile)
    outputFile.close()

def printConfidence(min_conf, outputFile):
    total_itemsets = []
    global support
    Confidence = {}

    global total_support
    global transactionNum
    
    for k in total_support:
        for item_set in total_support[k]:
            denominatorSupport = total_support[k][item_set]
            for single in total_support[1]:                
                if len(item_set) == 1:
                    if item_set[0]==single[0]:
                        continue
                #print list(itertools.permutations(list(item_set + single),k+1))            
                for numerator_set in list(itertools.permutations(list(item_set + single),k+1)):
                    if numerator_set in total_support[k+1]:
                        numeratorSupport = total_support[k+1][numerator_set]
                        confidence = float(numeratorSupport)/float(denominatorSupport)
                        if confidence >= min_conf:
                            #print confidence, item_set
                            Confidence[(item_set, single, numerator_set)] = confidence
                    
                
    #print Confidence
    sorted_conf = sorted(Confidence.iteritems(), key=operator.itemgetter(1), reverse = True)

    print >> outputFile,'\n'
    print >> outputFile,"==High-confidence association rules (",min_conf*100,"%)"

    #print sorted_conf
    #print support
    for entry in sorted_conf:
        #print entry
        lhs = entry[0][0][0]
        for word in entry[0][0][1:]:
            lhs = lhs + ' ,' +word
        #print float(support[entry[0][0] + entry[0][1]])
        supp = float(support[entry[0][2]]) / float(transactionNum)
        print >> outputFile,'[',lhs,'] => [',entry[0][1][0],'] (Conf:',entry[1]*100,'%, Supp:',supp*100,'%)'
    
            


def getLargeSets(k, fileName, minSupport, candidates):

    global total_support
    global transactionNum
    transactionNum = -1 # initialize at -1 to take care of first line
    print "in getlargeSets"
    f = open(fileName)
    supportDict = {}
    typeNames = []
    row_items = []
    for line in f:
        basket_items = line.split('","')
        #basket_items[0] = basket_items[0][1:]
        #basket_items[len(basket_items)-1] = basket_items[len(basket_items)-1][:-2]
        if transactionNum == -1:
            transactionNum = 0 # read the heading
            for i in range(len(basket_items)):
                typeNames.append(basket_items[i].strip())
            continue

        transactionNum = transactionNum + 1
        for i in range(len(basket_items)):
            if not basket_items[i].strip():
                continue
            row_items.append(typeNames[i] + '|' + basket_items[i].strip())
        
        #print candidates
        for i in itertools.combinations(row_items, k):
            new_key = deepcopy(i)

            #CHECK IF PRESENT IN CANDIDATES
            if k>1 and list(new_key) not in candidates:
                continue

            if new_key in supportDict:
                supportDict[new_key] = supportDict[new_key] + 1
            else:
                supportDict[new_key] = 1
        
        row_items = []
        
    f.close()
    #print supportDict
    
    itemNum = len(supportDict.keys())

    
    print "length of dictionary of all items ",itemNum
    for item in supportDict.keys():
        if float(supportDict[item])/float(transactionNum) < minSupport:
            del supportDict[item]

    print "length of dictionary of all large items ", len(supportDict.keys()), "of value k ", k

    total_support[k] = supportDict  
    return supportDict.keys()



def a_priori(filename, min_sup, min_conf, outputFile):
    global total_support
    global support
    k = 1
    
    LargeSets = getLargeSets(k, filename, min_sup, [])

    while LargeSets:
        k = k + 1
        Ck = aprioriGen(LargeSets, k) #generates candidates
        LargeSets = getLargeSets(k, filename, min_sup, Ck)
        #print Ck

    print >> outputFile,"==Frequent itemsets (min_sup=",min_sup*100,"%)"

    #HAVE TO SORT
    for k in total_support:
        support_dict = total_support[k]
        for item_set in support_dict:
            support[item_set] = support_dict[item_set]

    sorted_x = sorted(support.iteritems(), key=operator.itemgetter(1), reverse=True)

    print 'total transactions ' , transactionNum
    for item_set_support in sorted_x:
        support1 = float(item_set_support[1]) / float(transactionNum)
        support1 = support1 * 100
        print >> outputFile,list(item_set_support[0]), ',' ,support1,'%'

    


def aprioriGen(LargeItemSets, k):
    lastIndex = k-2
    Candidates =[]
    print 'in aprioriGen and candidates of k ', k,' is going to be generated is '
    for i in range(len(LargeItemSets)):
        for j in range(i+1,len(LargeItemSets)):
            fail = 0
            for x in range(lastIndex):
                if LargeItemSets[i][x] != LargeItemSets[j][x]:
                    fail = 1
                    break
            if not fail:
                if LargeItemSets[i][lastIndex] < LargeItemSets[j][lastIndex]:
                    newItemSet = list(LargeItemSets[i][:])
                    newItemSet.append(LargeItemSets[j][lastIndex])
                    Candidates.append(newItemSet)
    #print Candidates
    print 'their length is ',len(Candidates)

    
    #pruning
    #TEST THIS ON HIGH K VALUES

    prunedCandidates = []
    pruneFlag = 0
    for j in range(len(Candidates)):
        for i in itertools.combinations(Candidates[j], k-1):
            #print list(i) not in LargeItemSets
            if i not in LargeItemSets:
                pruneFlag = 1
                break
        if not pruneFlag:
            prunedCandidates.append(Candidates[j])
            pruneFlag = 0
    print 'after pruning length is ',len(prunedCandidates)
    return prunedCandidates



if __name__ == "__main__":
    main()
