import pygame
import pandas as pd
import numpy as np 
import random
import math

def displayGame(screenWidth, screenHeight, caption):
	pygame.init()
	game = pygame.display.set_mode((screenWidth, screenHeight))
	pygame.display.set_caption(caption)
	return game

def drawLines(game, backgroundColor, lineColor, lineWidth, listOfPoints):
	game.fill(WHITE)
	pygame.draw.lines(game, lineColor, False, listOfPoints, lineWidth)
	return game



length = 250
carHeight = 150

duplicateFrameforEachState = 10
totalState = 20
totalFrame = duplicateFrameforEachState * totalState





############# initialized values

screenWidth = 1000
screenHeight = 750
FPS = 60

upperboundOfTimeInterval = 6000 #seconds 
lowerboundOfTimeInterval = 2500
requiredTimeFromEnd = 1500
probeExtendTime = 215

missTolerenceTime = 1250 


######### random df
x1 = [val for val in random.sample(range(250, screenWidth), totalState) for _ in range(duplicateFrameforEachState)]
y1 = [val for val in random.sample(range(0, int(screenHeight/2)), totalState) for _ in range(duplicateFrameforEachState)]

x3 = [val for val in random.sample(range(250, screenWidth), totalState) for _ in range(duplicateFrameforEachState)]
y3_rand = list()
for i in range(totalState):
	up = y1[i]+length
	low = y1[i]
	y3_rand.append(random.sample(range(low, up), 1)[0])

y3 = [val for val in y3_rand for _ in range(duplicateFrameforEachState)]


x5 = [val for val in random.sample(range(250, screenWidth), totalState) for _ in range(duplicateFrameforEachState)]
y5_rand = list()

for i in range(totalState):
	up = y3[i]+length
	low = y3[i]
	y5_rand.append(random.sample(range(low, up), 1)[0])
y5 = [val for val in y5_rand for _ in range(duplicateFrameforEachState)]


x6 = x5
y6 = [y + carHeight for y in y5]

x2 = [int((a+b)/2) for a,b in zip(x1,x3)]
y2 = [int((a+b)/2) for a,b in zip(y1,y3)]

x4 = [int((a+b)/2) for a,b in zip(x3,x5)]
y4 = [int((a+b)/2) for a,b in zip(y3,y5)]



points = {"point1": list(zip(x1, y1)), "point2" : list(zip(x2, y2)), "point3" : list(zip(x3, y3)), 
"point4": list(zip(x4, y4)), "point5" : list(zip(x5, y5)), "point6" : list(zip(x6, y6))}
pointsDf = pd.DataFrame.from_dict(points)

############################################################################################################



#########################################################################

class ProbeList:
	def __init__(self, FPS, upperboundOfTimeInterval, lowerboundOfTimeInterval, requiredTimeFromEnd):
		self.FPS = FPS
		self.upperboundOfFrameInterval = int(upperboundOfTimeInterval* FPS/1000 ) #frames
		self.lowerboundOfFrameInterval = int(lowerboundOfTimeInterval* FPS/1000 )
		self.requiredFrameFromEnd = int(requiredTimeFromEnd* FPS/1000 )

	def __call__(self, pointsDf):
		probeList = list()
		currentProbeFrame = random.sample(range(self.lowerboundOfFrameInterval, self.upperboundOfFrameInterval),1)[0]
		probeList.append(currentProbeFrame)
		while((currentProbeFrame + self.requiredFrameFromEnd + self.lowerboundOfFrameInterval) <= len(pointsDf.index)):
			oldProbeFrame = currentProbeFrame
			currentProbeFrame = random.sample(range(oldProbeFrame + self.lowerboundOfFrameInterval, oldProbeFrame + self.upperboundOfFrameInterval),1)[0]
			if(currentProbeFrame + self.requiredFrameFromEnd >= len(pointsDf.index)):
				break
		probeList.append(currentProbeFrame)
		return probeList

class ExperimentAndDataLists:
	def __init__(self, screenWidth, screenHeight, caption, FPS, probeExtendTime, missTolerenceTime, lineColor, lineWidth,
		backgroundColor, probeColor, probeWidth, displayFunction, drawLinesFunction):

		self.screenWidth = screenWidth
		self.screenHeight = screenHeight
		self.caption = caption

		self.FPS = FPS
		self.probeExtendFrame = int(probeExtendTime * FPS/1000)
		self.missTolerenceFrame = int(missTolerenceTime * FPS/1000)
		self.lineColor = lineColor
		self.lineWidth = lineWidth
		self.probeColor = probeColor
		self.probeWidth = probeWidth

		self.backgroundColor = backgroundColor

		self.displayGame = displayFunction
		self.drawLines = drawLinesFunction

	def __call__(self, pointsDf, probeList):
		# pygame.init()
		# game = pygame.display.set_mode((self.screenWidth, self.screenHeight))
		# pygame.display.set_caption(caption)
		game = displayGame(self.screenWidth, self.screenHeight, self.caption)

		fpsClock = pygame.time.Clock()

		probeNumberList = list()
		probeShownTimeList = list()
		pressTimeList = list()
		probeLocationList = list()
		pressSuccessList = list()

		probeShownIndex = 0
		probeShownFrame = 0
		probeNumber = 0

		keyPressed = False
		alreadySucceed = False



#
		for currentFrame in range(len(pointsDf.index)):
			fpsClock.tick(self.FPS)
			pointList = list(pointsDf.iloc[currentFrame])
			game = drawLines(game, self.backgroundColor, self.lineColor, self.lineWidth, pointList)
			print(pointList)
			# game.fill(WHITE)
			# pygame.draw.lines(game, self.lineColor, False, list(pointsDf.iloc[currentFrame]), self.lineWidth)

			if currentFrame in probeList:
				probeShownIndex = 1
				probeIndex = random.sample(range(len(pointsDf.columns)),1)[0]

				probeCoordinates = [pointsDf.iloc[(currentFrame, probeIndex)][0], pointsDf.iloc[(currentFrame, probeIndex)][1]]
				pygame.draw.circle(game, self.probeColor, probeCoordinates, self.probeWidth)

				probeTime = pygame.time.get_ticks()

				probeShownFrame = currentFrame
				probeNumber +=1

				keyPressed = False
				alreadySucceed = False

			if probeShownIndex != 0:
				probeCoordinates = [pointsDf.iloc[(currentFrame, probeIndex)][0], pointsDf.iloc[(currentFrame, probeIndex)][1]]
				pygame.draw.circle(game, self.probeColor, probeCoordinates, self.probeWidth)
				probeShownIndex += 1

			if probeShownIndex == self.probeExtendFrame + 1:
				probeShownIndex = 0

#

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.KEYDOWN:

					if (event.key == pygame.K_SPACE) & (probeShownFrame !=0):
						pressTime = pygame.time.get_ticks()
						pressTimeList.append(pressTime)
						probeShownTimeList.append(probeTime)
						probeLocationList.append(probeIndex)
						probeNumberList.append(probeNumber)


						keyPressed = True
						if (currentFrame - probeShownFrame < self.missTolerenceFrame) & (alreadySucceed == False):
							pressSuccessList.append("Success")
							alreadySucceed = True
						else:
							pressSuccessList.append("FalseAlarm")

			if (currentFrame == probeShownFrame + self.missTolerenceFrame) & (probeShownFrame !=0):
				if(keyPressed == False):
					probeShownTimeList.append(probeTime)
					probeLocationList.append(probeIndex)
					probeNumberList.append(probeNumber)
					pressTimeList.append(0)
					pressSuccessList.append("TimeOut")


			pygame.display.update()



		return {'probeNumberList': probeNumberList, 'probeLocationList': probeLocationList,
		'probeShownTimeList': probeShownTimeList, 'pressTimeList': pressTimeList, 'pressSuccessList' : pressSuccessList}



BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)

lineColor = BLACK
lineWidth = 3
probeColor = BLUE
probeWidth = 5

backgroundColor = WHITE
caption = "Double Pendulum Experiment"


getProbeList = ProbeList(FPS, upperboundOfTimeInterval, lowerboundOfTimeInterval, requiredTimeFromEnd)
probeFrameList = getProbeList(pointsDf)


probeFrameList = [40, 90, 150]
missTolerenceTime = 300


runExperimentAndGetData = ExperimentAndDataLists(screenWidth, screenHeight, caption, FPS, probeExtendTime, missTolerenceTime, 
	lineColor, lineWidth, backgroundColor, probeColor, probeWidth, displayGame, drawLines)

resultDictionary = runExperimentAndGetData(pointsDf, probeFrameList)

print(resultDictionary)



