#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os.path
from os import path
import time
from datetime import datetime
from re import search
import calendar


#Function to store data in a dictionary and display them.
def displayData(totalArr, dayS, monthS, startS):
    ind = 0 
    ind2 = 0
    prev = '' #String variable to store the last even day and month to check with next event.
    counter = 0 #Loop control counter.
    
    #Events dictionary.
    Event={ 'day':totalArr[0],'month':totalArr[1],'year': totalArr[2],
    'start': totalArr[3],'end':totalArr[4],'id': totalArr[5],'description':totalArr[6],
    'location': totalArr[7],'circuit': totalArr[8],'broadcaster':totalArr[9],
    'direction':totalArr[10],'timezone':totalArr[11]  }

    
    #Printing out output to a file.
    sys.stdout = open('output.yaml', 'w')
     
    print("events:")
    
    #Displaying events.
    while True :
        
        if(dayS[ind] == Event['day'][ind2].replace('\n','') and 
        monthS[ind] == Event['month'][ind2].replace('\n','')
        and startS[ind] == Event['start'][ind2].replace('\n','')):
            
            counter = counter + 1  
            
            if prev != str(dayS[ind] + monthS[ind]):
                displayDateNum(Event['day'][ind2].replace('\n',''),
                Event['month'][ind2].replace('\n',''),
                Event['year'][ind2].replace('\n',''))
                
            displayID(Event['id'][ind2])
            displayDescription(Event['description'][ind2])
            displayCircuit(Event['circuit'][ind2])
            displayRotation(Event['direction'][ind2])
            displayLocation(Event['location'][ind2])
            displayStartTime(Event['start'][ind2])
            displayEndTime(Event['end'][ind2])
            displayDateAlpha(int(Event['day'][ind2]),int(Event['month'][ind2]),int(Event['year'][ind2]))
            displayTimezone(Event['timezone'][ind2])
            displayBroadcast(Event['broadcaster'][ind2])
            
        ind2 = ind2 + 1  
        
        if(counter == 1):
            prev = str(dayS[ind] + monthS[ind])
            ind = ind + 1 
            ind2 = 0
            counter = 0
           
        if(ind >= len(dayS)):
            break
        
        if (ind2 == len(Event['day']) and counter == 0):
            print("No Match")
            break
        
        if(ind2 == len(Event['day'])):
            ind2 = 0
    
    return ''

        
#Function to store and sort events' data.
def storeData(fileArr1,fileArr2,fileArr3):
    
    #Arrays/lists to store each event data.
    day={};month={};year={};Id={};description={};circuit={};locationID={};
    location={};start={};end={};location_Event={};circuit_Event={};
    broadcaster_Event={};direction_Event={};timezone_Event={};timezone={}; direction={};broadcaster={};
    broadcasterID={}
    
    storeBroadcasterName(fileArr3,broadcaster)
    storeDirection(fileArr2,direction)
    storeTimezone(fileArr2,timezone)
    storeLocation(fileArr2,location)
    storeCircuit(fileArr2,circuit)
    storeDay(fileArr1,day)
    storeMonth(fileArr1,month)
    storeYear(fileArr1,year)
    storeID(fileArr1,Id)
    storeDescription(fileArr1,description)
    storeBroadcasterID(fileArr1,broadcasterID)
    storeLocationID(fileArr1,locationID)
    storeStart(fileArr1,start)
    storeEnd(fileArr1,end)
    storeIdentifyLocation(location_Event,locationID,location)
    storeIdentifyCircuit(circuit_Event,locationID,circuit)
    storeIdentifyBroadcast(broadcaster_Event,broadcasterID,broadcaster)
    storeIdentifyDirection(direction_Event,locationID,direction)
    storeIdentifyTimezone(timezone_Event,locationID,timezone)
    
    #Array of arrays of the total needed arrays after storing and modifying data.
    totalArr = [day,month,year,start,end,Id,description,location_Event,circuit_Event,
    broadcaster_Event,direction_Event,timezone_Event]
    
    #Sort data.
    SortedDMS(totalArr)
    
    return ''

#Function to store events' locations.
def storeIdentifyLocation(location_Event,locationID,location):
    ind = -1

    for item in locationID:
        ind = ind + 1
        if(locationID[ind] != None):
            location_Event[ind]= location[int(locationID[ind][2:]) - 1]
    
    return ''

#Function to store events' circuits.
def storeIdentifyCircuit(circuit_Event,locationID,circuit):
    ind = -1
    for item in locationID:
        ind = ind + 1
        if(locationID[ind] != None):
            circuit_Event[ind]= circuit[int(locationID[ind][2:]) - 1]
            
    return ''

#Function to sotre events broadcasters after picking the correct ones for each event.
def storeIdentifyBroadcast(broadcaster_Event,broadcasterID,broadcaster):
    ind = -1
    for item in broadcasterID:
        ind = ind + 1
        
        #Checking if there is only one broadcaster to display and if not separate them.
        if(broadcasterID[ind] != None and (len(broadcasterID[ind]) == 5)):
            broadcaster_Event[ind]= broadcaster[int(broadcasterID[ind][2:]) - 1]
        
        #Separate multiple broacasters.
        elif(len(broadcasterID[ind]) > 5):
            ind2 = 4 
            ind3 = 2 
            counter = -1
            broadcaster_Event[ind]= ""
            for item in broadcasterID:
                counter = counter + 1
                broadcaster_Event[ind] = broadcaster_Event[ind] + broadcaster[int(broadcasterID[ind][ind3:ind2]) - 1].rstrip('\n') +','
                ind3 = ind3 + 5
                ind2 = ind2 + 5
                if(broadcasterID[ind][ind3:ind2]) == '': 
                    break
    return ''

#Function to store circuits direction.
def storeIdentifyDirection(direction_Event,locationID,direction):
    ind  = -1;
    for item in locationID:
        ind = ind + 1
        if(locationID[ind] != None):
            direction_Event[ind]= direction[int(locationID[ind][2:]) - 1]
    
    return ''

#Function to store events' timezones.
def storeIdentifyTimezone(timezone_Event,locationID,timezone):
    ind  = -1;
    for item in locationID:
        ind = ind + 1
        if(locationID[ind] != None):
            timezone_Event[ind]= timezone[int(locationID[ind][2:]) - 1]
    
    return ''

#Function to store events days, months and start-times then sort them.
def SortedDMS(totalArr):
    ind = -1
    ind2 = 0
    daySorted={}
    monthSorted={}
    startSorted={}

    #Arrays/lists to sotre the given specified dates.
    startDate = sys.argv[1].replace('--start=','')
    endDate = sys.argv[2].replace('--end=','')
    Sdate = time.strptime(startDate[5:],"%m/%d")
    Edate = time.strptime(endDate[5:], "%m/%d")

    for item in totalArr[0]:
        ind = ind + 1

        #Comapring the events day and month with the given specifed date range to display.
        if time.strptime(f"{totalArr[1][ind]}/{totalArr[0][ind]}","%m/%d") >= Sdate and time.strptime(f"{totalArr[1][ind]}/{totalArr          [0][ind]}","%m/%d") <= Edate:
         daySorted[ind2] = totalArr[0][ind]
         monthSorted[ind2] = totalArr[1][ind]
         startSorted[ind2] = totalArr[3][ind]
         ind2 = ind2 + 1
    
    #In case the given date doesn't specify any range of events, the program is terminated and an empty events' list is shown.
    if len(daySorted) != 0:
        sortData(daySorted,monthSorted,startSorted)
        displayData(totalArr,daySorted,monthSorted,startSorted)
    else:
        sys.stdout = open("output.yaml","w")
        print("events:")
        exit(0)
    return''

#Function to sort data.
def sortData(daySorted,monthSorted,startSorted):
    ind = -1
    combinedSortedDMT = []
    
    for item in daySorted:
        ind = ind + 1
        combinedSortedDMT.append(monthSorted[ind].replace('\n','') + daySorted[ind].replace('\n','') + 
        startSorted[ind].replace('\n','').replace(':',''))
        
      
    combinedSortedDMT.sort()
    
    ind = -1
    
    for item in combinedSortedDMT:
        ind = ind + 1
        monthSorted[ind] = combinedSortedDMT[ind][0:2]
        daySorted[ind] = combinedSortedDMT[ind][2:4]
        startSorted[ind] = combinedSortedDMT[ind][4:8][:2]+":"+combinedSortedDMT[ind][4:8][2:]
    
    return ''

#Function to store events' broadcasters directly from file.
def storeBroadcasterName(fileArr3,broadcasterName):
    ind = 0
    ind2 = 0
    for item in fileArr3:
     
     if fileArr3[ind] != None and ' <name>' in fileArr3[ind]:
         broadcasterName[ind2] = fileArr3[ind].strip(' <name>').replace('</name>','')
         ind2= ind2 + 1
     ind = ind + 1

#Function to store events' circuit direction directly from file.
def storeDirection(fileArr2,direction):
    ind = 0
    ind2 = 0
    for item in fileArr2:
     
     if fileArr2[ind] != None and ' <direction>' in fileArr2[ind]:
         direction[ind2] = fileArr2[ind].replace('        <direction>','').replace('</direction>','')
         ind2= ind2 + 1
     ind = ind + 1

#Function to directly store events' location from file.
def storeLocation(fileArr2,location):
    ind = 0
    ind2 = 0
    for item in fileArr2:
     
     if fileArr2[ind] != None and ' <location>' in fileArr2[ind]:
         location[ind2] = fileArr2[ind].strip(' <location>').replace('</location>','')
         ind2= ind2 + 1
     ind = ind + 1

#Function to directly store events' timezone from file.
def storeTimezone(fileArr2, timezone):
    ind = 0
    ind2 = 0
    for item in fileArr2:
     
     if fileArr2[ind] != None and ' <timezone>' in fileArr2[ind]:
         timezone[ind2] = fileArr2[ind].strip(' <timezone>').replace('</timezone>','')
         ind2= ind2 + 1
     ind = ind + 1

#Function to directly store events' circuit names from file.
def storeCircuit(fileArr2,circuit):
    ind = 0
    ind2 = 0
    for item in fileArr2:
     
     if fileArr2[ind] != None and ' <name>' in fileArr2[ind]:
         circuit[ind2] = fileArr2[ind].strip(' <name>').replace('</name>','')
         ind2= ind2 + 1
     ind = ind + 1

#Function to directly store events' days direclty from file.
def storeDay(fileArr1,day):
    ind = 0
    ind2 = 0
    for item in fileArr1:
     
     if fileArr1[ind] != None and ' <day>' in fileArr1[ind]:
         day[ind2] = fileArr1[ind].strip(' <day>').replace('</day>','').replace('\n','')
         ind2= ind2 + 1
     ind = ind + 1

#Function to store events' months directly from file.
def storeMonth(fileArr1,month):    
    ind = 0
    ind2 = 0
    for item in fileArr1:
     
     if fileArr1[ind] != None and ' <month>' in fileArr1[ind]:
         month[ind2] = fileArr1[ind].strip(' <month>').replace('</month>','').replace('\n','')
         ind2= ind2 + 1
     ind = ind + 1

#Function to store events' year direclty from year.
def storeYear(fileArr1,year):
    ind = 0
    ind2 = 0
    for item in fileArr1:
     
     if fileArr1[ind] != None and ' <year>' in fileArr1[ind]:
         year[ind2] = fileArr1[ind].strip(' <year>').replace('</year>','').replace('\n','')
         ind2= ind2 + 1
     ind = ind + 1

#Function to store events' ID direclty from file.
def storeID(fileArr1,Id):
    ind = 0
    ind2 = 0
    for item in fileArr1:
     
     if fileArr1[ind] != None and ' <id>' in fileArr1[ind]:
         Id[ind2] = fileArr1[ind].strip(' <id>').replace('</id>','')
         ind2= ind2 + 1
     ind = ind + 1

#Function to store events' description directly from file.
def storeDescription(fileArr1,description):
    ind = 0
    ind2 = 0
    for item in fileArr1:
     
     if fileArr1[ind] != None and ' <description>' in fileArr1[ind]:
         description[ind2] = fileArr1[ind].strip(' <description>').replace('</description>','')
         ind2= ind2 + 1
     ind = ind + 1

#Function to store events' broadcasters directly from file.
def storeBroadcasterID(fileArr1,broadcasterID):
    ind = 0
    ind2 = 0
    for item in fileArr1:
     
     if fileArr1[ind] != None and ' <broadcaster>' in fileArr1[ind]:
         broadcasterID[ind2] = fileArr1[ind].strip(' <broadcaster>').replace('</broadcaster>','').replace('<broadcaster>','')
         ind2= ind2 + 1
     ind = ind + 1
    

#Function to store events' locations direclty from file.
def storeLocationID(fileArr1,locationID):
    ind = 0
    ind2 = 0
    for item in fileArr1:
     
     if fileArr1[ind] != None and ' <location>' in fileArr1[ind]:
        locationID[ind2] = fileArr1[ind].strip(' <location>').replace('</location>','')
        ind2= ind2 + 1
     ind = ind + 1
  
#Function to directly store events' start-times from file.
def storeStart(fileArr1,start):
    ind = 0
    ind2 = 0
    for item in fileArr1:
     
     if fileArr1[ind] != None and ' <start>' in fileArr1[ind]:
         start[ind2] = fileArr1[ind].strip(' <start>').replace('</start>','').replace('\n','')
         ind2= ind2 + 1
     ind = ind + 1

#Function to direclty store events' end-times from file.
def storeEnd(fileArr1,end):
    ind = 0
    ind2 = 0
    for item in fileArr1:
     
     if fileArr1[ind] != None and ' <end>' in fileArr1[ind]:
         end[ind2] = fileArr1[ind].strip(' <end>').replace('</end>','')
         ind2= ind2 + 1
     ind = ind + 1
    
#Function to display events' broadcasters and check if there are multiple ones for each event.
def displayBroadcast(db):
    ind = 0
    ind2 = 0
    
    print('      broadcasters:')
    if ',' not in db:
         print("        -", db.replace('\n',''))
    elif ',' in db:
        while db[ind] != '' :
            ind = ind + 1
                    
            if ind < len(db):
                if db[ind] == ',':
                    print("        -",db[ind2:ind].replace('\n',''))
                    ind2 = ind + 1
            else:
                break

    return  ''
    
#Function to display events' rotations.
def displayRotation(rot):
    
    print(" (" + rot.replace('\n','') + ")") 

    return  ''
    
#Function to display events' timezones.
def displayTimezone(tmz):

    print(" (" + tmz.replace('\n','') + ")")

    return  ''
    
#Function to display events' day number. 
def displayDayinWeek(dw):
    
    print(" ",dw.replace('\n',''),end='')

    return  ''

#Function to display events' end-times.
def displayEndTime(et):
    
    stri = datetime.strptime(et.replace('\n',''),'%H:%M')
    print(" - " + stri.strftime('%I:%M'), end='')
    if int(et[0:2]) < 12:
        print(" AM",end='')
    else:
        print(" PM", end='')
        
    return  ''   

#Function to display events' start times.
def displayStartTime(st):
    
    stri = datetime.strptime(st.replace('\n',''),'%H:%M')
    print("      when: " + stri.strftime('%I:%M'), end='')
    if int(st[0:2]) < 12:
        print(" AM",end='')
    else:
        print(" PM", end='')
        
    return  ''    

#Function to display events' locations.
def displayLocation(loc):
    print("      location:",loc.replace('\n',''))
    return  ''
    
#Function to display events' circuits.
def displayCircuit(crc):
    print("      circuit:",crc.replace('\n',''),end='')
    return  ''
    
#Function to display events' description.
def displayDescription(dsc):
    print("      description:",dsc.replace('\n',''))
    return  ''
    
#Function to display events' dates numbered.
def displayDateNum(day,month,year):

    print("  - " + day + "-"+ month + "-" + year + ":")
 
    return  ''
    
#Function to display events' date in alpha-numerical form.
def displayDateAlpha (day,month,year):
    
    stri = calendar.weekday(int(year),int(month),int(day))
    
    print(" " + calendar.day_name[stri]+", ",end="")
    month_year = datetime.strptime(str(month),"%m" )
    print(month_year.strftime("%B"), str(day) + ", " + str(year),end="",)
    return  ''

#Function to display events' IDs.
def displayID(ID):
    print( "    - id:",ID.replace('\n',''))
    return ''

#Function to read data from files into arrays/lists.
def readFile():
    
    arr1 = {}
    arr2 = {}
    arr3 = {}
    
    ind = 0
    file_1 = sys.argv[3].replace("--events=",'')
    if path.exists(file_1):
       Ofile1 = open(file_1,'r')
       with Ofile1 as file1:
            for line in file1:
                arr1[ind] = line
                ind = ind + 1
       Ofile1.close()
    else:
        print("ERROR: Events File Doesn't Exist!!")
        exit(0)
 

    ind = 0
    file_2 = sys.argv[4].replace("--circuits=",'');
    if path.exists(file_2):
       Ofile2 = open(file_2, 'r')
       with Ofile2 as file2:
            for line in file2:
                arr2[ind] = line
                ind = ind + 1
            Ofile2.close()  
    else:
        print("ERROR: Circuits File Doesn't Exist!!")
        exit(0)

    ind = 0
    file_3 = sys.argv[5].replace("--broadcasters=",'');
    if path.exists(file_3):
       Ofile3 = open(file_3, 'r')
       with Ofile3 as file3:
            for line in file3:
                arr3[ind] = line
                ind = ind + 1
            Ofile3.close()
    else:
        print("ERROR: Broadcasters File Doesn't Exist!!")
        exit(0)


    storeData(arr1,arr2,arr3)
    
    return ''

#Main function.
def main():

    #Read files.
    readFile()
    
    
if __name__ == "__main__":
     main()
    
