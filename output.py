import os

def printOutput(analysisValues, forecastValues):
    """
    This function prints all forecasted values as well as analysis values

    Args:
        analysisValues (String): The analysis containing slope, intercept, and R^2
        forecastValues (List): List of all forecasted values from our analysis

    """
    print("Forecasted Values:")
    for value in forecastValues:
        print(value)

    print("Analysis Values:")
    print(analysisValues)

def fileOutput(forecastValues, fileName):
    """
    This function saves all forecasted values to the specified file name under the current active directory

    Args:
        forecastValues (List): List of all forecasted values from our analysis
        fileName (str): The name of the file that will be saved
    """
    currentDirectory = os.getcwd()
    filePath = os.path.join(currentDirectory, fileName)

    with open(filePath, "w") as file:
        for value in forecastValues:
            file.write("%s\n" % value)
