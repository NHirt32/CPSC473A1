import pandas as pd

forecastList = []

def dataRead(filePath):
    """
    This function reads in a specified csv file and converts it to a Pandas DataFrame dropping all NaN values

    Args:
        filePath (string): Relative path to csv file
    Returns:
        dfFiscal (DataFrame): Our unprocessed Pandas DataFrame
    """
    dfFiscal = pd.read_csv(filePath)
    dfFiscal.dropna(how='all', inplace=True)
    return dfFiscal

def periodSplit(dfFiscal, period):
    """
    This function splits a given DataFrame converting each set of points in a year to the given period number of points

    Args:
        dfFiscal (DataFrame): DataFrame containing completely unprocessed data from our CSV file
        period (int): Number of divisions required for each year
    Returns:
        dfPeriod(DataFrame): DataFrame where our yearly data has been divided into the specified number of periods
    """
    valueAvg = 0
    rowIndex = 0
    # New DataFrame for processed data storage
    dfPeriod = pd.DataFrame(columns=('Year', 'Value'))

    # Iterating through every row in dfFiscal
    while rowIndex < len(dfFiscal):

        valueAvg += dfFiscal['Value'].iloc[rowIndex]
        aggregateSum = 12 / period

        # Taking the average of every 3 rows to create quarters
        if (rowIndex+1) % aggregateSum == 0:
            dateValues = dfFiscal['Date'].astype(str).iloc[rowIndex]
            dfPeriod.loc[len(dfPeriod.index)] = [dateValues, valueAvg]
            # Resetting used and lent amounts for future quarterly calculations
            valueAvg = 0

        rowIndex += 1
    return dfPeriod

def dataPreprocess(period, inputFile):
    """
    This function is the parent function for data preprocessing and does the following:
    Reads in csv file and translates it to a pandas Dataframe -> Splits the DataFrame based off provided period

    Args:
        period (int): The number of required divisions in each year
        inputFile (String): The name of the input file
    Returns:
        dfPeriod (DataFrame): The DataFrame containing data processed to given period
    """
    dfFiscal = dataRead(inputFile)
    dfPeriod = periodSplit(dfFiscal, period)
    return dfPeriod

def movingAverage(dfPeriod, year, period):
    """
    This function calculates the moving average of our processed DataFrame, appends the year and forecasted value to
    our dataframe, and adds (year,period,avg) to our predicted value list
    Args:
        dfPeriod (DataFrame): Period processed DataFrame
        year (int): The current year of our forecasted value
        period (int): The current period of our forecasted value
    Returns:
        dfPeriod (DataFrame): The DataFrame containing our newly forecasted value
    """
    rowCount = len(dfPeriod)
    sum = 0
    valueList = dfPeriod['Value'].tolist()

    for value in  valueList:
        sum += value

    avg = sum / rowCount
    newRow = {'Year': year, 'Value': avg}
    forecastList.append(f"<{year}, {period}, {avg}>")
    dfPeriod.loc[rowCount] = newRow
    return dfPeriod

def forecast(dfPeriod, forecastYears, period):
    """
        This function forecasts future values of our DataFrame based off the moving average

        Args:
            dfPeriod (DataFrame): DataFrame with values processed to period number
            forecastYears (int): The number of requested years to forecast
            period (int): The number of divisions of each year
        Returns:
            dfFiscal (DataFrame): Our unprocessed Pandas DataFrame
        """
    forecastPeriods = forecastYears * period
    while forecastPeriods > 0:
        currYear = dfPeriod['Year'].iloc[-1]
        yearCount = (dfPeriod['Year'] == currYear).sum()
        if yearCount == period:
            currYear = int(currYear) + 1
            yearCount = 0
        dfPeriod = movingAverage(dfPeriod, currYear, yearCount+1)
        forecastPeriods -= 1

    return dfPeriod

def rSquared(dfPeriod, slope, intercept):
    """
    This function computes our R^2  value for our forecasting

    Args:
        dfPeriod (DataFrame): Pandas dataframe containing financial information parsed to given periods
        slope (float): The slope of our line analysis
        intercept (float): The y intercept of our line analysis
    Returns:
        rSq (float): The r^2 value of our line analysis
    """
    rowCount = len(dfPeriod)
    sum = 0
    valueList = dfPeriod['Value'].tolist()

    for value in valueList:
        sum += value

    avg = sum / rowCount

    totalSumOfSquares = 0

    for value in valueList:
        totalSumOfSquares += (value - avg)**2

    residualSumOfSquares = 0

    for count, value in enumerate(valueList):
        residualSumOfSquares += (value -(slope*count+intercept))**2

    rSq = 1 - (residualSumOfSquares / totalSumOfSquares)
    return rSq

def graphAnalysis(dfPeriod):
    """
    This function analyzes a given dataframe calculating its slope and intercept as well as acquiring the r^2 value
    from the corresponding function. It then creates a string concisely containing relevant information

    Args:
        dfPeriod (DataFrame): DataFrame with values processed to period number
    Returns:
        analysisOutput (str): The string containing slope, intercept, and r^2 value
    """
    rise = dfPeriod['Value'].iloc[-1] - dfPeriod['Value'].iloc[0]
    run = len(dfPeriod) - 1
    slope = rise/run
    intercept = dfPeriod['Value'].iloc[0] - slope
    rSq = rSquared(dfPeriod, slope, intercept)
    analysisOutput = f"<{slope}, {intercept}, {rSq}>"
    return analysisOutput

def dataAnalysis(inputFile, period, forecastYears):
    """
    This function is the overarching function for our data analysis which does the following:
    Calculates periodic values based on given period -> Forecasts years based off given forecastYears + period ->
    -> Analyzes our graph post forecasting to find critical value such as R^2, Intercept, Slope, etc..

    Args:
        inputFile (String): The name of the input file 
        period (int): The number of divisions for each year in our financial data
        forecastYears (int): The number of years we wish to forecast off known data
    Returns:
        tuple: The tuple of both our analysis values and all forecasted values
    """
    if 12 % period == 0:
        dfPeriod = dataPreprocess(period, inputFile)
        forecast(dfPeriod, forecastYears, period)
        analysisValues = graphAnalysis(dfPeriod)
    else:
        print("Invalid period (Indivisible)")
        exit(1)

    return analysisValues, forecastList

