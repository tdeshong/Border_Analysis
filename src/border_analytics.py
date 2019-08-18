# Python 3.7.4
from datetime import datetime
import csv

# global orderedDate

def writeReport (inputFile, outputFile):
  data = readFile(inputFile)
  if len(data)>0: 
    average(data, 'US-Mexico Border')
    finalAvg = average(data, 'US-Canada Border')
    writefile(outputFile, finalAvg)



'''
Reads a csv from Input directory
Returns a nested dictionary with hierarchy of
{date:{border: {measure: [value, average (defaulted to 0)]}}}
'''
'''
need to still check if the date is  date
'''
def readFile (inputFile):
  fileDict = {}
  header = ['Port Name', 'State', 'Port Code', 'Border', 'Date', 'Measure', 'Value', 'Location']

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

        if date not in fileDict:
          # primaryKeys.append(date)
          fileDict[date] = {border:{measure:[int(value), 0]}}
        elif border not in fileDict[date]:
          fileDict[date][border] = {measure:[int(value), 0]}
        elif measure not in fileDict[date][border]:
          fileDict[date][border][measure] = [int(value), 0]
        else:
          fileDict[date][border][measure][0] += int(value)

      global orderedDate
      orderedDate = list(fileDict.keys())
      orderedDate.sort(key = lambda date: datetime.strptime(date, "%m/%d/%Y %I:%M:%S %p"))
  except IOError:
    print ("Error: Can not read file")
  except (IndexError, ValueError):
    print ("Error: Inccorect File format")
  finally:
    return fileDict


def average (dataDict, border):
  
  filteredDate = [date for date in orderedDate if border in dataDict[date]]
  

  freqDict = {}

  for date in filteredDate:
    for measure in dataDict[date][border]:
      if measure not in freqDict:
        freqDict[measure]=[1, date]
      else:
        lastDate = freqDict[measure][1]
        lastVal, lastAvg = dataDict[lastDate][border][measure]
        freq = freqDict[measure][0]
        avg = sum([lastVal, lastAvg*(freq-1)])/freq
        dec = avg - int(avg)
        avg = int(avg+1) if dec>=0.5 else int(avg)
        # update everything
        freqDict[measure][0]+=1
        freqDict[measure][1] = date
        dataDict[date][border][measure][1] = avg

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

    for date in orderedDate[::-1]:
      print (date)
      monthSummary = sort(dataDict, date)
      for info in monthSummary:
        report.writerow(info)



if __name__ == "__main__":
  x =readFile("Border_Crossing_Entry_Data.csv")
  print(x)
  writeReport("Border_Crossing_Entry_Data.csv", "report.csv")
  # y = average(x, 'US-Mexico Border' )
  # print (y)
