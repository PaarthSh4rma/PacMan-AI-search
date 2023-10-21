import logging
import time

import util
from problems.q1c_problem import q1c_problem


def q1c_solver(problem: q1c_problem):
    "*** YOUR CODE HERE ***"

    def minimum_heuristic(state):
        distances = [util.manhattanDistance(state[0], goal) for goal in state[1]]
        return min(distances) if distances else 0

    def a_star(problem):
        startState = problem.getStartState()
        initialFn = minimum_heuristic(startState)

        openNodesList = util.PriorityQueue()
        closedNodesList = set()

        openNodesList.push((startState, [], 0), initialFn)

        while not openNodesList.isEmpty():
            currentState, path, gn = openNodesList.pop()

            if problem.isGoalState(currentState):
                return path

            if currentState not in closedNodesList:
                closedNodesList.add(currentState)
                for successorState, action, step_cost in problem.getSuccessors(currentState):
                    if successorState not in closedNodesList:
                        newPath = path + [action]
                        successorGn = gn + step_cost
                        successorHn = minimum_heuristic(successorState)
                        successorFn = successorGn + successorHn
                        openNodesList.push((successorState, newPath, successorGn), successorFn)

        return None

    def beam_search(problem):
        beamWidth = 10
        startState = problem.getStartState()
        openNodesList = util.PriorityQueue()
        visited = set()

        openNodesList.push((startState, []), minimum_heuristic(startState))

        visited.add(startState)

        while openNodesList:

            newBeam = []
            for _ in range(min(beamWidth, openNodesList.count)):
                if not openNodesList.isEmpty():
                    newBeam.append(openNodesList.pop())

            openNodesList = util.PriorityQueue()
            for currentNode, path in newBeam:
                if problem.isGoalState(currentNode):
                    return path

                successorList = problem.getSuccessors(currentNode)
                for successorState, action, cost in successorList:
                    if successorState not in visited:
                        newpath = path + [action]
                        h = minimum_heuristic(successorState)
                        openNodesList.push((successorState, newpath), h)
                        visited.add(successorState)

        return None

    start = problem.getStartState()
    if len(start[1]) < 25:
        return a_star(problem)
    else:
        return beam_search(problem)
