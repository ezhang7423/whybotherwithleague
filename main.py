import data
from bokeh.plotting import figure
from bokeh.io import show
from bokeh.models import Title
from bokeh.plotting import figure, output_file

def scrapeData(stringy):
	scrapedData = []
	for x in range(len(stringy)-1):
		if stringy[x:x+22] == 'date-duration-duration':
			scrapedData.append(stringy[x+71:x+78])
		if stringy[x:x+18] == 'date-duration-date':
			scrapedData.append(stringy[x+66:x+79])
	return scrapedData
   	
def cleanData(scrapedData):
	for index, x in enumerate(scrapedData):
		if x[0:3] == '"">':
			scrapedData[index] = x[3:(len(x))]
		if x[0:2] == '">':
			scrapedData[index] = x[2:(len(x))]
		if x[0] == '>':
			scrapedData[index] = x[1:(len(x))]
	for index, x in enumerate(scrapedData):
		if x[len(x)-5:len(x)] == '</div':
			scrapedData[index] = x[:len(x)-5]
		if x[len(x)-4:len(x)] == '</di':
			scrapedData[index] = x[:len(x)-4]
		if x[len(x)-3:len(x)] == '</d':
			scrapedData[index] = x[:len(x)-3]
		if x[len(x)-2:len(x)] == '</':
			scrapedData[index] = x[:len(x)-2]
		if x[len(x)-1:len(x)] == '<':
			scrapedData[index] = x[:len(x)-1]
	return scrapedData

def checkAcc(dicte):
	totalamt = 0 
	for x in dicte:
		totalamt+=len(dicte[x])
	return totalamt

def createDict(scrapedData):
	dictData = {}
	for x in range(1, len(scrapedData), 2):
		if scrapedData[x] in dictData.keys():
			dictData[scrapedData[x]].append(scrapedData[x-1])
		else:
			dictData[scrapedData[x]] = [scrapedData[x-1]]
	return dictData

def durationToSec(duration):
	temp = duration.split(':')
	for x in range(2):
		temp[x] = int(temp[x])
	temp[0]*=60
	ans = temp[0]+temp[1]
	return ans

def createTimeDict(totalTimeDict):
	for eachDay in totalTimeDict:
		totalTimeOfDay = 0
		for eachGame in totalTimeDict[eachDay]:
			totalTimeOfDay+=durationToSec(eachGame)
		totalTimeDict[eachDay] = totalTimeOfDay
	return totalTimeDict


cleanedData = cleanData(scrapeData(data.stringy)) 



totalTimeDict = createTimeDict(createDict(cleanedData))

amt = 0 
for eachInterval in totalTimeDict:
	amt+=totalTimeDict[eachInterval]
print(amt/3600)

for x in data.valueOf260Days:
	for y in totalTimeDict:
		if x == y:
			data.valueOf260Days[x] = totalTimeDict[y]

print(len(totalTimeDict))

print(len(totalTimeDict)/len(data.valueOf260Days))
totalTimeDict = data.valueOf260Days

dates = []
for x in totalTimeDict:
	dates.append(x)
newDates = []
for x in reversed(dates):
	newDates.append(x)

duration = []
newDuration = []
for x in totalTimeDict:
	duration.append(totalTimeDict[x])
for x in range(len(duration)):
	duration[x]=int(duration[x])/3600


# plot = figure(x_range=dates, title='Time spent playing league', plot_width=875, plot_height=350)
# plot.vbar(x=dates, width=2.5, bottom=0, color='lightgrey', top=duration)
# plot.xaxis.visible = False
# plot.xgrid.grid_line_color = None
# plot.y_range.start = 0
# plot.title.align = 'center'
# plot.title.text_font_size = '25px'
# plot.title.text_font = 'Times New Roman'
# plot.add_layout(Title(text="Date (12/2/2018-8/20/2019)", align="center"), "below")
# plot.add_layout(Title(text="Hours", align="center"), "left")
# show(plot)