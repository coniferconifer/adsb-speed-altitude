#!/usr/bin/python3
# adsb-speed-altitude.py slicer for speed and altitude
# LICENSE Apache 2.0
# copyright 2023 by coniferconifer
#
import pandas as pd
import matplotlib.pyplot as plt
import csv
import sys
print('adsb-speed-altitude.py speed vs altitude')
speed=''
icao=''
time=''
first_date=''
first_time=''
last_date=''
last_time=''
if len(sys.argv) < 2: # fine not specified
    print("specify .csv file from dump1090 port 30003")
    sys.exit(1)
try:
	f = open(sys.argv[1], 'r', newline='')  # open csv file
	print(sys.argv[1])
except FileNotFoundError: 
	print('csv file not found')
	sys.exit(2)

print('Phase1: producing output.csv as working file')
reader = csv.reader(f)
writer = csv.writer(open('output.csv', 'w', newline=''),quoting=csv.QUOTE_NONNUMERIC, quotechar=' ')
first_row = next(reader)
last_row = None
icao_dict={}
for row in reader:
	last_row = row
	if ( row[1]=='4' ): #find MSG,4 where speed is written in row12
		speed=row[12]
		time=row[9]
		icao=row[4]
		icao_dict[icao]=speed # make latest icao and speed pair
		print(time,'.',icao,',',icao_dict[icao],',','speed')

	if  row[1]=='3' and row[4] in icao_dict: # if MSG,3 
		print(row[9],',',row[4],',',icao_dict[row[4]],',',row[11], ',',row[14],',' ,row[15])
		arg=row[9]+','+row[4]+','+icao_dict[row[4]]+','+row[11]+ ','+row[14]+','+row[15]
		writer.writerow([arg])
# get start and  last date/time
		
first_date = first_row[8]
first_time = first_row[9]
last_date = last_row[8]
last_time = last_row[9]
print(f'First row {first_date} {first_time}')
print(f'Last row  {last_date} {last_time}')


f.close()
# output.csv : time, icat , speed, altitude ,lat,lon
print('Phase2: speed altitude analysis')

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

print('Phase3: making scatter plot')

plt.scatter(x,y,s=200 ,  alpha=0.10)
Title="Flight speed vs altitude at Lon="+str(baselon)+" delta="+str(delta)
plt.suptitle(Title)
plt.title(first_date + ' '+first_time + '-' + last_date + ' '+ last_time)
#plt.title("blue: 2022/1/8 17:29-19:29")
plt.ylabel("Altitude(ft)")
plt.xlabel("Speed(knots)")
plt.grid(True)

file_string = first_date+'-'+first_time+'.jpg'
new_string = file_string.replace(":", "-")
datetime_string = new_string.replace("/", "-")
plt.savefig( datetime_string)
print( datetime_string )

