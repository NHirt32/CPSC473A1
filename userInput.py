import sys

def userInput():
    """
    This function analyzes user input from a terminal call and passes forward parameters to the rest of the function

    Returns:
        tuple: The tuple of the csv file input name, the period for yearly division, and the number of years to be forecasted
    """

    if len(sys.argv) != 4:
        print('Incorrect number of arguments (Should be 3)')
        sys.exit(1)
    inputFileName = sys.argv[1]
    period = int(sys.argv[2])
    forecastingYears = int(sys.argv[3])
    return inputFileName, period, forecastingYears