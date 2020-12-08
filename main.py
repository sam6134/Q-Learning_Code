from random import randint
# The parameters can be changes to appropriate parameters
# For better training put the number of episodes to be atleast 100 times of the side of the grid
Nx = 10
Ny = 10
NumEpisodes = 1000

# Environment Class ------------------------------
class Environment:
    def __init__(self,Nx,Ny):
        self.Nx = Nx
        self.Ny = Ny
        self.grid = [[0]]
    def getActions(self,i,j):
        if(i==0 and j ==0):
            return ['D','R']
        if(i==( self.Nx - 1 ) and j == 0):
            return ['U','R']
        if(i == 0 and j == (self.Ny-1)):
            return ['D','L']
        if(i==0):
            return ['D','L','R']
        if(i==(self.Nx-1)):
            return ['U','L','R']
        if(j == 0):
            return ['U','D','R']
        if(j==(self.Ny-1)):
            return ['U','D','L']
        return ['U','D','L','R']
    def getRewards(self,i,j):
        if(i == (self.Nx-1) and j==(self.Ny-1)):
            return 100
        else:
            return -0.1

# Brain Class --------------------------------
class Brain:
    def __init__(self,alpha,gamma):
        self.Qtable = dict()
        self.alpha = alpha
        self.gamma = gamma
    def updateQvalue(self,i,j,a,i1,j1,r):
        key1 = str(i)+":"+str(j)+":"+str(a)
        keyU = str(i1) + ":" + str(j1) + ":" + "U"
        keyD = str(i1) + ":" + str(j1) + ":" + "D"
        keyL = str(i1) + ":" + str(j1) + ":" + "L"
        keyR = str(i1) + ":" + str(j1) + ":" + "R"
        maxQ = max(self.Qtable.get(keyD,0),self.Qtable.get(keyU,0),self.Qtable.get(keyL,0),self.Qtable.get(keyR,0))
        self.Qtable[key1] = (1-self.alpha)*self.Qtable.get(key1,0) + self.alpha*(r + self.gamma*(maxQ))
    def makeTransitionMax(self,i,j,actions):
        maxi = -1
        for a in actions:
            keyi = str(i) + ":" + str(j) + ":" + str(a)
            Qval = self.Qtable.get(keyi,0)
            maxi = max(maxi,Qval)
        for a in actions:
            keyi = str(i) + ":" + str(j) + ":" + str(a)
            Qval = self.Qtable.get(keyi,0)
            if(Qval == maxi):
                if (a == 'U'):
                    return i - 1, j, a
                if (a == 'D'):
                    return i + 1, j, a
                if (a == 'L'):
                    return i, j - 1, a
                if (a == 'R'):
                    return i, j + 1, a

# Agent Class ---------------------------------------------------
class Agent:
    def __init__(self):
        pass
    def makeTransitionRandom(self,i,j,actions):
        n = len(actions)
        x = randint(0,n-1)
        a = actions[x]
        if(a == 'U'):
            return i-1,j,a
        if (a == 'D'):
            return i + 1, j, a
        if (a == 'L'):
            return i, j-1, a
        if (a == 'R'):
            return i, j+1, a

# Main function -----------------------------------------
environment = Environment(Nx,Ny)
agent = Agent()
brain = Brain(0.2,0.9)
epsilon = 0.9
decay = 0.999
for episodes in range(NumEpisodes):
    Total_reward = 0
    curr_i =0
    curr_j =0
    while(True):
        if(curr_i == (environment.Nx-1) and curr_j == (environment.Ny-1)):
            break
        chk = randint(1,10)
        if(chk<=10*epsilon):
            actions = environment.getActions(curr_i,curr_j)
            i1,j1,a = agent.makeTransitionRandom(curr_i,curr_j,actions)
            r = environment.getRewards(i1,j1)
            Total_reward += r
            brain.updateQvalue(curr_i,curr_j,a,i1,j1,r)
        else:
            actions = environment.getActions(curr_i,curr_j)
            i1,j1,a = brain.makeTransitionMax(curr_i,curr_j,actions)
            r = environment.getRewards(i1, j1)
            Total_reward += r
            brain.updateQvalue(curr_i, curr_j, a, i1, j1, r)
        curr_i, curr_j = i1,j1
    epsilon = epsilon*decay
    if(episodes%100 == 0):
        print(episodes,"episodes are done")
        print("Reward Collected during this episode is",Total_reward)

print(brain.Qtable)











