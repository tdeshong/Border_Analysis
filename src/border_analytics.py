# Python 3.7.4
from datetime import datetime
import csv


def writeReport (inputFile, outputFile):
  '''
  Parameters: 
  inputFile --> csv in the input directory
  outputFile --> csv written to the output directory

  from input file calculates monthly averages and sorts by date, 
  value, measure, border in descending order
  and writes it to the outputFile in the output directory
  if input file is not a csv or is incorrectly formatted
  an output file will not be created
  '''
  data, ascDates= readFile(inputFile)
  if len(data)>0: 
    average(data, ascDates, 'US-Mexico Border')
    finalAvg = average(data, ascDates, 'US-Canada Border')
    writefile(outputFile, finalAvg, ascDates)


def readFile (inputFile):
  '''
  Parameter:
  inputFile --> csv in the input directory

  Reads a properly formatted csv from input directory

  Returns a tuple of a nested dictionary with hierarchy
  of {date:{border: {measure: [value, average
  (defaulted to 0)]}}} and a list of all the dates from the dictionary 
  in ascending order
  '''

  fileDict = {}
  ascDates = []
  header = ['Port Name', 'State', 'Port Code', 'Border', 'Date', 
            'Measure', 'Value', 'Location']

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

        # Creating the dictionary
        if date not in fileDict:
          fileDict[date] = {border:{measure:[int(value), 0]}}
        elif border not in fileDict[date]:
          fileDict[date][border] = {measure:[int(value), 0]}
        elif measure not in fileDict[date][border]:
          fileDict[date][border][measure] = [int(value), 0]
        else:
          fileDict[date][border][measure][0] += int(value)

      # get and sort dates from dictionary
      ascDates = list(fileDict.keys())
      ascDates.sort(key = lambda date: 
                    datetime.strptime(date, "%m/%d/%Y %I:%M:%S %p"))
  except IOError:
    print ("Error: Can not read file")
  except (IndexError, ValueError):
    print ("Error: Inccorect file format")
  finally:
    return (fileDict, ascDates)


def average (dataDict, ascDates, border):
  '''
  Parameters:
  dataDict --> dictionary with the hierarchy of
             {date:{border: {measure: [value, average(default 0]}}}
  ascDate --> list of all the dates in dictionary in ascending order
  border --> string that is either 'US-Canada Border' or 'US-Mexico Border'

  Calculates monthly average for each measure

  Returns dictionary with hierarchy of 
  {date:{border: {measure: [value, average]}}} with updated monthly
  averages
  '''
  
  freqDict = {}

  # filter out dates without this border key
  filteredDate = [date for date in ascDates if border in dataDict[date]]

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
        # round avg
        avg = int(avg+1) if dec>=0.5 else int(avg)
        # update freqdict and avg in dataDict
        freqDict[measure][0]+=1
        freqDict[measure][1] = date
        dataDict[date][border][measure][1] = avg

  return dataDict


def sort(dataDict, date):
  '''
  Parameters:
  dataDict --> dictionary with the hierarchy of
             {date:{border: {measure: [value, average(default 0]}}}
  date --> string of a datatime object in format MM/DD/YYYY HH:MM:SS AM/PM

  sorts the values of the date by value, measure, border in
  descending order

  returns a sorted list of list 
  [[border, date, measure, value, average]...[]] for that date
  '''

  monthSummary= []
  for border in dataDict[date]:
    for measure in dataDict[date][border]:
      summary = [border, date, measure] + dataDict[date][border][measure]
      monthSummary.append(summary)
  
  if len(monthSummary) > 1:
    monthSummary.sort(key = lambda info: (info[3], info[2], info[0]), reverse = True)
  return monthSummary


def writefile (outputFile, dataDict, ascDates):
  '''
  Parameters:
  outputFile --> csv written to output directory
  dataDict --> dictionary with the hierarchy of
             {date:{border: {measure: [value, average(default 0]}}}
  ascDate --> list of all the dates in dictionary in ascending order

  sorts information from dataDict in descending order by date, value, 
  measure, border and outputFile to the output directory
  '''

  with open ("output/"+outputFile, mode ='w') as fw:
    report = csv.writer(fw, delimiter = ',')
    report.writerow (['Border','Date','Measure','Value','Average'])

    for date in ascDates[::-1]:
      monthSummary = sort(dataDict, date)
      for info in monthSummary:
        report.writerow(info)




if __name__ == "__main__":
  writeReport("Border_Crossing_Entry_Data.csv", "report.csv")
