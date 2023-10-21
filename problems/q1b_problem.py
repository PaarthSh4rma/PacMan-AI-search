import logging
import time
from typing import Tuple

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState


class q1b_problem:
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
    """
    def __str__(self):
        return str(self.__class__.__module__)

    def __init__(self, gameState: GameState):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.startingGameState: GameState = gameState
        self.goalList = self.startingGameState.getFood().asList()
        self.startState = (self.startingGameState.getPacmanPosition(), tuple(sorted(self.goalList)))


    @log_function
    def getStartState(self):
        "*** YOUR CODE HERE ***"
        return self.startState

    @log_function
    def isGoalState(self, state):
        "*** YOUR CODE HERE ***"
        remaining_goals = state[1]
        return len(remaining_goals) == 0

    @log_function
    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """
        "*** YOUR CODE HERE ***"
        successors = []
        current_pos, remaining_goals = state

        allowed_actions = [
            ((0, 1), "North"),
            ((0, -1), "South"),
            ((1, 0), "East"),
            ((-1, 0), "West"),
        ]

        for (dx, dy), action in allowed_actions:
            x, y = current_pos
            next_x, next_y = x + dx, y + dy

            if not self.startingGameState.hasWall(next_x, next_y):
                new_remaining_goals = []
                for pos in remaining_goals:
                    if pos != (next_x, next_y):
                        new_remaining_goals.append(pos)
                new_remaining_goals = tuple(sorted(new_remaining_goals))

                successors.append((((next_x, next_y), new_remaining_goals), action, 1))

        return successors


