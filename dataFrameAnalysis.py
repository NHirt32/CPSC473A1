import pandas as pd

quarter_dict = {'Mar': 'Q1', 'Jun': 'Q2', 'Sep': 'Q3', 'Dec': 'Q4'}

def dataRead():
    dfFiscal = pd.read_csv('CPSC473A1Dataset.csv')
    dfFiscal.dropna(how='all', inplace=True)
    return dfFiscal

def quarterAnalysis(dfFiscal):
    usedAvg = 0
    lentAvg = 0
    rowIndex = 0
    dfQuarter = pd.DataFrame(columns=('Quarter + Year', 'Amount_Used', 'Amount_Lent'))

    while rowIndex < len(dfFiscal):

        usedAvg += dfFiscal['Amount_Used'].iloc[rowIndex]
        lentAvg += dfFiscal['Amount_Lent'].iloc[rowIndex]

        # Taking the average of every 3 rows to create quarters
        if (rowIndex+1) % 3 == 0:
            dateValues = dfFiscal['Date'].astype(str).iloc[rowIndex]
            currentQuarter = quarter_dict[f"{dateValues[0]}{dateValues[1]}{dateValues[2]}"]
            currentYear = f"{dateValues[4]}{dateValues[5]}"
            quarterYear = f"{currentQuarter}-{currentYear}"

            dfQuarter.loc[len(dfQuarter.index)] = [quarterYear, usedAvg, lentAvg]
            # Resetting used and lent amounts for future quarterly calculations
            usedAvg = 0
            lentAvg = 0

        rowIndex += 1

    return dfQuarter

def dataPreprocess():
    dfFiscal = dataRead()
    dfQuarter = quarterAnalysis(dfFiscal)
    return dfFiscal

def movingAverage(dfQuarter):
    rowCount = len(dfQuarter)
    currRow = 0
    totalUsed = 0
    totalLent = 0

    while currRow < rowCount:
        totalUsed += dfQuarter['Amount_Used'].iloc[currRow]
        totalLent += dfQuarter['Amount_Lent'].iloc[currRow]
        currRow += 1

    avgUsed = totalUsed / rowCount
    avgLent = totalLent / rowCount

    return avgUsed, avgLent

def dataAnalysis():
    dfQuarter = dataPreprocess()
    avgUsed, avgLent = movingAverage(dfQuarter)

    return avgUsed, avgLent

