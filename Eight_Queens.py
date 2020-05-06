from collections import defaultdict


class NQueensNode:

    # StateTuple ((Q1r,Q1c),(Q2r,Q2c), ..., (-1, -1))  <-- no queen pos yet
    # Qs = n = rows = cols

    @classmethod
    def isValidState(cls, stateTuple):
        n = len(stateTuple)
        board = [[0 for x in range(n)] for y in range(n)]
        availableSpots = [(r, c) for r in range(n) for c in range(n)]
        for queen in list(filter(lambda q: q != (-1, -1), stateTuple)):
            for row in range(n):
                for col in range(n):
                    # queen pos
                    if queen == (row, col):
                        if board[row][col] == 0:
                            # flag the queen
                            board[row][col] = -1
                            # removed from availableSpots
                            availableSpots = list(filter(lambda spot: spot != (row, col), availableSpots))
                        else:
                            # trying to place a queen in a flagged spot
                            return False, []
                    # same row and same col
                    elif queen[0] == row or queen[1] == col:
                        board[row][col] += 1
                        # removed from availableSpots
                        availableSpots = list(filter(lambda spot: spot != (row, col), availableSpots))
                    # diagonals
                    elif abs(queen[0] - row) == abs(queen[1] - col):
                        board[row][col] += 1
                        # removed from availableSpots
                        availableSpots = list(filter(lambda spot: spot != (row, col), availableSpots))

        return True, availableSpots

    #                  parent           root
    def __init__(self, parentTuple=None, stateTuple=((-1, -1), (-1, -1), (-1, -1), (-1, -1))):

        self.__stateTuple = stateTuple
        self.__adjEqTuples = [] if parentTuple is None else [parentTuple]  # _adjMcNodes[0] --> parent
        self.__buildChildrenStateTuples()
        self.findGoalCalled = False

    @property
    def stateTuple(self):
        return self.__stateTuple

    @property
    def isGoal(self):
        # n Queen are placed ok
        placingNQueens = (-1, -1) not in self.stateTuple
        allQueenPlaced = NQueensNode.isValidState(self.stateTuple)[0]
        return placingNQueens and allQueenPlaced

    def __buildChildrenStateTuples(self):
        if self.isGoal:
            return
        # the first no yet queen
        index = list(self.stateTuple).index((-1, -1))
        s = set()
        for availableSpot in NQueensNode.isValidState(self.stateTuple)[1]:
            childTupleAsList = list(self.stateTuple)
            head, tail = childTupleAsList[:childTupleAsList.index((-1, -1))], childTupleAsList[
                                                                              childTupleAsList.index((-1, -1)):]
            head.append(availableSpot)
            head.sort()
            tail.pop()
            head.extend(tail)
            # print(head)
            if tuple(head) not in self.__adjEqTuples:
                self.__adjEqTuples.append(tuple(head))
            # print("From {} generated Tuple: {}".format(self.stateTuple, tuple(childTupleAsList)))

    # singleton Dis
    defDict = defaultdict(lambda: "None")

    @classmethod
    def getEqNodeFromStateTuple(cls,
                                parentTuple=None, stateTuple=((-1, -1), (-1, -1), (-1, -1), (-1, -1))
                                ):
        if NQueensNode.defDict[str(stateTuple)] == "None":
            NQueensNode.defDict[str(stateTuple)] = NQueensNode(parentTuple, stateTuple)
        return NQueensNode.defDict[str(stateTuple)]

    @property
    def adjMcNodes(self):
        return [
            NQueensNode.getEqNodeFromStateTuple(
                self.stateTuple,
                tup
            ) for tup in self.__adjEqTuples
        ]

    goals = set()

    def FindGoal(self):
        self.findGoalCalled = True
        GoalFound = False
        if self.isGoal:
            GoalFound = True
            NQueensNode.goals.add(self.stateTuple)
        else:
            for nqNode in self.adjMcNodes:
                if not nqNode.findGoalCalled:
                    if nqNode.FindGoal():
                        GoalFound = True
                if nqNode.isGoal:
                    print("Goal {} Found from parent: {}".format(nqNode.stateTuple, self.stateTuple))
        return GoalFound


def run():
    nQueensRoot = NQueensNode.getEqNodeFromStateTuple(
        #stateTuple=((-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1))
    )
    print("Goal Found: {}".format(nQueensRoot.FindGoal()))
    print("Goals Found: {}".format(len(NQueensNode.goals)))


run()
