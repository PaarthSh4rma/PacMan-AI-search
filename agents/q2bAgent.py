import logging
import random
import time

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState
from util import manhattanDistance


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class Q2B_Agent(Agent):

    def __init__(self, evalFn='eval_function', depth='9'):
        self.index = 0  # Pacman is always agent index 0
        self.positionCount = {}  # To keep track of visited positions
        if evalFn == 'eval_function':
            self.evaluationFunction = self.eval_function
        else:
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
        pos = gameState.getPacmanPosition()
        if pos in self.positionCount:
            self.positionCount[pos] += 1
        else:
            self.positionCount = {}
            self.positionCount[pos] = 1

        logger = logging.getLogger('root')
        logger.info('MinimaxAgent')

        start_time = time.time()

        def alpha_beta(agentIdx, depth, gameState, alpha, beta):
            if gameState.isWin() or gameState.isLose() or (depth == 0 and agentIdx == 0):
                return self.evaluationFunction(gameState), ""

            legalActions = gameState.getLegalActions(agentIdx)
            if len(legalActions) == 0:
                return self.evaluationFunction(gameState), ""

            nextAgentIdx = (agentIdx + 1) % gameState.getNumAgents()

            if agentIdx == 0:
                value = -float('inf')
                action = []
                for act in legalActions:
                    successor = gameState.generateSuccessor(agentIdx, act)
                    nextVal, nextAct = alpha_beta(nextAgentIdx, depth - 1, successor, alpha, beta)
                    if nextVal > value:
                        value, action = nextVal, [act]
                    if nextVal == value:
                        value = nextVal
                        action.append(act)

                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break  # cut
                return value, random.choice(action)

            else:
                value = float('inf')
                action = ""
                for act in legalActions:
                    successor = gameState.generateSuccessor(agentIdx, act)
                    nextVal, nextAct = alpha_beta(nextAgentIdx, depth, successor, alpha, beta)
                    if nextVal < value:
                        value, action = nextVal, act
                    beta = min(beta, value)
                    if alpha >= beta:
                        break  # cut
                return value, action

        time_limit = 0.05
        bestAction = Directions.STOP

        for depth in range(1, self.depth + 1):
            if time.time() - start_time >= time_limit:
                break
            bestVal, current_bestAction = alpha_beta(0, depth, gameState, -float('inf'), float('inf'))
            if current_bestAction:
                bestAction = current_bestAction

        return bestAction

    def eval_function(self, gameState):
        score = gameState.getScore()
        pos = gameState.getPacmanPosition()
        foods = gameState.getFood().asList()
        ghost_states = gameState.getGhostStates()
        capsules = gameState.getCapsules()
        foods += capsules  # Consider capsules as food

        closestFood = sum([manhattanDistance(food, pos) for food in foods]) if foods else float('inf')
        closestGhost = min(
            [manhattanDistance(ghost.getPosition(), pos) for ghost in ghost_states]) if ghost_states else float('inf')

        score += 20.0 / (closestFood + 1)

        if closestFood == 0:
            score += 40

        closestCapsule = min([manhattanDistance(capsule, pos) for capsule in capsules]) if capsules else float('inf')

        score += 20.0 / (closestCapsule + 1)

        if closestCapsule == 0:
            score += 50

        for ghost in ghost_states:
            if ghost.scaredTimer > 0:
                score += 200
            elif closestGhost < 3:
                score -= 500 / (closestGhost + 1)

        if len(foods) == 0:
            score += 1000

        numLegalActions = len(gameState.getLegalActions(0))
        score += numLegalActions * 10

        return score

