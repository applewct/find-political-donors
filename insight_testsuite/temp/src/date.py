import os
from heapq import *


file_name = os.path.join(os.path.dirname(__file__), '../input/itcont.txt')
output_by_date = os.path.join(os.path.dirname(__file__), '../output/medianvals_by_date.txt')

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


date_med_dict = {}
date_count_dict = {}
date_amt_dict = {}

with open(file_name, 'r') as f:
    for line in f:
        result = []
        line = line.split('|')
        #skip for CMTE_ID is none, OTHER_ID is not none, TRANSACTION_AMT is none, ZIP_CODE is none
        if (line[0] == '' or line[15] != '' or line[14] == '' or line[13] == ''):
            continue 
             
        date = line[13]
        recipient = line[0]
        if (date, recipient) not in date_med_dict:
            date_med_dict[(date, recipient)] = MedianFinder()
            date_count_dict[(date, recipient)] = 0
            date_amt_dict[(date, recipient)] = 0
        date_med_dict[(date, recipient)].addNum(float(line[14]))
        date_count_dict[(date, recipient)] += 1
        date_amt_dict[(date, recipient)] += int(line[14])
        
        tmpMed = date_med_dict[(date, recipient)].findMedian()
        med_trans = convert(tmpMed)
        
# result = [line[0], date, str(med_trans), str(date_count_dict[(date, recipient)]), str(date_amt_dict[(date, recippient)])]

for key in date_med_dict:
    result = [key[1], key[0], str(convert(date_med_dict[key].findMedian())), str(date_count_dict[key]), str(date_amt_dict[key])]   
    with open(output_by_date, 'a') as f:
        f.write("|".join(result) + '\n')

