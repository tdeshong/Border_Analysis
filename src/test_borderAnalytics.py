# Python 3.7.4
#!/usr/bin/python
import unittest
import borderAnalytics

class TestBorderAnalytic(unittest.TestCase):

  def test_readFile(self):
    ordinary = main.readFile("Border_Crossing_Entry_Data.csv")
    expected = ({'03/01/2019 12:00:00 AM': {'US-Canada Border': {'Truck Containers Full': [6483, 0], 'Trains': [19, 0]}, 'US-Mexico Border': {'Pedestrians': [346158,0]}}, '02/01/2019 12:00:00 AM': {'US-Mexico Border': {'Pedestrians': [172163, 0]}, 'US-Canada Border': {'Truck Containers Empty': [1319, 0]}}, '01/01/2019 12:00:00 AM': {'US-Mexico Border': {'Pedestrians': [56810, 0]}}},
    ['01/01/2019 12:00:00 AM','02/01/2019 12:00:00 AM','03/01/2019 12:00:00 AM'])

    self.assertEqual(ordinary, expected)
    
    emptyCsv = main.readFile("Empty.csv")
    self.assertEqual(emptyCsv, ({},[]))

    onlyHeader = main.readFile("OnlyHeader.csv")
    self.assertEqual(onlyHeader, ({},[]))

    txtFile = main.readFile("Test1.txt")
    self.assertEqual(txtFile, ({},[]))
  
  def test_average(self):
    dates = ['01/01/2019 12:00:00 AM','02/01/2019 12:00:00 AM','03/01/2019 12:00:00 AM']
    # consecutive month average
    dict1 = {'03/01/2019 12:00:00 AM': {'US-Mexico Border': {'Pedestrians': [346158,0]}}, '02/01/2019 12:00:00 AM': {'US-Mexico Border': {'Pedestrians': [172163, 0]}}, '01/01/2019 12:00:00 AM': {'US-Mexico Border': {'Pedestrians': [56810, 0]}}}

    expected1 = {'03/01/2019 12:00:00 AM': {'US-Mexico Border': {'Pedestrians': [346158,114487]}}, '02/01/2019 12:00:00 AM': {'US-Mexico Border': {'Pedestrians': [172163, 56810]}}, '01/01/2019 12:00:00 AM': {'US-Mexico Border': {'Pedestrians': [56810, 0]}}}

    # month have a value of zero
    dict2 = {'03/01/2019 12:00:00 AM': {'US-Mexico Border': {'Pedestrians': [346158,0]}}, '02/01/2019 12:00:00 AM': {'US-Mexico Border': {'Pedestrians': [172163, 0]}}, '01/01/2019 12:00:00 AM': {'US-Mexico Border': {'Pedestrians': [56810, 0]}}, '04/01/2019 12:00:00 AM': {'US-Mexico Border': {'Pedestrians': [0,0]}}, '05/01/2019 12:00:00 AM': {'US-Mexico Border': {'Pedestrians': [2000,0]}}}

    expected2 = {'03/01/2019 12:00:00 AM': {'US-Mexico Border': {'Pedestrians': [346158,114487]}}, '02/01/2019 12:00:00 AM': {'US-Mexico Border': {'Pedestrians': [172163, 56810]}}, '01/01/2019 12:00:00 AM': {'US-Mexico Border': {'Pedestrians': [56810, 0]}}, '04/01/2019 12:00:00 AM': {'US-Mexico Border': {'Pedestrians': [0,191711]}}, '05/01/2019 12:00:00 AM': {'US-Mexico Border': {'Pedestrians': [2000,143783]}}}

    self.assertDictEqual(main.average(dict1,dates, "US-Mexico Border"), expected1) 

    self.assertDictEqual(main.average(dict2,dates, "US-Mexico Border"), expected2)
  
  def test_sort(self):
    date = '03/01/2019 12:00:00 AM'

    dict1 = {'03/01/2019 12:00:00 AM': {'US-Canada Border': {'Truck Containers Full': [19, 0], 'Trains': [1000, 0]}}}

    expected1 = [['US-Canada Border', '03/01/2019 12:00:00 AM', 'Trains', 1000, 0],['US-Canada Border', '03/01/2019 12:00:00 AM', 'Truck Containers Full', 19, 0], ]


    dict2 = {'03/01/2019 12:00:00 AM': {'US-Canada Border': {'Truck Containers Full': [19, 0], 'Trains': [19, 0]}, 'US-Mexico Border': {'Trains': [19,0]}}} 
    
    expected2 =[['US-Canada Border', '03/01/2019 12:00:00 AM', 'Truck Containers Full', 19, 0], ['US-Mexico Border', '03/01/2019 12:00:00 AM', 'Trains', 19, 0], ['US-Canada Border', '03/01/2019 12:00:00 AM', 'Trains', 19, 0]]

    self.assertEqual(main.sort(dict1, date), expected1)

    self.assertEqual(main.sort(dict2, date), expected2)

    
  

if __name__ == 'main':
  unittest.main()
