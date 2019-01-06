#Isaac Silva
#ID:015014894
#CECS 451
#08/03/2018
#I need numpy to reshape the values
import numpy as np
import sys

## This is the class Sudoku that applies hill climbing
class Sudoku():
    # Is it self and have a freshed values
    def __init__(self):
        self.reset()
#Reseting the puzzle
    def reset(self):
        #This
        self.board = (np.indices((9, 9)) + 1)[1]
        for i in range(len(self.board)):
            #permutation
            self.board[i] = np.random.permutation(self.board[i])
            #Array to be fixed
        self.fixedValues = np.array([
            # These numbers are represented as -->> (val, row, col)
            (3, 0, 0), (7, 0, 3), (9, 0, 5), (6, 0, 7),(9, 1, 0),(5, 1, 1),(8, 1, 5),(2, 1, 8),(6, 2, 0),(7, 2, 3),(3, 3, 1),(6, 3, 4),(5, 3, 7),(9, 4, 2),(6, 4, 6),(8, 5, 1),(4, 5, 4),
            (2, 5, 7),(5, 6, 5),(6, 6, 8),(4, 7, 0),(9, 7, 3),(1, 7, 7),(3, 7, 8),(9, 8, 1),(1, 8, 4),(2, 8, 6),(7, 8, 8)
        ])
        #Helpful for the Sudoku puzzle values placement 'setup'
        self.setup()

# In this defenition is a basic formation of the Sudoku puzzle
    def printBoard(self, board=[]):
        if (board == []):
            board = self.board

        for i in range(len(board)):
            if (i % 3 == 0 and i != 0):
                ####
                print("------+------+------")
            for j in range(len(board[i])):
                if (j % 3 == 0 and j != 0):
                    sys.stdout.write("|")
                sys.stdout.write(str(board[i][j]) + " ")
            print("")
#Swaping values dependent on Index
    def swapP(self, val, line, col):
        valIndex = np.where(self.board[line] == val)[0][0]
        self.swap(self.board[line], valIndex, col)
#This defenetion
    def setup(self):
        for (val, row, col) in self.fixedValues:
            self.swapP(val, row, col)

#This where the values would fit in their place and perspective in a UNIQUE form
    def insertForm(self, board=[]):
        if (board == []):
            board = self.board
        score = 0
        rows, cols = board.shape
        for row in board:
            score += len(np.unique(row))
        for col in board.T:
            score += len(np.unique(col))
        for i in range(0, 3):
            for j in range(0, 3):
                sub = board[3 * i:3 * i + 3, 3 * j:3 * j + 3]
                score += len(np.unique(sub))
        return score
#Defenition for a swap method
    def swap(self, arr, pos1, pos2):
        arr[pos1], arr[pos2] = arr[pos2], arr[pos1]
#Checking if the value in the place is in the right place if the row is 1 and col is 2 return True
    def isFixed(self, row, col):
        for t in self.fixedValues:
            if (row == t[1] and col == t[2]):
                return True
        return False
#This defenition is to check the "neighbor node" to see if it is appropriate.
    def NeighborNode(self):
        tempBoard = self.board.copy()
        best = (0, (0, 0), -1)
        for i in range(len(tempBoard)):
            for j in range(len(tempBoard[i])):
                for k in range(i, len(tempBoard)):
                    #check if fixed
                    if (self.isFixed(i, j) or self.isFixed(i, k)):
                        continue
                    #swap
                    self.swap(tempBoard[i], j, k)
                    #see if is best or not
                    contestant = (i, (j, k), self.insertForm(tempBoard))
                    #If it is swap
                    if (contestant[2] > best[2]):
                        best = contestant
                    self.swap(tempBoard[i], j, k)
        return best
#Defenition for the conept of hill climbing and see if and when the value should be in the right place if not return the scores or nextscore depending on success
    def HillClimb(self):
        scores = []
        maxScore = self.insertForm()
        #Use a while loop to append values and swap column and rows.
        while True:
            scores.append(maxScore)
            (row, (col1, col2), nextScore) = self.NeighborNode()
            if (nextScore <= maxScore):
                return scores
            self.swap(self.board[row], col1, col2)
            maxScore = nextScore
#Call a new Sudoku

sud = Sudoku()
print("Hill Climbing")
#This a blank to fill
t = []
maxScore = -1
bestOption = []
#create a for loop for "Thinking"
for i in range(10):
    #reset puzzle
    sud.reset()
    #Have it equal to final score
    finalScore = sud.HillClimb()
    maxFinalScore = max(finalScore)
    if (maxScore < maxFinalScore):
        maxScore = maxFinalScore
        #chooses the best option
        bestOption = sud.board.copy()
    print(str(i) + ") " + str(finalScore[-1]) + "/243")
    #Finding the score
    if (finalScore == 243):
        sud.printBoard()
        break
        #Append answer
    t.append(finalScore)
    #Display completed puzzle
sud.printBoard(bestOption)
