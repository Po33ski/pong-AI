# Building the Environment

# Importing the libraries
import os
import numpy as np
import pygame as pg
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# Initializing the Environment class
class Environment():
    
    def __init__(self, waitTime):
        
        self.width = 880            # width of the game window
        self.height = 880           # height of the game window
        self.nRows = 16             # number of rows in our board
        self.nColumns = 16         # number of columns in our board
        self.lenPlatform = 3       # initial length of the platform
        self.defReward = -0.03      # reward for taking an action - The Living Penalty
        self.negReward = -1.        # reward for loosing a point
        self.posReward = 2.         # reward for collecting an apple
        self.waitTime = waitTime    # slowdown after taking an action
        self.gotPoint = False
        
        self.screen = pg.display.set_mode((self.width, self.height))
        self.platformPos = list()
        self.platformPos2 = list()
        
        
        # Creating the array that contains mathematical representation of the game's board
        self.screenMap = np.zeros((self.nRows, self.nColumns))

        for i in range(self.lenPlatform):
            self.platformPos.append([ self.nRows-1, int(self.nColumns / 2) + i])
            self.screenMap[self.nRows - 1][int(self.nColumns / 2) + i] = 0.5

            self.platformPos2.append([ 0, int(self.nColumns / 2) + i])
            self.screenMap[0][int(self.nColumns / 2) + i] = 2.


        
        self.directionSet = ("down", "up", "leftUp", "rightUp", "leftDown", "rightDown")
        self.ballDirection = "down"
            
        self.ballPos = self.placeBall()
        
        self.drawScreen()
        
        self.lastMove = 0
        self.gotPoint = False
    # Building a method that gets new, random position of the ball
    def placeBall(self):
        posx = int(self.nColumns/2)-1
        posy = int(self.nRows / 2)-1

        self.ballDirection = self.directionSet[np.random.randint(0,2)]
        self.screenMap[posy][posx] = 1
        
        return [posy, posx]
    
        

    # Making a function that draws everything for us to see
    def drawScreen(self):
        
        self.screen.fill((0, 0, 0))
        
        cellWidth = self.width / self.nColumns
        cellHeight = self.height / self.nRows
        
        for i in range(self.nRows):
            for j in range(self.nColumns):
                if self.screenMap[i][j] == 0.5:
                    pg.draw.rect(self.screen, (255, 255, 255), (j*cellWidth + 1, i*cellHeight + 1, cellWidth - 2, cellHeight - 2))
                elif self.screenMap[i][j] == 2:
                    pg.draw.rect(self.screen, (255, 255, 255), (j*cellWidth + 1, i*cellHeight + 1, cellWidth - 2, cellHeight - 2))
                elif self.screenMap[i][j] == 1:
                    pg.draw.rect(self.screen, (255, 0, 0), (j*cellWidth + 1, i*cellHeight + 1, cellWidth - 2, cellHeight - 2))
                    
        pg.display.flip()
    
    # A method that updates the platform's position
    def movePlatform(self, nextMove, whatPlatform):
        
        if whatPlatform == 1:
            if nextMove == "left":
                nextPos = [self.nRows - 1, self.platformPos[0][1] - 1]
                self.platformPos.insert(0, nextPos)
                self.platformPos.pop(len(self.platformPos)-1)
                print("left: ", self.platformPos)
            elif nextMove == "right":
                nextPos = [self.nRows -1, self.platformPos[2][1] + 1]
                self.platformPos.append(nextPos)
                self.platformPos.pop(0)
                print("right: ", self.platformPos)
        else:
            if nextMove == "left":
                nextPos = [0, self.platformPos2[0][1] - 1]
                self.platformPos2.insert(0, nextPos)
                self.platformPos2.pop(len(self.platformPos2)-1)
                print("left2: ", self.platformPos2)
            elif nextMove == "right":
                nextPos = [0, self.platformPos2[2][1] + 1]
                self.platformPos2.append(nextPos)
                self.platformPos2.pop(0)
                print("right2: ", self.platformPos2)
        self.screenMap = np.zeros((self.nRows, self.nColumns))   
        for i in range(self.lenPlatform):
            self.screenMap[self.platformPos[i][0]][self.platformPos[i][1]] = 0.5
            self.screenMap[self.platformPos2[i][0]][self.platformPos2[i][1]] = 2.


    

    def bounceBall(self, whatPlatform):
        if whatPlatform == 1:
            if self.platformPos[0][1] == 0:
                self.ballDirection = self.directionSet[3]
            elif self.platformPos[0][1]  == 10:
                self.ballDirection = self.directionSet[2]
            else:
                self.ballDirection = self.directionSet[np.random.randint(1,4)]
        else:
            if self.platformPos2[0][1] == 0:
                self.ballDirection = self.directionSet[5]
            elif self.platformPos2[0][1]  == 10:
                self.ballDirection = self.directionSet[4]
            else:
                self.ballDirection = self.directionSet[np.random.randint(4,6)]
        

    def moveBall(self):
        if self.ballPos[0] < self.nRows and self.ballPos[0] >= 0:
            print(self.ballPos)
            if self.ballDirection == "down":
                self.ballPos[0] += 1 # y+1
                print(self.ballPos)
            elif self.ballDirection == "up":
                self.ballPos[0] -= 1 # y-1
                print(self.ballPos)
            elif self.ballDirection == "leftUp":
                self.ballPos[0] -= 1 # y-1
                self.ballPos[1] -= 1 # x-1
                print(self.ballPos)
            elif self.ballDirection == "rightUp":
                self.ballPos[0] -= 1 # y-1
                self.ballPos[1] += 1 # x+1
                print(self.ballPos)
            elif self.ballDirection == "leftDown":
                self.ballPos[0] += 1 # y+1
                self.ballPos[1] -= 1 # x-1
                print(self.ballPos)
            elif self.ballDirection == "rightDown":
                self.ballPos[0] += 1 # y+1
                self.ballPos[1] += 1 # x+1
            

    # The main method that updates the environment
    def step(self, action):
        # action = 0 -> stay
        # action = 1 -> left for platform 1
        # action = 2 -> right for platform 1
        # action = 3 -> left for platform 2
        # action = 4 -> right for platform 2
        
        # Resetting these parameters and setting the reward to the living penalty
        gameOver = False
        reward = self.defReward
        
        ballY = self.ballPos[0]
        ballX = self.ballPos[1]
        
        self.gotPoint = False
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        
        def actionMove (ballX, ballY):
            gameOver = False
            reward = 0
            if ballY == self.nRows - 2 and self.ballDirection == "down":
                if self.screenMap[ballY+1][ballX] != 0.5:
                    gameOver = True
                    reward = self.negReward
                elif self.screenMap[ballY+1][ballX] == 0.5:
                    reward = self.posReward
                    #points += 1
                    self.gotPoint = True
                    self.bounceBall(1)

            elif ballY == self.nRows - 2 and self.ballDirection == "leftDown":
                if self.screenMap[ballY+1][ballX-1] != 0.5:
                    gameOver = True
                    reward = self.negReward
                elif self.screenMap[ballY+1][ballX-1] == 0.5:
                    reward = self.posReward
                    #points += 1
                    self.gotPoint = True
                    self.bounceBall(1)

            elif ballY == self.nRows - 2 and self.ballDirection == "rightDown":
                if self.screenMap[ballY+1][ballX+1] != 0.5:
                    gameOver = True
                    reward = self.negReward
                elif self.screenMap[ballY+1][ballX+1] == 0.5:
                    reward = self.posReward
                    #points += 1
                    self.gotPoint = True
                    self.bounceBall(1) 

            # actions for platform 2:
            elif ballY == 1 and self.ballDirection == "up":
                if self.screenMap[ballY-1][ballX] != 2:
                    gameOver = True
                    reward = self.negReward
                elif self.screenMap[ballY-1][ballX] == 2:
                    reward = self.posReward
                    #points += 1
                    self.gotPoint = True
                    self.bounceBall(2)

            elif ballY == 1 and self.ballDirection == "leftUp":
                if self.screenMap[ballY-1][ballX-1] != 2:
                    gameOver = True
                    reward = self.negReward
                elif self.screenMap[ballY-1][ballX-1] == 2:
                    reward = self.posReward
                    #points += 1
                    self.gotPoint = True
                    self.bounceBall(2)

            elif ballY == 1 and self.ballDirection == "rightUp":
                if self.screenMap[ballY-1][ballX+1] != 2:
                    gameOver = True
                    reward = self.negReward
                elif self.screenMap[ballY-1][ballX+1] == 2:
                    reward = self.posReward
                    #points += 1
                    self.gotPoint = True
                    self.bounceBall(2) 
            return gameOver, reward

        # Checking what happens when we take this action
        if action == 0:
            gameOver, reward = actionMove(ballX, ballY)
        elif action == 1:
            if self.platformPos[0][1] > 0:
                self.movePlatform("left", 1)
            gameOver, reward = actionMove(ballX, ballY)
                
        elif action == 2:
            if self.platformPos[2][1] < self.nRows - 1:
                self.movePlatform("right", 1)
            gameOver, reward = actionMove(ballX, ballY)
        elif action == 3:
            if self.platformPos2[0][1] > 0:
                self.movePlatform("left", 2)
            gameOver, reward = actionMove(ballX, ballY)
                
        elif action == 4:
            if self.platformPos2[2][1] < self.nRows - 1:
                self.movePlatform("right", 2)
            gameOver, reward = actionMove(ballX, ballY)
        else:
               gameOver = True
               reward = self.negReward
        
        if ballY < self.nRows - 2 and ballY > 0:
            if ballX == self.nColumns - 1:
                if self.ballDirection == "rightUp":
                    self.ballDirection = self.directionSet[2]
                if self.ballDirection == "rightDown":
                    self.ballDirection = self.directionSet[4]
            elif ballX == 0:
                if self.ballDirection == "leftUp":
                    self.ballDirection = self.directionSet[3]
                if self.ballDirection == "leftDown":
                    self.ballDirection = self.directionSet[5]

        self.screenMap[ballY][ballX] = 0
        self.moveBall()
        ballY = self.ballPos[0]
        ballX = self.ballPos[1]
        self.screenMap[ballY][ballX] = 1
        # Drawing the screen, updating last move and waiting the wait time specified
        self.drawScreen()
        
        self.lastMove = action
        
        pg.time.wait(self.waitTime)
        
        # Returning the new frame of the game, the reward obtained and whether the game has ended or not
        return self.screenMap, reward, gameOver
    
    # Making a function that resets the environment
    def reset(self):
        self.screenMap  = np.zeros((self.nRows, self.nColumns))
        self.platformPos = list()
        self.platformPos2 = list()
        self.ballPos = self.placeBall()

        for i in range(self.lenPlatform):
            self.platformPos.append([self.nRows - 1, int(self.nColumns / 2) + i])
            self.screenMap[self.nRows - 1][int(self.nColumns / 2) + i] = 0.5
            self.platformPos2.append([ 0, int(self.nColumns / 2) + i])
            self.screenMap[0][int(self.nColumns / 2) + i] = 2.
        
        self.lastMove = 0

