import os
from heapq import *


file_name = os.path.join(os.path.dirname(__file__), '../input/itcont.txt')
output_by_zip = os.path.join(os.path.dirname(__file__), '../output/medianvals_by_zip.txt')

def convert(tmpMed):
    if tmpMed * 10 % 10 >= 5:
        return (int)(tmpMed + 1)
    else: 
        return (int)(tmpMed)

class MedianFinder:
    def __init__(self):
        self.heaps = [], []

    def addNum(self, num):
        small, large = self.heaps
        heappush(small, -heappushpop(large, num))
        if len(large) < len(small):
            heappush(large, -heappop(small))

    def findMedian(self):
        small, large = self.heaps
        if len(large) > len(small):
            return float(large[0])
        return (large[0] - small[0]) / 2.0



zipcode_med_dict = {}
zipcode_count_dict = {}
zipcode_amt_dict = {}

with open(file_name, 'r') as f:
    for line in f:
        result = []
        line = line.split('|')
        #skip for CMTE_ID is none, OTHER_ID is not none, TRANSACTION_AMT is none, ZIP_CODE is none
        if (line[0] == '' or line[15] != '' or line[14] == '' or line[10] == ''):
            continue 
        
        #skip invalid zipcode
        if (len(line[10]) <5):
            continue
        
        
        zipcode = line[10][0:5]
        if line[10][0:5] not in zipcode_med_dict:
            zipcode_med_dict[zipcode] = MedianFinder()
            zipcode_count_dict[zipcode] = 0
            zipcode_amt_dict[zipcode] = 0
        zipcode_med_dict[zipcode].addNum(float(line[14]))
        zipcode_count_dict[zipcode] += 1
        zipcode_amt_dict[zipcode] += int(line[14])
        
        tmpMed = zipcode_med_dict[zipcode].findMedian()
        med_trans = convert(tmpMed)
        
        result = [line[0], zipcode, str(med_trans), str(zipcode_count_dict[zipcode]), str(zipcode_amt_dict[zipcode])]

        
        with open(output_by_zip, 'a') as f:
            f.write("|".join(result) + '\n')

