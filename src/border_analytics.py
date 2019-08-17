# Python 3.7.4
from datetime import datetime
import csv


'''
Reads a csv from Input directory
Returns a nested dictionary with hierarchy of
{date:{border: {measure: [value, average (defaulted to 0)]}}}
'''
def readFile (inputFile):
  fileDict = {}
  header =['Port Name', 'State', 'Port Code', 'Border', 'Date', 'Measure', 'Value', 'Location']
  global primaryKeys
  primaryKeys = []
  try:
    with open ("input/"+inputFile) as f:
      firstLine = f.readline().strip().split(',')

      if header != firstLine:
        return fileDict
        

      for row in f.readlines(): 
        row = row.split(",")
        border,date, measure, value = row[3:7]
        border = border.strip()
        measure = measure.strip()
        
        # create dictionary
        if date not in fileDict:
          primaryKeys.append(date)
          fileDict[date] = {border:{measure:[int(value), 0]}}
        elif border not in fileDict[date]:
          fileDict[date][border] = {measure:[int(value), 0]}
        elif measure not in fileDict[date][border]:
          fileDict[date][border][measure] = [int(value), 0]
        else:
          fileDict[date][border][measure][0] += int(value)

    primaryKeys.sort(key = lambda date: datetime.strptime(date, "%m/%d/%Y %I:%M:%S %p"))
  except IOError:
    print ("Can not read file")
  except IndexError:
    print ("index error")
  except ValueError:
    print ("value error")
  finally:
    return fileDict
  # except :
  #   print ("File is not properly formatted")
      
'''
this function updates the monthly averages of the measures in the dicitonary and returns the update dictionary

dataDict --> dictionary with a hierarchy of {date:{border: {measure: [value, average]}}}
border --> one of 2 options which are 'US-Mexico Border' or 'US-Canada Border'

returns dictionary with the hierarchy of 
{date:{border: {measure: [value, average]}}}

****BUG : not occuring in consecutive months
'''
def average(dataDict, border):
  commonMeasure = []
  freq = []
  # for loop compares the measures 2 dates 2 at a time
  for dates in range(len(primaryKeys)-1):
    try:
      # measure at the current date
      mNow = dataDict[primaryKeys[dates]][border]
      # measure at the next date in the list
      mNext = dataDict[primaryKeys[dates+1]][border]
      measureIntersection = mNow.keys() & mNext.keys()

      # updating frequency of the measures seen
      if len(commonMeasure)==0:
        commonMeasure = list(measureIntersection)
        freq = list(map (lambda num: 1, list(measureIntersection)))
      else:
        temp = list(measureIntersection)
        for m in temp:
          if m in commonMeasure:
            freq[commonMeasure.index(m)] +=1

      # Calculating and updating monthly averages for measures
      if len(measureIntersection) > 0:
        for j in measureIntersection:
          if mNow[j][1]==0:
            mNext[j][1]= mNow[j][0]
          else:
            numMonth = freq[commonMeasure.index(m)]
            avg = sum([mNow[j][0], mNow[j][1]*(numMonth-1)])/numMonth
            dec = avg - int(avg)
            avg = int(avg+1) if dec>=0.5 else int(avg)
            mNext[j][1] = avg
            freq[commonMeasure.index(m)] +=1

    except KeyError:
      pass
    
  return dataDict


'''
The function sorts monthly measures by value, measure then border

dataDict --> dictionary with a hierarchy of {date:{border: {measure: [value, average]}}}
date --> string of a datatime object in format MM/DD/YYYY HH:MM:SS AM/PM

returns a sorted list of list [[border, date, measure, value, average], ... ]
'''
def sort(dataDict, date):
  monthSummary= []
  for border in dataDict[date]:
    for measure in dataDict[date][border]:
      summary = [border, date, measure] + dataDict[date][border][measure]
      monthSummary.append(summary)
  
  if len(monthSummary) > 1:
    monthSummary.sort(key = lambda info: (info[3], info[2], info[0]), reverse = True)
  return monthSummary

'''

'''
def writefile (outputFile, dataDict):
  with open ("output/"+outputFile, mode ='w') as fw:
    report = csv.writer(fw, delimiter = ',')
    report.writerow (['Border','Date','Measure','Value','Average'])

    for date in primaryKeys[::-1]:
      monthSummary = sort(dataDict, date)
      for info in monthSummary:
        report.writerow(info)

def writeReport (inputFile, outputFile):
  data = readFile(inputFile)
  if len(data)>0: 
    average(data, 'US-Mexico Border')
    finalAvg = average(data, 'US-Canada Border')
    writefile(outputFile, finalAvg)

# writeReport ("Border.csv", 'report.csv')
