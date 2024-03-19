import csv
import sys
from datetime import date
class energyData:
    def __init__(self,ESIID,USAGE_DATE,REVISION_DATE,USAGE_START_TIME,USAGE_END_TIME,USAGE_KWH,ESTIMATED_ACTUAL,CONSUMPTION_SURPLUSGENERATION):
        self.esiid = ESIID
        self.usageDate = USAGE_DATE
        self.revisionDate = REVISION_DATE
        self.usageStartTime = USAGE_START_TIME
        self.usageEndTime = USAGE_END_TIME
        self.usageKWH = USAGE_KWH
        self.estimatedActual = ESTIMATED_ACTUAL
        self.consumptionSurplus = CONSUMPTION_SURPLUSGENERATION
    def __str__(self):
       return f"{self.esiid} {self.usageDate} {self.revisionDate} {self.usageStartTime} {self.usageEndTime} {self.usageKWH} {self.estimatedActual} {self.consumptionSurplus}"
    def getUsageKWH(self): 
        return self.usageKWH.strip().replace("'","")
    def getUsageStartTime(self):
        return self.usageStartTime.replace("'","")
    def getUsageDate(self):
        return self.usageDate.replace("'","")

class customerData:
    eDataArray = []
    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName
    
    def energyDataInput(self,filename):
        with open(filename, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                row = str(row)
                row = row.split(",")
                eData = energyData(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
                self.eDataArray.append(eData)
    
    def flatRateCalculation(self,rate):
        sum = 0
        for i in self.eDataArray:
            sum = rate * float(i.getUsageKWH()) + sum
        return sum
    
    def varyRate(self, dayTimeRate, nightRate, dayStartTime, nightStartTime):
        sum = 0
        for i in self.eDataArray:
            hour = int(i.getUsageStartTime().split(":")[0])
            if(hour >= dayStartTime or hour < nightStartTime):
                sum = dayTimeRate * float(i.getUsageKWH())+ sum
            else:
                sum = nightRate * float(i.getUsageKWH())+ sum
        return sum
    
    def compareRates(self, dayTimeRate, nightRate, dayStartTime, nightStartTime, rate, freeWeekendsRate, freeHighestDays, numDays):
        flat = self.flatRateCalculation(rate)
        vary = self.varyRate(dayTimeRate, nightRate, dayStartTime, nightStartTime)
        weekends = self.freeWeekends(freeWeekendsRate)
        highestDays = self.highestDay(freeHighestDays,numDays)
        ratesList = [flat, vary, weekends, highestDays]
        ratesList.sort()
        if(ratesList[0] == flat):
            return "The flat rate is best"
        elif(ratesList[0] == vary):
            return "The variable rate is best"
        elif(ratesList[0] == weekends):
            return "Free weekends rate is best"
        else:
            return "The free highest days rate is best"
    
    def variableCompareRates(self, dayTimeRate, nightRate, dayStartTime, nightStartTime, rate, freeWeekendsRate, freeHighestDays, numDays, checkboxList):
        ratesList = None
        for i in checkboxList:
            if(i == '1'):
                vary = self.varyRate(dayTimeRate, nightRate, dayStartTime, nightStartTime)
                ratesList.append(vary)
            if(i == '2'):
                flat = self.flatRateCalculation(rate)
                ratesList.append(flat)
            if(i == '3'):
                weekends = self.freeWeekends(freeWeekendsRate)
                ratesList.append(weekends)
            if(i == '4'):
                highestDays = self.highestDay(freeHighestDays,numDays)
                ratesList.append(highestDays)
        ratesList.sort()
        if(ratesList[0] == flat):
            return "The flat rate is best"
        elif(ratesList[0] == vary):
            return "The variable rate is best"
        elif(ratesList[0] == weekends):
            return "Free weekends rate is best"
        else:
            return "The free highest days rate is best"
    
    def freeWeekends(self, rate):
        sum = 0
        for i in self.eDataArray:
            month = i.getUsageDate().split("/")[0].replace(" ","")
            if(int(month) < 10):
                month = "0" + month
            day = i.getUsageDate().split("/")[1]
            if(int(day) < 10):
                day = "0" + day
            year = i.getUsageDate().split("/")[2]
            if(date.fromisoformat(year + "-" + month + "-" +  day).weekday() < 5):
                sum = rate * float(i.getUsageKWH())+ sum
        return sum
    
    def highestDay(self, rate, numDays):
        sum = 0
        sumDay = 0
        monthc = self.eDataArray[0].getUsageDate().split("/")[0].replace(" ","")
        dayc = self.eDataArray[0].getUsageDate().split("/")[1].replace(" ","")
        sumList = []
        count = 0
        daycount = 0
        for i in self.eDataArray:
            month = i.getUsageDate().split("/")[0].replace(" ","") 
            day = i.getUsageDate().split("/")[1].replace(" ","")
            if(day == dayc):
                    sumDay = rate * float(i.getUsageKWH())+ sumDay
                    count = count + 1
            else:
                    sumList.append(sumDay)
                    count = 1
                    dayc = day
                    daycount = daycount + 1
                    sumDay = rate * float(i.getUsageKWH())
            if(month != monthc):
                monthc = month
                sumDay = rate * float(i.getUsageKWH())
                daycount = daycount + 1
                dayc = day
                sumList.sort(reverse=True)
                c = len(sumList) - 1
                while(c > numDays):
                    sum = sumList[c] + sum
                    c = c - 1
                sumList = []
        sumList.append(sumDay)
        sumList.sort(reverse=True)
        c = len(sumList) - 1
        while(c > -1):
            sum = sumList[c] + sum
            c = c - 1
        return sum


#i = customerData("Jonathan","Procknow")
#i.energyDataInput(r"C:\Users\carso\OneDrive - Clear Creek ISD\ISProject\IntervalData(4).csv")
#print(i.highestDay(.15, 1))
#print(i.freeWeekends(1))
#print(i.flatRateCalculation(.15))
#print(i.varyRate(9999,20,9,18))
#print(i.compareRates(9999,20,9,18,12,1,.15,1))

        



