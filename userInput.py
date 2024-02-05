import sys

def userInput():
    if sys.argv != 3:
        print('Incorrect number of arguments (Should be 2)')
        sys.exit(1)
    period = sys.argv[1]
    forecastingYears = sys.argv[2]
    return period, forecastingYears