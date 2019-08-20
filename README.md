# Border Crossing Analysis
Border Analysis creates a csv report from a csv file with information from the [Bureau of Transportation's](https://data.transportation.gov/Research-and-Statistics/Border-Crossing-Entry-Data/keg4-3bc2) data on the number of vehicles, equipment, passengers and pedestrians crossing into the United Stated by land. The report is comprised of a monthly summary of the amount of vehicles, equipment, passengers and pedestrians that cross into the United States from Mexico or Canada as well as a running monthly average of the total number of crossings from these categories (vehicles, equipment, passengers or pedestrians).

## File Format
The csv file with the information from the Bureau of Transportation must be in the "input" directory. The header of this csv file must be in this order: Port Name, State, Port Code, Border, Date, Measure, Value, Location. 
The date value must be written in either MM/DD/YYYY or M/D/YYYY. The time can be paired with the date but it is not required and if the time is paired with the date, it must be after the date. An "output" directory must be created for the report csv to be written into.

If the input or output directories do not exist or the csv file from the Bureau of Transportation do not follow the above criteria, the report csv will not be created.


## Libraries 
```python
from date time import date time
import csv
import unnittest
```

## Tests
The test_borderAnalysis.py in src directory is the unit test for borderAnalysis.py.
There are 3 test in insight_testsuite/tests: 1) which was the test that was provided, 
2) which test months are sorted correctly and 3) test that a border with multiple recurring measures calculates the correct monthly average 

## Approach

The information read from the csv is put into a nested dictionary with the first key being the date, the second key being the border, the third key being the measure with the value of a list with the zero index being the value(from csv) and 1st index being the average defaulted at zero. {date : {border: {measure : [value, avgerage] }}}
The function that creates this dictionary returns a tuple with the dictionary in the 0th index and a list of sorted dates from the dictionary in ascending order in the 1st index. 

Since finding the running monthly averages and order of the rows written to the file need to be sorted by the date, I decided to sort once in the beginning instead of multiple times throughout.

Once that tuple is create I calculate the monthly average for each measure at each border by filtering the dates that have a border as a key and looping through those dates which are in ascending order to calculate the monthly average.

Then I sort the information from the updated dictionary by date, value, measure border to write to the report.


If the file read is not a csv or not [correctly formatted](#File Format), a report csv will not be created.
