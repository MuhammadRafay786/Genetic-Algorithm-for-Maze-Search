# Importing the Libraries
from pyamaze import maze, agent
from random import *

# Maze related Modules
Rows=10
Cols=10
a=maze(Rows,Cols)           #Generating a MAZE
a.CreateMaze(Rows,Cols,loopPercent=100, theme="dark")
finalAgent=agent(a,1,1,shape='square',footprints=True,color='green')
Dictt=a.maze_map

# Constants & Global Variables
population_size = 500
Generations = 0
checkFlag=0
Total_Path,PathLength,Inf_Steps,Total_Fitness=[],[],[],[]
w_l,w_f,w_t=2,3,3

# Functions to get Solution.
# Random Population Generation in a list.
def RandomPopulation():
    population=[]
    pop1=[]
    for _ in range(1, population_size+1):
        random_pop=[[1]+[randint(1,Rows) for _ in range (Cols-2)]+[Rows]]       # Fixing 1st and last element
        direct_bit =[randint(0,1) for _ in range(2)]
        population=random_pop+[direct_bit]
        pop1.append(population)
    return pop1
    # population=[[[1]+[randint(1,Rows) for _ in range (Cols-2)]+[Rows],[randint(0,1) for _ in range(2)]] for _ in range (population_size)]
    # return population
# Getting Number of Turns
def Turns():
    Total_Turns=[]
    for i in range(population_size):
        m,o=population[i]
        turns=0
        for k in range (Cols-1):
            if m[k]!=m[k+1]:        # Comparing if the 1st gene with 2nd gene.
                turns+=1
        Total_Turns.append(turns)   
    return Total_Turns           
# Infeasible Step generation. This Function calculates Path, Path length and Infeasible Steps. Path is generated as a tuple. Starting and 
# ending point is fixed while in between we apply different conditions to generate path and its path length.
def InfeasibleSteps(listt):
    chromosome, [Orientation, Direction] = listt        #Unpacking of a list.
    Inf_Steps=[]; Total_Path=[]
    if checkFlag==1: Total_Path.append((1,1))       #Fixing 1st coordinate as (1,1).
    if Rows!=Cols: Orientation=0
    Decision_bit=Orientation ^ Direction        #XOR Operator between orientation and direction to get column wise or row wise approach.
    x_point,increment=(1,1),1
    Inf_Steps = []
    for i in range (0,len(chromosome) - 1):
        NextMove=i+1
        Limit=(chromosome[i+1]+1) if chromosome[i+1] > chromosome[i] else (chromosome[i+1]-1)
        while increment!= Limit:
            if Orientation==0: y_point=(increment,NextMove+Decision_bit)
            else: y_point=(NextMove+Decision_bit,increment)
            if checkFlag==1 and y_point not in ((1,1),(Rows,Cols)):
                Total_Path.append(y_point)
            if y_point[0]-x_point[0]!=0:        #Checking the condition for infeasible steps by finding the obstacle in all ways.
                if y_point[0]-x_point[0]>0:
                    if Dictt[x_point]['S']==0: Inf_Steps.append(1)   
                    else: Inf_Steps.append(0)
                else:
                    if Dictt[x_point]['N']==0: Inf_Steps.append(1)         
                    else: Inf_Steps.append(0)        
            elif y_point[1]-x_point[1]!=0:
                if y_point[1]-x_point[1]>0:
                    if Dictt[x_point]['E']==0: Inf_Steps.append(1)
                    else: Inf_Steps.append(0)
                else:
                    if Dictt[x_point]['W']==0: Inf_Steps.append(1)         
                    else: Inf_Steps.append(0)           
            x_point=y_point
            if chromosome[i+1]>chromosome[i]: increment+=1
            else: increment-=1
        if chromosome[i+1]>chromosome[i]: increment-=1
        else: increment+=1
    if checkFlag==1:
        Total_Path.append((Rows,Cols))
        return Total_Path,len(Inf_Steps),sum(Inf_Steps)
    return len(Inf_Steps),sum(Inf_Steps)   
# CrossOver Function that uses half population of 1 gene and swap them with the 2nd half population of other gene.
def CrossOver(chromosome):
    crossPoint=randint(2,Cols - 2)      #Generating random Crosspoint.
    Half_pop=int(population_size / 2)
    for i in range (Half_pop,(population_size - 1),2):
        chromosome[i][0]=chromosome[i-Half_pop][0][0:crossPoint]+chromosome[i-Half_pop+1][0][crossPoint:]
        chromosome[i+1][0]=chromosome[i-Half_pop+1][0][0:crossPoint]+chromosome[i-Half_pop][0][crossPoint:]
# Mutation Function that changes random gene with the random number and also mutates direction bit.
def Mutation(chromosome):
    for i in range (population_size ):
        Gene,Direction_bit=chromosome[i]        #Unpacking a list.
        Gene[randint(2,Cols-2)]=randint(1,Rows)
        if i>=int(population_size /2):
            Direction_bit[0],Direction_bit[1]=randint(0,1),randint(0,1)     #Mutating Random Direction bit. 
# Final Fitness Check Function that takes turns, length and infeasible steps and putting the values in the formula to get final fitness.
def Fitness_Check(turns, length, infeasible):
    Fitness_Turns=1-(turns-min(Turn))/(max(Turn)-min(Turn))
    Fitness_Length=1-(length-min(PathLength))/(max(PathLength)-min(PathLength))
    Fitness_Infeasible=1-(infeasible-min(Inf_Steps))/(max(Inf_Steps)-min(Inf_Steps))
    return (100*w_f*Fitness_Infeasible)*((w_l*Fitness_Length)+(w_t*Fitness_Turns))/(w_l+w_t)

# Main Function and Calling of Functions
if __name__ == "__main__":
    population=RandomPopulation()
    while(Generations <= 2000):
        Total_Path,PathLength,Inf_Steps,Total_Fitness=[],[],[],[]
        print(f'Generation: {Generations}') 
        Turn=Turns()        
        inf=[InfeasibleSteps(chromosome) for chromosome in population]
        for i in range (population_size):
            PathLength.append(inf[i][0])            #Unpacking of Path Length and Infeasible steps from Insfeasible Function above.
            Inf_Steps.append(inf[i][1])
        for i in range (population_size):
            fittest=Fitness_Check(Turn[i], PathLength[i], Inf_Steps[i])
            Total_Fitness.append(fittest)
            if Inf_Steps[i]==0:     #Checking for the final Result if infeasible steps are 0 to get the solution.
                checkFlag=1
                Solved_Path, Solved_Length, Solved_Inf = InfeasibleSteps(population[i])
                Solved_Turns = Turn[i]
                print(f"\nSolution found after {Generations} iterations")
                print("\n"+"*"*80)      #Printing of the results.
                print(f'Fittest Chromosome = {population[i][0]}')
                print("\n"+"*"*80); print(f'Path Length = {Solved_Length}\t\tTurns = {Solved_Turns}\t\tInfeasible Steps = {Solved_Inf}')
                print("\n"+"*"*80); print(f'Path Generated = {Solved_Path}')
                print("\n"+"*"*80)
                a.tracePath({finalAgent:Solved_Path}, delay=150)
                a.run()
                break
        if checkFlag==1:
            break
        pop=list(zip(population,Total_Fitness))         #Parent Selection?Sorting of the Population according to fitness
        SortedPopulation=sorted(pop,key= lambda x: x[1],reverse=True)
        population=[x[0] for x in SortedPopulation]
        t=list(zip(Turn,Total_Fitness))                 #Parent Selection?Sorting of the Turns according to fitness
        SortedTurns=sorted(t,key= lambda x: x[1],reverse=True)          #Sorting in decreasing/descending order.
        Turn=[x[0] for x in SortedTurns]
        CrossOver(population)
        Mutation(population)
        Generations+=1
# End of the Program.