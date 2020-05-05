# Assignment

# Write a program that solves the following problem:

# Three missionaries and three cannibals come to a river and find a boat that holds two people. Everyone must get across the river to continue the journey. However, if the cannibals ever outnumber the missionaries on either bank, the missionaries will be eaten.

# Find a series of crossings that will get everyone safely to the other side of the river.  Record your program running and submit your code and recording.

# Canvas questions

# 1. How many hours do you estimate you used completing this assignment?

# 10 h

# 2. What was easiest for you when completing this assignment?

# Understanding the problem and find a solution using graph

# 3. What was the most difficult challenge you experienced when completing this assignment?

# Creating a real computer science solution (further discussion on the video). Generate and validate permutation, traverse a graph finding a solution.

# Suggested article 

# https://mark-borg.github.io/blog/2016/river-crossing-puzzles/

from collections import defaultdict

class McNode:

    @classmethod
    def isValidState(cls, stateTuple):
        for tupl in stateTuple:
            mOk = tupl[0] in [0, 1, 2, 3]
            cOk = tupl[1] in [0, 1, 2, 3]
            bOk = tupl[2] in [0, 1]
            mHEc = tupl[0] >= tupl[1] or tupl[0] == 0
            if mOk and cOk and bOk and mHEc:
                continue
            else:
                return False
        return True

    #                  parent           root
    def __init__(self, parentTuple=None, stateTuple=((3, 3, 1), (0, 0, 0))):
        self.__adjMcTuples = [] if parentTuple is None else [parentTuple]  # _adjMcNodes[0] --> parent
        self.__stateTuple = stateTuple
        self.__buildChildrenStateTuples()
        self.findGoalCalled = False

    @property
    def isGoal(self):
        return self.stateTuple == ((0, 0, 0), (3, 3, 1))

    def __buildChildrenStateTuples(self):
        if self.isGoal:
            return
        mOrcMoves = [0, 1, 2]
        bMoves = [1, -1]  # b == 1 r --> l, b == -1 r <-- l
        childrenTuples = self.__adjMcTuples
        for bDir in bMoves:
            for moveM in mOrcMoves:
                for moveC in mOrcMoves:
                    if 0 < moveM + moveC <= 2:  # at least 1 in the boat
                        newStateTuple = (
                            (
                                self.stateTuple[0][0] + (moveM * (-1) * bDir),
                                self.stateTuple[0][1] + (moveC * (-1) * bDir),
                                self.stateTuple[0][2] + (-1 * bDir)
                            ),
                            (
                                self.stateTuple[1][0] + (moveM * (1) * bDir),
                                self.stateTuple[1][1] + (moveC * (1) * bDir),
                                self.stateTuple[1][2] + (1 * bDir)
                            )
                        )
                        if McNode.isValidState(newStateTuple) and newStateTuple not in childrenTuples:
                            print("From {} generated Tuple: {}".format(self.stateTuple, newStateTuple))
                            childrenTuples.append(newStateTuple)

    @property
    def stateTuple(self):
        return self.__stateTuple

    # singleton Dis
    defDict = defaultdict(lambda: None)

    @classmethod
    def getMcNodeFromStateTuple(cls,
                                parentTuple=None, stateTuple=((3, 3, 1), (0, 0, 0))
                                ):
        if McNode.defDict[str(stateTuple)] is None:
            McNode.defDict[str(stateTuple)] = McNode(parentTuple, stateTuple)
        return McNode.defDict[str(stateTuple)]

    @property
    def adjMcNodes(self):
        return [
            McNode.getMcNodeFromStateTuple(
                self.stateTuple,
                tup
            ) for tup in self.__adjMcTuples
        ]

    def FindGoal(self):
        self.findGoalCalled = True
        GoalFound = False
        if self.isGoal:
            GoalFound = True
        else:
            for mcNode in self.adjMcNodes:
                if not mcNode.findGoalCalled:
                    if mcNode.FindGoal():
                        GoalFound = True
                if mcNode.isGoal:
                    print("Goal Found from parent: {}".format(self.stateTuple))
        return GoalFound


def run():

    print("Goal Found: {}".format(McNode.getMcNodeFromStateTuple().FindGoal()))
