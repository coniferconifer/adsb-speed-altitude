#!/usr/bin/python3
# adsb-speed-altitude.py slicer for speed and altitude
# LICENSE Apache 2.0
# copyright 2023 by coniferconifer
#
import pandas as pd
import matplotlib.pyplot as plt
import csv
print('adsb-speed-altitude.py speed vs altitude')
speed=''
icao=''
time=''
with open('adsb202201081729.csv',newline='') as f:
#with open('adsb202201082242.csv',newline='') as f:
        writer = csv.writer(open('output.csv', 'w', newline=''),quoting=csv.QUOTE_NONNUMERIC, quotechar=' ')
        reader = csv.reader(f)
        icao_dict={}
        for row in reader:
            if ( row[1]=='4' ): #find MSG,4 where speed is written in row12
                speed=row[12]
                time=row[9]
                icao=row[4]
                icao_dict[icao]=speed # make latest icao and speed pair
                print(time,'.',icao,',',icao_dict[icao],',','speed')

#            if  row[1]=='3' and row[4] in icao_dict: # if MSG,3 
#                print(row[9],',',row[4],',',icao_dict[row[4]],',',row[11], ',',row[14],',' ,row[15])

            if  row[1]=='3' and row[4] in icao_dict: # if MSG,3 
                print(row[9],',',row[4],',',icao_dict[row[4]],',',row[11], ',',row[14],',' ,row[15])
                arg=row[9]+','+row[4]+','+icao_dict[row[4]]+','+row[11]+ ','+row[14]+','+row[15]
#                print( arg)
                writer.writerow([arg])
f.close()
# output.csv : time, icat , speed, altitude ,lat,lon
print('speed altitude analysis')
dat = pd.read_csv('output.csv',header=None,index_col=0)
delta=0.05
baselon=135.83 # sliced at this longitude
flight=dat
flight2=flight[ flight[5] < baselon+delta]
flight3=flight2[ flight2[5] >= baselon]
x=flight3[2]
print(x)
y=flight3[3]
print(y)
print(flight3)
plt.scatter(x,y,s=200 ,  alpha=0.10)
Title="Flight speed vs altitude at Lon="+str(baselon)+"delta="+str(delta)
plt.suptitle(Title)
plt.title("blue: 2022/1/8 17:29-19:29")
plt.ylabel("Altitude(ft)")
plt.xlabel("Speed(knot)")
plt.grid(True)
plt.savefig('adsb5.jpg')
