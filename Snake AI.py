import pygame, random, graph
pygame.init()

#==============================================================================================================================================================
#==============================================================================================================================================================
#==============================================================================================================================================================

# FOR USER- edit parameters

block_size = 50
width  = 34
height = 18
gap_size = 1
food_amount = 1  # amount that the snake increases by every time it eats
ai = True
grap = graph.hamiltonian(width, height)

print("========= HAMILTONIAN PATH FOUND =========")
cycle = {}
for i in grap:
    cycle[i] = grap.index(i)



#==============================================================================================================================================================
#==============================================================================================================================================================
#==============================================================================================================================================================


# initialize clock and screen
clock = pygame.time.Clock()
screen = pygame.display.set_mode([(width+2) * block_size, (height+2) * block_size])

white = [255, 255, 255]
red = [160, 34, 34]
black = [0, 0, 0]
grey = [50, 50, 50]
green = [34, 139, 34]

screen.fill(white)

# directions as integers
stop  = 0
up = 1
right = 2
down = 3
left = 4

# initial state of game
running = True
alive = True
reset = True

direction = stop
start = False

# get all of the available blocks where food can be placed
availableBlocks = set()
for i in range(width):
    for j in range(height):
        if i != grap[-1][0] or j != grap[-1][1]:
            availableBlocks.add((i, j))


food = random.sample(availableBlocks, 1)[0]


# main window loop
while running:

    
    # Inputs
    for event in pygame.event.get():

        # allows player to close window
        if event.type == pygame.QUIT:
            running = False
            alive = False



        # handles keypresses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset = True

                # set the food

                availableBlocks = set()
                for i in range(width):
                    for j in range(height):
                        if i != grap[-1][0] or j != grap[-1][1]:
                            availableBlocks.add((i, j))
                food = random.sample(availableBlocks, 1)[0]

                # start needs to be false so that the game doesnt start immediately
                start = False
            
            if event.key == pygame.K_w:
                # makes sure that going forward then back in 1 step is impossible
                if direction != down:
                    direction = up
                start = True

            if event.key == pygame.K_a:
                # makes sure that going forward then back in 1 step is impossible
                if direction != right:
                    direction = left
                start = True

            if event.key == pygame.K_s:
                # makes sure that going forward then back in 1 step is impossible
                if direction != up:
                    direction = down
                start = True

            if event.key == pygame.K_d:
                # makes sure that going forward then back in 1 step is impossible
                if direction != left:
                    direction = right
                start = True

    
    # on game start or press of r key
    if reset:
        # refresh screen and fill bounds 
        screen.fill(grey)
        screen.fill(black, [0, 0, block_size * (width + 2) , block_size ]) # screen.fill(x coord, y coord, width, height)
        screen.fill(black, [0, 0, block_size , block_size * (height + 2) ])
        screen.fill(black, [block_size * (width + 1), 0, block_size , block_size * (height + 2) ])
        screen.fill(black, [0, block_size * (height + 1), block_size * (width + 2) , block_size ])
        # randomize starting food coordinate and start snake in middle
        won = False
        # dictionary contaiting a snake componnent and its prevous spot
        snakeBody = { grap[-1]: grap[0]}
        head = grap[-1]
        tail = grap[-1]
        prevTail = grap[-2]



        
        
        # if you press w, a, s, d, start
        if start:
            reset = False
            alive = True
    
    # if playing the game
    else:

        if alive == True:
        # process the snakes movement
            

            # if ai turned on, then follow the algorithm
            if ai == True:

                # find the possible next blocks
                successors = set([(snakeBody[head][0] - 1, snakeBody[head][1]), (snakeBody[head][0] + 1, snakeBody[head][1]), 
                (snakeBody[head][0], snakeBody[head][1] - 1), (snakeBody[head][0], snakeBody[head][1] + 1)])

                successorsTemp = set([(snakeBody[head][0] - 1, snakeBody[head][1]), (snakeBody[head][0] + 1, snakeBody[head][1]), 
                (snakeBody[head][0], snakeBody[head][1] - 1), (snakeBody[head][0], snakeBody[head][1] + 1)])
                # if successor out of bounds
                for i in successorsTemp:
                    if i[0]  == width:
                        successors.remove(i)

                    if i[0] < 0:
                        successors.remove(i)

                    if i[1]  == height:
                        successors.remove(i)

                    if i[1] < 0:
                        successors.remove(i)


                # grab next cycle element
                num = cycle[snakeBody[head]]
                for i in successors:
                    ind = cycle[i]
                    if ind == (num + 1) % len(cycle):
                        next = i


                # remove next cycle element

                '''
                successors.remove(cycle[index])

                
                # Find subpaths from head to successor. If its ok, record its length. If not, put -1.
                length = []
                valid = True
                for i in successors:
                 

                    # if successor in snake body
                    if len(snakeBody) > 1:
                        if i in snakeBody:
                            valid = False
                            '''



                
            # otherwise, grab player movement 
            else:

                if direction == up:
                    next = (snakeBody[head][0], snakeBody[head][1] - 1)

                if direction == down:
                    next = (snakeBody[head][0], snakeBody[head][1] + 1)

                if direction == left:
                    next = (snakeBody[head][0] - 1, snakeBody[head][1])

                if direction == right:
                    next = (snakeBody[head][0] + 1, snakeBody[head][1])


            # update the snake head
            head = snakeBody[head]
            

            # update the available blocks for the food
            if head in availableBlocks:

                availableBlocks.remove(head)


            # if the snake ate an apple
            if head == food:
                screen.fill(green, [(tail[0] + 1) * block_size + gap_size , (tail[1] + 1) * block_size + gap_size, block_size-gap_size * 2, block_size-gap_size * 2])
                # Spawn new food if the game isn't won
                if availableBlocks != set():
                    food = random.sample(availableBlocks, 1)[0]

                else:
                    won = True

            # if it didn't eat an apple:
            else:
                prevTail = tail
                tail = snakeBody[tail]
                snakeBody.pop(prevTail, None)
                availableBlocks.add(prevTail)


            
               
                    

            # if the snake hit itself
            if head in snakeBody.keys():

                alive = False
 
            # check if snake hit a wall

            if head[0] < 0:
                alive = False

            if head[0] > width -1:
                alive = False

            if head[1] < 0:
                alive = False

            if head[1] > height - 1:
                alive = False

            # if all good, add the head to the dictionary
            snakeBody[head] = next

        # if dead, do nothing
        if alive == False:
            continue
    

    # first, draw snake body
    screen.fill(grey, [(prevTail[0] + 1) * block_size + gap_size , (prevTail[1] + 1) * block_size + gap_size, block_size-gap_size * 2, block_size-gap_size * 2])
    screen.fill(green, [(head[0] + 1) * block_size + gap_size , (head[1] + 1) * block_size + gap_size, block_size-gap_size * 2, block_size-gap_size * 2])

    
   
    # fill in scoreboard
    #my_font = pygame.font.SysFont('Arcade', 30)
    #text_surface = my_font.render('Score: ' + str(len(snakeBody)), False, (255, 255, 255))
    #screen.blit(text_surface, ((width+1) * block_size /2 - 15 , 40))

    # fill in food if there is food
    if not won:
        screen.fill(red, [(food[0] + 1) * block_size + gap_size , (food[1] + 1) * block_size + gap_size, block_size - gap_size*2, block_size - gap_size * 2])

    # remove gaps at tail
    # fill in gap horizontally 
    previous = prevTail
    i = tail
    x = i[0] - previous[0]
    y = i[1] - previous[1]

    if x > 0:
        screen.fill(grey, [(i[0]+ 1) * block_size - gap_size, (i[1] + 1) * block_size + gap_size, gap_size * 2, block_size - gap_size *2 ])
    if x < 0:
        screen.fill(grey, [(previous[0] + 1) * block_size - gap_size, (previous[1] + 1) * block_size + gap_size, gap_size * 2, block_size - gap_size * 2])

    # fill in gaps vertically

    if y > 0:
        screen.fill(grey, [(i[0] + 1) * block_size + gap_size, (i[1] + 1) * block_size - gap_size, block_size-gap_size * 2, gap_size * 2])
    if y < 0:
        screen.fill(grey, [(previous[0] + 1) * block_size + gap_size, (previous[1] + 1) * block_size - gap_size, block_size-gap_size * 2, gap_size* 2])

################################################################################################################################################################
    # update screen
    pygame.display.flip()

    # fill in gap in head of snake
    # fill in gap horizontally 
    previous = head
    i = snakeBody[head]
    x = i[0] - previous[0]
    y = i[1] - previous[1]

    if x > 0:
        screen.fill(green, [(i[0]+ 1) * block_size - gap_size, (i[1] + 1) * block_size + gap_size, gap_size * 2, block_size - gap_size *2 ])
    if x < 0:
        screen.fill(green, [(previous[0] + 1) * block_size - gap_size, (previous[1] + 1) * block_size + gap_size, gap_size * 2, block_size - gap_size * 2])

    # fill in gaps vertically

    if y > 0:
        screen.fill(green, [(i[0] + 1) * block_size + gap_size, (i[1] + 1) * block_size - gap_size, block_size-gap_size * 2, gap_size * 2])
    if y < 0:
        screen.fill(green, [(previous[0] + 1) * block_size + gap_size, (previous[1] + 1) * block_size - gap_size, block_size-gap_size * 2, gap_size* 2])

    #clock.tick(10)
    

    # if won
    if won:
        alive = False

# Notes: Make sure to make the cycle a dictionary so that cycle index lookup is faster. 
# Also, make sure to check if new head increasing
# make sure to use the doc from https://johnflux.com/2015/05/02/nokia-6110-part-3-algorithms/