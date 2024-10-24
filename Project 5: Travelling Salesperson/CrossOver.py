from random import randint

def CrossOver(solution1, solution2):
    path1 = solution1.getPath()
    path2 = solution2.getPath()
    cut1 = randint(0, len(path1) - 1)
    cut2 = randint(cut1-1, len(path2) - 1)
    cross_path = path1[cut1:cut2]
    for i in range(len(path2)):
        city = path2[i]
        if city not in cross_path:
            cross_path.append(city)
    return cross_path

#https://youtu.be/M3KTWnTrU_c?t=963 - talks about normalizing fitness values
#I think this will be important for picking which ones to cross over