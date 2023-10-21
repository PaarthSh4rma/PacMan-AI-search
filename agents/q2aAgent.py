import logging
import random

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class Q2A_Agent(Agent):

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '3'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    @log_function
    def getAction(self, gameState: GameState):
        """
            Returns the minimax action from the current gameState using self.depth
            and self.evaluationFunction.

            Here are some method calls that might be useful when implementing minimax.

            gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

            gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

            gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        logger = logging.getLogger('root')
        logger.info('MinimaxAgent')
        "*** YOUR CODE HERE ***"

        def minimax(agentIndex, depth, gameState):

            if gameState.isWin() or gameState.isLose() or (depth == 0 and agentIndex == 0):
                return self.evaluationFunction(gameState), ""

            legalActions = gameState.getLegalActions(agentIndex)

            if len(legalActions) == 0:
                return self.evaluationFunction(gameState), ""

            nextAgentIdx = (agentIndex + 1) % gameState.getNumAgents()
            if agentIndex == 0:
                bestActions, bestVal = maximise(depth, agentIndex, gameState, legalActions, nextAgentIdx)
                return bestVal, random.choice(bestActions)

            else:
                bestActions, bestVal = minimise(depth, agentIndex, gameState, legalActions, nextAgentIdx)
                return bestVal, random.choice(bestActions)

        def minimise(depth, agentIndex, gameState, legalActions, nextAgentIdx):
            bestVal = float("inf")
            bestActions = [""]
            for action in legalActions:
                successorState = gameState.generateSuccessor(agentIndex, action)
                value, _ = minimax(nextAgentIdx, depth - 1 if nextAgentIdx == 0 else depth, successorState)
                if value < bestVal:
                    bestVal = value
                    bestActions = [action]
                elif value == bestVal:
                    bestActions.append(action)
            return bestActions, bestVal

        def maximise(depth, agentIndex, gameState, legalActions, nextAgentIdx):
            bestVal = -float("inf")
            bestActions = [""]
            for action in legalActions:
                successorState = gameState.generateSuccessor(agentIndex, action)
                value, _ = minimax(nextAgentIdx, depth, successorState)
                if value > bestVal:
                    bestVal = value
                    bestActions = [action]
                elif value == bestVal:
                    bestActions.append(action)
            return bestActions, bestVal

        best_val, bestAction = minimax(0, self.depth, gameState)
        return bestAction
