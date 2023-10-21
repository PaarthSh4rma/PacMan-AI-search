import logging

import util
from problems.q1b_problem import q1b_problem


def q1b_solver(problem: q1b_problem):
    "*** YOUR CODE HERE ***"

    def min_heuristic(state):
        distances = [util.manhattanDistance(state[0], goal) for goal in state[1]]
        return min(distances) if distances else 0

    def a_star(problem):
        start = problem.getStartState()
        initialFn = min_heuristic(start)

        openNodesList = util.PriorityQueue()
        closedNodesList = set()

        openNodesList.push((start, [], 0), initialFn)

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
                        successorHn = min_heuristic(successorState)
                        successorFn = successorGn + successorHn
                        openNodesList.push((successorState, newPath, successorGn), successorFn)

        return None

    return a_star(problem)