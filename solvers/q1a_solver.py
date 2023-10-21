import logging

import util
from problems.q1a_problem import q1a_problem


def q1a_solver(problem: q1a_problem):
    "*** YOUR CODE HERE ***"

    def a_star(problem):
        start = problem.getStartState()
        goal = problem.goalPosition
        initialFn = 0

        openNodes = util.PriorityQueue()
        closedNodes = set()

        openNodes.push((start, [], 0), initialFn)

        while not openNodes.isEmpty():
            currentState, path, gn = openNodes.pop()

            if problem.isGoalState(currentState):
                return path

            if currentState not in closedNodes:
                closedNodes.add(currentState)
                successors = problem.getSuccessors(currentState)

                for successor in successors:
                    successorState = successor[0]
                    action = successor[1]
                    cost = successor[2]

                    if successorState not in closedNodes:
                        newPath = path + [action]
                        newGn = gn + cost
                        newHn = util.manhattanDistance(successorState, goal)
                        Fn = newGn + newHn
                        openNodes.push((successorState, newPath, newGn), Fn)
        return None

    return a_star(problem)




