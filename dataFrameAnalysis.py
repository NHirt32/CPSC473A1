import pandas as pd

forecastList = []

def dataRead():
    dfFiscal = pd.read_csv('CPSC473A1Dataset.csv')
    dfFiscal.dropna(how='all', inplace=True)
    return dfFiscal

def periodSplit(dfFiscal, period):
    valueAvg = 0
    rowIndex = 0
    dfPeriod = pd.DataFrame(columns=('Year', 'Value'))

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

def dataPreprocess(period):
    dfFiscal = dataRead()
    dfPeriod = periodSplit(dfFiscal, period)
    return dfPeriod

def movingAverage(dfPeriod, year, period):
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
    rowCount = len(dfPeriod)
    sum = 0
    valueList = dfPeriod['Value'].tolist()

    for value in valueList:
        sum += value

    avg = sum / rowCount

    sumOfSquares = 0

    for value in valueList:
        sumOfSquares += (value - avg)**2

    

def graphAnalysis(dfPeriod):
    rise = dfPeriod['Value'].iloc[-1] - dfPeriod['Value'].iloc[0]
    run = len(dfPeriod) - 1
    slope = rise/run
    intercept = dfPeriod['Value'].iloc[0] - slope
    print(intercept)
    return 0

def dataAnalysis(period, forecastYears):
    if 12 % period == 0:
        dfPeriod = dataPreprocess(period)
        forecast(dfPeriod, forecastYears, period)
        graphAnalysis(dfPeriod)
        print(forecastList)
    else:
        print("Invalid period (Indivisible)")
        exit(1)

    return forecastList

