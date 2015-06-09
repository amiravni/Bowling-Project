class NewGame():
    
    def __init__(self,numOfPlayers=0):
        self.numOfPlayers = numOfPlayers        
        self.initScoreSheet()
        self.firstShot = True
        self.gameEnded = False
        self.nextToBowlPlayerId = 0
        self.nextToBowlFrame = 1
        self.nextToBowlPlayerName = self.scoreSheet[0]['NAME']
        
    def initScoreSheet(self):
        self.scoreSheet = []          
        for i in range(self.numOfPlayers):
            playerName = 'player'+str(i)            
            self.scoreSheet.append({'ID' : i,
                                    'NAME' : playerName,
                                    1 : [None,None,None],
                                    2 : [None,None,None],
                                    3 : [None,None,None],
                                    4 : [None,None,None],
                                    5 : [None,None,None],
                                    6 : [None,None,None],
                                    7 : [None,None,None],
                                    8 : [None,None,None],
                                    9 : [None,None,None],
                                    10: [None,None,None],
                                    11: [None,None,None],
                                    12: [None,None,None],
                                    'CURRENT_GAME_TOTAL' : 0
                                    })
    
    def receiveFrameScore(self,playerID,currentFrame,shotCount,pinCount):
        for playerListIndex,player in enumerate(self.scoreSheet):
            if playerID == player['ID']:
                if shotCount == 1:                                      
                    self.scoreSheet[playerListIndex][currentFrame][0] = pinCount
                elif shotCount == 2:
                    self.scoreSheet[playerListIndex][currentFrame][1] = pinCount
                self.calcScore(playerID,currentFrame) 

    def calcScore(self,playerID,currentFrame):
        for playerListIndex,player in enumerate(self.scoreSheet):
            if playerID == player['ID']:
                firstShotCount = self.scoreSheet[playerListIndex][currentFrame][0]
                secondShotCount = self.scoreSheet[playerListIndex][currentFrame][1]                
                #print 'first and second: ',firstShotCount,secondShotCount
                #print self.scoreSheet
                if secondShotCount is None:
                    frameTotal = int(firstShotCount)
                else:
                    frameTotal = int(firstShotCount) + int(secondShotCount)               
                
                if currentFrame == 1:
                    self.scoreSheet[playerListIndex][currentFrame][2] = frameTotal
                    
                elif currentFrame == 2:
                    print int(self.scoreSheet[playerListIndex][1][0])                  
                    if self.strike(int(self.scoreSheet[playerListIndex][1][0])):
                        self.scoreSheet[playerListIndex][1][2] = 10 + frameTotal
                    elif self.spare(int(self.scoreSheet[playerListIndex][1][0]),
                                     int(self.scoreSheet[playerListIndex][1][1])):
                            self.scoreSheet[playerListIndex][1][2] = 10 + firstShotCount                            
    
                    self.scoreSheet[playerListIndex][currentFrame][2] = frameTotal 
                else:
                    if self.strike(self.scoreSheet[playerListIndex][currentFrame - 1][0]):
                        self.scoreSheet[playerListIndex][currentFrame - 1][2] = 10 + frameTotal                       
                    elif self.spare(int(self.scoreSheet[playerListIndex][currentFrame - 1][0]),
                                     int(self.scoreSheet[playerListIndex][currentFrame - 1][1])):
                            self.scoreSheet[playerListIndex][currentFrame - 1][2] = 10 + firstShotCount
                    if self.strike(int(self.scoreSheet[playerListIndex][currentFrame - 2][0])) \
                       and self.strike(int(self.scoreSheet[playerListIndex][currentFrame - 1][0])):
                            self.scoreSheet[playerListIndex][currentFrame - 2][2] = 20 + firstShotCount
                                             
                    self.scoreSheet[playerListIndex][currentFrame][2] = frameTotal
                
                self.calcGameTotal(playerListIndex)
                
    def calcGameTotal(self,playerListIndex):
        gameTotal = 0
        for frame in range(10):
            if self.scoreSheet[playerListIndex][frame+1][2] is None:
                continue
            else:
                gameTotal += int(self.scoreSheet[playerListIndex][frame+1][2])
        
        self.scoreSheet[playerListIndex]['CURRENT_GAME_TOTAL'] = gameTotal
    
    def calcGameTotalUpToFrame(self,playerListIndex,upToFrame):
        gameTotalUpToFrame = 0
        for frame in range(upToFrame):
            if self.scoreSheet[playerListIndex][frame+1][2] is None:
                continue
            else:
                gameTotalUpToFrame += int(self.scoreSheet[playerListIndex][frame+1][2])
        return gameTotalUpToFrame
        
    def strike(self,pinCount):
        if pinCount is None:
            return False

        if pinCount == 10:
            return True
        
        return False

    def spare(self,firstShotCount,secondShotCount):
        if secondShotCount is None or firstShotCount is None:
            return False

        if (firstShotCount + secondShotCount) == 10:
            return True
        
        return False
                  
    def addNewPlayer(self,playerName):
        self.scoreSheet.append({'ID' : self.numOfPlayers,
                                    'NAME' : playerName,
                                    1 : [None,None,None],
                                    2 : [None,None,None],
                                    3 : [None,None,None],
                                    4 : [None,None,None],
                                    5 : [None,None,None],
                                    6 : [None,None,None],
                                    7 : [None,None,None],
                                    8 : [None,None,None],
                                    9 : [None,None,None],
                                    10: [None,None,None],
                                    11: [None,None,None],
                                    12: [None,None,None],
                                    'CURRENT_GAME_TOTAL' : 0
                                    })
        self.numOfPlayers +=1
    
    def printScoreSheet(self):
        for i,player in enumerate(self.scoreSheet):
            print player['NAME']            
            print '___________________________________________________________________________________'
            print '|   1   |   2   |   3   |   4   |   5   |   6   |   7   |   8   |   9   |   10    |'
            print '-----------------------------------------------------------------------------------'
            print '|',' ' if player[1][0] is None else player[1][0],' ',' ' if player[1][1] is None else player[1][1],\
                  '|',' ' if player[2][0] is None else player[2][0],' ',' ' if player[2][1] is None else player[2][1],\
                  '|',' ' if player[3][0] is None else player[3][0],' ',' ' if player[3][1] is None else player[3][1],\
                  '|',' ' if player[4][0] is None else player[4][0],' ',' ' if player[4][1] is None else player[4][1],\
                  '|',' ' if player[5][0] is None else player[5][0],' ',' ' if player[5][1] is None else player[5][1],\
                  '|',' ' if player[6][0] is None else player[6][0],' ',' ' if player[6][1] is None else player[6][1],\
                  '|',' ' if player[7][0] is None else player[7][0],' ',' ' if player[7][1] is None else player[7][1],\
                  '|',' ' if player[8][0] is None else player[8][0],' ',' ' if player[8][1] is None else player[8][1],\
                  '|',' ' if player[9][0] is None else player[9][0],' ',' ' if player[9][1] is None else player[9][1],\
                  '|',' ' if player[10][0] is None else player[10][0],' ',' ' if player[10][1] is None else player[10][1],\
                  '|',' ' if player[11][0] is None else player[11][0],' ',' ' if player[11][1] is None else player[11][1],\
                  '|',' ' if player[12][0] is None else player[12][0],' ',' ' if player[12][1] is None else player[12][1],'|'
            print '-----------------------------------------------------------------------------------'
            print '|',' ' if player[1][2] is None else self.calcGameTotalUpToFrame(i,1),\
                  '|',' ' if player[2][2] is None else self.calcGameTotalUpToFrame(i,2),\
                  '|',' ' if player[3][2] is None else self.calcGameTotalUpToFrame(i,3),\
                  '|',' ' if player[4][2] is None else self.calcGameTotalUpToFrame(i,4),\
                  '|',' ' if player[5][2] is None else self.calcGameTotalUpToFrame(i,5),\
                  '|',' ' if player[6][2] is None else self.calcGameTotalUpToFrame(i,6),\
                  '|',' ' if player[7][2] is None else self.calcGameTotalUpToFrame(i,7),\
                  '|',' ' if player[8][2] is None else self.calcGameTotalUpToFrame(i,8),\
                  '|',' ' if player[9][2] is None else self.calcGameTotalUpToFrame(i,9),\
                  '|',' ' if player[10][2] is None else self.calcGameTotalUpToFrame(i,10),'|',player['CURRENT_GAME_TOTAL']
                  
    
    def helpScreen(self):
        command = ''   
        while not command == 'q':
            text = '---->'        
            command = raw_input(text)
            if command == 'a':
                text = 'Enter New player Name:'        
                playerName = raw_input(text)               
                self.addNewPlayer(playerName)
                self.printScoreSheet()
    
    def updateNextPlayerToBowl(self,playerId,frame,name):
        if playerId == self.numOfPlayers:
            self.nextToBowlPlayerId = 0             
            self.nextToBowlFrame = frame + 1
            self.nextToBowlPlayerName = self.scoreSheet[0]['NAME']
        else:
            self.nextToBowlPlayerId = playerId 
            self.nextToBowlFrame = frame
            self.nextToBowlPlayerName = self.scoreSheet[playerId]['NAME']
        
    def getNextPlayerToBowl(self):
        '''
        playerId = self.numOfPlayers
        frame = 13
        playerName = None
        for i in range(12):            
            for playerListIndex,player in enumerate(self.scoreSheet):
                if self.scoreSheet[playerListIndex][i+1][0] is None:
                    if self.scoreSheet[playerListIndex]['ID'] < playerId \
                       and (i+1) < frame:
                           playerId = self.scoreSheet[playerListIndex]['ID']
                           frame = i+1
                           playerName = self.scoreSheet[playerListIndex]['NAME']
                elif not (self.scoreSheet[playerListIndex][i+1][0] == 10):
                    if self.scoreSheet[playerListIndex][i+1][1] is None:
                        if self.scoreSheet[playerListIndex]['ID'] < playerId \
                           and (i+1) < frame:
                               playerId = self.scoreSheet[playerListIndex]['ID']
                               frame = i+1
                               playerName = self.scoreSheet[playerListIndex]['NAME']    
        '''
        #return playerId, playerName, frame
        return self.nextToBowlPlayerId,self.nextToBowlFrame,self.nextToBowlPlayerName
        
    def runGame(self,pinCount):
        playerId , nextFrame, playerName  = self.getNextPlayerToBowl()         
        shotCount = self.firstShot        
        #print 'playerId, playerName, nextFrame :',playerId,playerName,nextFrame        
        if not self.gameEnded:
            if (nextFrame < 10):
                if self.firstShot:            
                    self.receiveFrameScore(playerId,nextFrame,1,int(pinCount))        
                    if not int(pinCount) == 10:
                        self.firstShot = False
                    else:
                        self.updateNextPlayerToBowl(playerId + 1,nextFrame, playerName)
                else:
                    self.receiveFrameScore(playerId,nextFrame,2,int(pinCount))
                    self.firstShot = True
                    self.updateNextPlayerToBowl(playerId + 1,nextFrame, playerName)
                    
            if (nextFrame == 10):
                if self.firstShot:            
                    self.receiveFrameScore(playerId,nextFrame,1,int(pinCount))        
                    if not int(pinCount) == 10:
                        self.firstShot = False
                    else:
                        self.updateNextPlayerToBowl(playerId,nextFrame + 1, playerName)
                else:
                    self.receiveFrameScore(playerId,nextFrame,2,int(pinCount))
                    self.firstShot = True
                    if not self.spare(self.scoreSheet[playerId][10][0],self.scoreSheet[playerId][10][1]):
                        if playerId == (self.numOfPlayers - 1):
                            self.gameEnded = True
                            self.updateNextPlayerToBowl(0,1, self.scoreSheet[0]['NAME'])
                        else:
                            self.updateNextPlayerToBowl(playerId + 1,nextFrame, playerName)
                    else:
                        self.updateNextPlayerToBowl(playerId,nextFrame + 1, playerName)
            
            if nextFrame == 11:
                if self.strike(self.scoreSheet[playerId][10][0]):
                    if self.firstShot:
                        self.receiveFrameScore(playerId,11,1,int(pinCount))
                        if not int(pinCount) == 10:
                            self.firstShot = False
                        else:
                            self.updateNextPlayerToBowl(playerId,nextFrame + 1, playerName)    
                    else:
                        self.receiveFrameScore(playerId,11,2,int(pinCount))
                        self.firstShot = True
                        if playerId == (self.numOfPlayers - 1):                        
                            self.gameEnded = True
                            self.updateNextPlayerToBowl(0,1, self.scoreSheet[0]['NAME'])
                        else:
                            self.updateNextPlayerToBowl(playerId + 1,10, playerName)
                            
                elif self.spare(self.scoreSheet[playerId][10][0],self.scoreSheet[playerId][10][1]):
                    self.receiveFrameScore(playerId,11,1,int(pinCount))
                    if playerId == (self.numOfPlayers - 1):                    
                        self.gameEnded = True
                        self.updateNextPlayerToBowl(0,1, self.scoreSheet[0]['NAME'])
                    else:
                        self.updateNextPlayerToBowl(playerId + 1,10, playerName)
                else:
                    if playerId == (self.numOfPlayers - 1):
                        self.gameEnded = True
                        self.updateNextPlayerToBowl(0,1, self.scoreSheet[0]['NAME'])
            if nextFrame == 12:
                if self.strike(self.scoreSheet[playerId][11][0]):
                    self.receiveFrameScore(playerId,12,1,int(pinCount))
                if playerId == (self.numOfPlayers - 1):
                    self.gameEnded = True
                    self.updateNextPlayerToBowl(0,1, self.scoreSheet[0]['NAME'])
                else:
                    self.updateNextPlayerToBowl(playerId + 1,10, playerName)
                        
        
            prevFrameTotalReCount = -1
            twoFramesBackTotalReCount = -1            
            if nextFrame == 2:
                prevFrameTotalReCount = self.calcGameTotalUpToFrame(playerId,1)
                twoFramesBackTotalReCount = -1
            if nextFrame > 2:
                prevFrameTotalReCount = self.calcGameTotalUpToFrame(playerId,nextFrame - 1)
                twoFramesBackTotalReCount = self.calcGameTotalUpToFrame(playerId,nextFrame - 2)
            data = [playerId,
                    nextFrame,
                    shotCount,
                    self.calcGameTotalUpToFrame(playerId,nextFrame),
                    prevFrameTotalReCount,
                    twoFramesBackTotalReCount]            
            return data
             
if __name__ == "__main__":
    text = 'Welcome to the Bowling Alley. Please Enter num of Players:'
    numOfPlayers = int(raw_input(text))    
    game = NewGame(numOfPlayers)    
    game.runGame()         
    print 'Game Over!'
    