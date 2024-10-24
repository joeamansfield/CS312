from random import randint
#set mutation rate between 0 and 100, 0 for no mutation and 100 for 100% mutation
#call mutate on entire population and let the mutation rate take care of which ones get selected
def Mutate(solution, mutation_rate): 
    if randint(0, 100) < mutation_rate:
        path = solution.getPath()
        index_1 = randint(0, len(path) - 1)
        index_2 = randint(0, len(path) - 1)
        city1 = path[index_1]
        path[index_1] = path[index_2]
        path[index_2] = city1
    #returns original solution if mutation failed
    #could potentially check solution fitness before adding to prevent duplicates
    #will still have to check for duplicates regardless?
    return path