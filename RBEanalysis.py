# RBEanalysis.py
# python script to read DORA heartbeat telemetry, focusing on the RBE data from the last two weeks of flight
# 1. read out the relevant data: timestamps, sequence count, payload fb data, and location
# 2. pick only the points: (a) after the ant has deployed, (b) with matching 1st and 2nd halves, and (c) that have been recently updated
# 3. save to a new csv

import numpy as np
import csv
from datetime import datetime, timedelta
import math
import pandas as pd

# deployed ant sometime around 11-15 00:00 UTC
firstfile = 'heartbeat_firsthalf.csv'
secondfile = 'heartbeat_secondhalf.csv'

f = open(firstfile)
reader = csv.reader(f, delimiter=',')
seqcount1 = []
timestamp1 = []
filterbank_ch1 = []
filterbank_ch2 = []
updated_timestamp1 = []
alt = []
lat = []
lon = []
i = 0
for line in reader:
    if i==0: # ignore the title line
        i+=1
        continue
    if (int(line[9]) < 1728386700) or (int(line[9]) >1732798000): # throw away packets with weird timestamps
        continue
    seqcount1.append(int(line[7]))
    timestamp1.append(int(line[9]))
    filterbank_ch1.append(float(line[-6]))
    filterbank_ch2.append(float(line[-5]))
    updated_timestamp1.append(line[-4])
    alt.append(float(line[-3]))
    lat.append(float(line[-2]))
    lon.append(float(line[-1]))
    i+=1

f = open(secondfile)
reader = csv.reader(f, delimiter=',')
timestamp2 = []
seqcount2 = []
filterbank_ch3 = []
filterbank_ch4 = []
filterbank_ch5 = []
filterbank_ch6 = []
filterbank_ch7 = []
filterbank_ch8 = []
updated_timestamp2 = []
i = 0
for line in reader:
    if i==0: # ignore the title line
        i+=1
        continue
    if (int(line[0]) < 1728386700) or (int(line[0]) >1732798000): # throw away packets with weird timestamps
        continue
    seqcount2.append(int(line[8])-1)
    timestamp2.append(int(line[0]))
    filterbank_ch3.append(float(line[-21]))
    filterbank_ch4.append(float(line[-20]))
    filterbank_ch5.append(float(line[-19]))
    filterbank_ch6.append(float(line[-18]))
    filterbank_ch7.append(float(line[-17]))
    filterbank_ch8.append(float(line[-16]))
    updated_timestamp2.append(line[-4])
    i+=1

seqcount1 = np.array(seqcount1)
seqcount2 = np.array(seqcount2)
packetno1 = [i for i in range(len(timestamp1))]
packetno2 = [i for i in range(len(timestamp2))]
# sometimes these timestamps don't match up. it seems like the second half timestamp was consistently 7 hours behind, but this might have been fixed in the decoder
timestamp1_r = np.array([datetime.utcfromtimestamp(i) for i in timestamp1])
timestamp2_r = np.array([datetime.utcfromtimestamp(i) for i in timestamp2])

# now match the first and second halves of the heartbeat
filterbank_data = []
time_delta = timedelta(hours=8) # look in 8-hr windows for matching packets
for i in range(len(timestamp2)):
    if filterbank_ch3[i] == 255: continue
    timestamp = timestamp2_r[i]
    seqcount = seqcount2[i]
    if seqcount < 10: continue # it's harder to match the lower sequence counts bc of constant restarts
    ind = np.where(np.abs(timestamp1_r-timestamp) < time_delta)
    tempSeqcountList = seqcount1[ind]
    try:
        matchIndex = np.where(tempSeqcountList==seqcount) # sometimes this doesn't work. to do: implement find nearest
        finalIndex = ind[0][matchIndex[0][0]]
        data = [timestamp1_r[finalIndex],
                filterbank_ch1[finalIndex],
                filterbank_ch2[finalIndex],
                filterbank_ch3[i],
                filterbank_ch4[i],
                filterbank_ch5[i],
                filterbank_ch6[i],
                filterbank_ch7[i],
                filterbank_ch8[i],
                alt[finalIndex],
                lat[finalIndex],
                lon[finalIndex]]
        filterbank_data.append(data)
    except:
        continue

# calibration parameters
p1_list = np.array([-41.816, -42.225, -39.413, -36.389, -39.096, -38.062, -38.759, -35.164])
p2_list = np.array([53.47, 51.09, 43.853, 36.678, 39.365, 37.424, 36.714, 28.01])
scale_factor = 0.010 # 1 bit is 10 mV

# cut all the repeating data points and calibrate the remaining data
filterbank_data = np.array(filterbank_data)
filterbank_cal = []
tot_power = []
for i in range(len(filterbank_data)):
    data = filterbank_data[i]
    fb = filterbank_data[i,1:9].astype(float)
    if i > 0:
        fb_past = filterbank_data[i-1,1:9].astype(float)
        if (fb_past == fb).all():
            continue
    power = p1_list*scale_factor*fb+p2_list
    totpower = np.sum(power)
    tot_power.append(totpower)
    new_data=data.copy()
    new_data[1:9]=power
    filterbank_cal.append(new_data)

filterbank_cal = np.array(filterbank_cal)
df = pd.DataFrame(filterbank_cal, columns=['timestamp', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8', 'altitude', 'latitude', 'longitude'])
df.to_csv("RBEdata.csv")


