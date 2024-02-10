#CPSC 473 A1

##Description:
This Python project's goal is to take in a CSV file, utilize moving average to forecast trends, and analyze core graph features.

##Requirements
This project requires an installation of Python as well as Pandas.

##Usage:
Navigate to your local folder that contains the project files and run the following command:
python main.py CSVFILENAME.csv PERIOD(int) FORECASTYEARS(int)
Please note that your CSV files first column needs to be named 'Date' and the second value needs to be named 'Value' with corresponding values in their appropriate columns.
Additionally, your 'Date' column needs to be appropriately divided into a monthly basis where each entry is simply referred to by the year it is in.
The program will divide these up such that each period is appropriately divided.
Below you can see an example of what columns should look like in your file for an individual year:
Date, Value
2019,41
2019,42
2019,41
2019,45
2019,40
2019,47
2019,48
2019,45
2019,43
2019,41
2019,48
2019,50

##File Structure:
###main.py:
This file contains calls to all seperated functionality and contains the setting of the output file's name

###userInput.py:
This file has a singular function that analyzes user input from a terminal call and passes these forward to the rest of the program.

###dataFrameAnalysis.py:
This file is composed of many different functions and is responsible for all forecasting and regression. The entry point to this functionality is the dataAnalysis function.

###output.py:
This file contains two functions which both print our forecasting and analysis results to the user as well as saves the forecasted predictions to a txt file.
