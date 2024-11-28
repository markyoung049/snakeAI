import random




'''
block_size = 10
import pygame
pygame.init()
clock = pygame.time.Clock()
width = 100
height = 90
gap_size = 1

screen = pygame.display.set_mode([(width+2) * block_size, (height+2) * block_size])    
white = [255, 255, 255]
red = [160, 34, 34]
black = [0, 0, 0]
grey = [50, 50, 50]
green = [34, 139, 34]

'''

def generatePath(sequence, element1, element2):
    
    path = []
    index = sequence.index(element1)
    current = None

    while current != element2:

        current = sequence[index]

        path.append(current)




        if index == len(sequence) - 1:
            index = 0
        
        else:
            index = index + 1

    return path



def hamiltonian(width, height):
    
    # minimum spanning tree of width/2 * height / 2
    primWidth = width / 2
    primHeight = height/ 2
    primStart = (random.randint(0, primWidth - 1), random.randint(0, primHeight - 1))

    # initialize prim algorithm 
    v = set()

    # initialize vertices
    for i in range(int(primWidth)):
        for j in range(int(primHeight)):
            v.add((i, j))
    u = set([primStart])
    t = []

    # initialize edges
    edges = set()
    for i in v:

        successors = set([(i[0] - 1, i[1]), (i[0] + 1, i[1]), (i[0], i[1] - 1),  (i[0], i[1] + 1)])
        successorsTemp = successors.copy()
        for j in successorsTemp:
            if j[0] < 0 or j[0] > primWidth - 1:
                successors.remove(j)
            
            elif j[1] < 0 or j[1] > primHeight - 1:
                successors.remove(j)
        # add edges
        for j in successors:
            edges.add((i, j))

    # perform prim
    while u != v:
        x = []
        while len(x) == 0:
            a = random.sample(u, 1)[0]
            b = v - u
            for i in edges:
                if i[0] == a:
                    if i[1] in b:


                        x.append(i)
        choice = random.choice(x)
        t.append(choice)
        u.add(choice[1])
    
    # generate cycle
    path = [(1, 0)]
    start = (0, 0)
    prev = start
    curr = (1, 0)
    # search loop
    while curr != start:
        
        primVertex = (curr[0] // 2, curr[1] // 2)
        location = (curr[0] % 2, curr[1] % 2)

        # grab minimum spanning tree edges
        primSuccessors = set([(primVertex[0] - 1, primVertex[1]), (primVertex[0] + 1, primVertex[1]), (primVertex[0], primVertex[1] - 1),  (primVertex[0], primVertex[1] + 1)])
        
        edges = set()
        
        for i in primSuccessors:
            if (primVertex, i) in t:
                edges.add((primVertex, i))

            elif (i, primVertex) in t:
                edges.add((i, primVertex))


        # look at successive nodes
        successors = set([(curr[0] - 1, curr[1]), (curr[0] + 1, curr[1]), (curr[0], curr[1] - 1),  (curr[0], curr[1] + 1)])
        successorsTemp = set([(curr[0] - 1, curr[1]), (curr[0] + 1, curr[1]), (curr[0], curr[1] - 1),  (curr[0], curr[1] + 1)])

        # first, remove the previous vertex
        if prev in successors:
            successors.remove(prev)
            successorsTemp.remove(prev)

        # rule out successors
        for i in successorsTemp:
            # check if its a bound:
            if i[0] < 0 or i[0] > width -1 :
                successors.remove(i)

            elif i[1] < 0 or i[1] > height -1 :
                successors.remove(i)

        # location-specific checking

        # if topLeft:
        if location == (0, 0):

            # try to rule out moving left
            if (((primVertex[0] -1, primVertex[1]), primVertex) not in edges) and ((primVertex, (primVertex[0] -1, primVertex[1])) not in edges):
                if (curr[0] - 1, curr[1]) in successors:
                    successors.remove((curr[0] - 1, curr[1]))

            # try to rule out moving right
            if (((primVertex[0], primVertex[1] - 1), primVertex) in edges) or ((primVertex, (primVertex[0], primVertex[1] - 1)) in edges):
                if (curr[0] + 1, curr[1]) in successors:
                    successors.remove((curr[0] + 1, curr[1]))

            # try to rule out moving up
            if (((primVertex[0], primVertex[1] - 1), primVertex) not in edges) and  ((primVertex, (primVertex[0], primVertex[1] - 1)) not in edges):
                if (curr[0], curr[1] - 1) in successors:
                    successors.remove((curr[0], curr[1] - 1))

            # try to rule out moving down
            if (((primVertex[0] -1, primVertex[1]), primVertex) in edges) or ((primVertex, (primVertex[0] -1, primVertex[1])) in edges):
                if (curr[0], curr[1] + 1) in successors:
                    successors.remove((curr[0], curr[1] + 1))

         # if topRight
        elif location == (1, 0):
            # try to rule out moving left
            if (((primVertex[0], primVertex[1] - 1), primVertex) in edges) or ((primVertex, (primVertex[0], primVertex[1] - 1)) in edges):
                if (curr[0] - 1, curr[1]) in successors:
                    successors.remove((curr[0] - 1, curr[1]))

            # try to rule out moving right
            if (((primVertex[0] + 1, primVertex[1]), primVertex) not in edges) and ((primVertex, (primVertex[0] + 1, primVertex[1])) not in edges):
                if (curr[0] + 1, curr[1]) in successors:
                    successors.remove((curr[0] + 1, curr[1]))

            # try to rule out moving up
            if (((primVertex[0], primVertex[1] - 1), primVertex) not in edges) and  ((primVertex, (primVertex[0], primVertex[1] - 1)) not in edges):
                if (curr[0], curr[1] - 1) in successors:
                    successors.remove((curr[0], curr[1] - 1))

            # try to rule out moving down
            if (((primVertex[0] + 1, primVertex[1]), primVertex) in edges) or ((primVertex, (primVertex[0] + 1, primVertex[1])) in edges):
                if (curr[0], curr[1] + 1) in successors:
                    successors.remove((curr[0], curr[1] + 1))

        # if bottomRight:
        elif location == (1, 1):
            # try to rule out moving left
            if (((primVertex[0], primVertex[1] + 1), primVertex) in edges) or ((primVertex, (primVertex[0], primVertex[1] + 1)) in edges):
                if (curr[0] - 1, curr[1]) in successors:
                    successors.remove((curr[0] - 1, curr[1]))

            # try to rule out moving right
            if (((primVertex[0] + 1, primVertex[1]), primVertex) not in edges) and ((primVertex, (primVertex[0] + 1, primVertex[1])) not in edges):
                if (curr[0] + 1, curr[1]) in successors:
                    successors.remove((curr[0] + 1, curr[1]))

            # try to rule out moving up
            if (((primVertex[0] + 1, primVertex[1]), primVertex) in edges) or  ((primVertex, (primVertex[0]+ 1, primVertex[1])) in edges):
                if (curr[0], curr[1] - 1) in successors:
                    successors.remove((curr[0], curr[1] - 1))

            # try to rule out moving down
            if (((primVertex[0], primVertex[1] + 1), primVertex) not in edges) and ((primVertex, (primVertex[0], primVertex[1] + 1)) not in edges):
                if (curr[0], curr[1] + 1) in successors:
                    successors.remove((curr[0], curr[1] + 1))

        # if bottomLeft
        elif location == (0, 1):
            # try to rule out moving left
            if (((primVertex[0] - 1, primVertex[1]), primVertex) not in edges) and ((primVertex, (primVertex[0] - 1, primVertex[1])) not in edges):
                if (curr[0] - 1, curr[1]) in successors:
                    successors.remove((curr[0] - 1, curr[1]))

            # try to rule out moving right
            if (((primVertex[0], primVertex[1] + 1), primVertex) in edges) or ((primVertex, (primVertex[0], primVertex[1] + 1)) in edges):
                if (curr[0] + 1, curr[1]) in successors:
                    successors.remove((curr[0] + 1, curr[1]))

            # try to rule out moving up
            if (((primVertex[0]- 1, primVertex[1]), primVertex) in edges) or ((primVertex, (primVertex[0] - 1, primVertex[1])) in edges):
                if (curr[0], curr[1] - 1) in successors:
                    successors.remove((curr[0], curr[1] - 1))

            # try to rule out moving down
            if (((primVertex[0], primVertex[1] + 1), primVertex) not in edges) and ((primVertex, (primVertex[0], primVertex[1] + 1)) not in edges):
                if (curr[0], curr[1] + 1) in successors:
                    successors.remove((curr[0], curr[1] + 1))

        '''
        screen.fill(green, [(curr[0] + 1) * block_size + gap_size , (curr[1] + 1) * block_size + 1, block_size-gap_size * 2, block_size-gap_size * 2])
        screen.fill(green, [(prev[0] + 1) * block_size + gap_size , (prev[1] + 1) * block_size + 1, block_size-gap_size * 2, block_size-gap_size * 2])

        previous = prev
        i = curr
        x = i[0] - previous[0]
        y = i[1] - previous[1]
        

        # fill in gaps horizontally 
        if x > 0:
            screen.fill(green, [(i[0]+ 1) * block_size - gap_size, (i[1] + 1) * block_size + gap_size, gap_size * 2, block_size - gap_size *2 ])
        if x < 0:
            screen.fill(green, [(previous[0] + 1) * block_size - gap_size, (previous[1] + 1) * block_size + gap_size, gap_size * 2, block_size - gap_size * 2])

        # fill in gaps vertically

        if y > 0:
            screen.fill(green, [(i[0] + 1) * block_size + gap_size, (i[1] + 1) * block_size - gap_size, block_size-gap_size * 2, gap_size * 2])
        if y < 0:
            screen.fill(green, [(previous[0] + 1) * block_size + gap_size, (previous[1] + 1) * block_size - gap_size, block_size-gap_size * 2, gap_size* 2])
        # update the previous
        previous = i




        pygame.display.flip()
        '''
        
        prev = curr
        curr = list(successors)[0]
        path.append(curr)



    return path


            

        
        
        

            



        
        




"""screen.fill(white)
for i in x:
        screen.fill(green, [(i[0] + 1) * block_size + 10 , (i[1] + 1) * block_size + 10, block_size-10 * 2, block_size-10 * 2])
        screen.fill(green, [(i[0] + 1) * block_size + 10 , (i[1] + 1) * block_size + 10, block_size-10 * 2, block_size-10 * 2])
        pygame.display.flip()
        clock.tick(5)


"""
'''
x = hamiltonian(width, height)
running = True
print("done")
clock.tick(10)
while running:
    for event in pygame.event.get():

        # allows player to close window
        if event.type == pygame.QUIT:
            running = False
            alive = False

'''

