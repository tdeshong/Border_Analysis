# Border Crossing Analysis
Border Analysis creates a csv report from a csv file with information from the [Bureau of Transportation's](https://data.transportation.gov/Research-and-Statistics/Border-Crossing-Entry-Data/keg4-3bc2) data on the number of vehicles, equipment, passengers and pedestrians crossing into the United Stated by land. The report is comprised of a monthly summary of the amount of vehicles, equipment, passengers and pedestrians that cross into the United States from Mexico or Canada as well as a running monthly average of the total number of crossings from these categories (vehicles, equipment, passengers or pedestrians).

## File format
The csv file with the information from the Bureau of Transportation must be in the "input" directory. The header of this csv file must be in this order: Port Name, State, Port Code, Border, Date, Measure, Value, Location. 
The date value must be written in either MM/DD/YYYY or M/D/YYYY. The time can be paired with the date but it is not required and if the time is paired with the date, it must be after the date. An "output" directory must be created for the report csv to be written into.

If the input or output directories do not exist or the csv file from the Bureau of Transportation do not follow the above criteria, the report csv will not be created.


## Libraries 
```python
from date time import date time
import csv
import unnittest



