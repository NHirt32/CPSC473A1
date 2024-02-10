import userInput as ui
import dataFrameAnalysis as dfa
import output

outputFileName = "ForecastingResult.txt"

inputFileName, period, forecastYears = ui.userInput()

analysisValues, forecastValues = dfa.dataAnalysis(inputFileName, period, forecastYears)

output.printOutput(analysisValues, forecastValues)
output.fileOutput(forecastValues, outputFileName)
