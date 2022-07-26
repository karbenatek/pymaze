from random import randint
from time import sleep
import tkinter as tk
import numpy as np

def xys_to_dir( x0,y0,x1,y1):
    match x1-x0:
        case  1:return 1
        case -1:return 3
        case 0:
            match y1 - y0:
                case  1:return 0
                case -1:return 2

def xy_movein_dir(dir,x,y):
    match dir:
        case 0:
            y = y + 1
        case 1:
            x = x + 1
        case 2:
            y = y - 1
        case 3:
            x = x - 1
    return (x,y)
#
# class cell:
#
#     def __init__(self, sides = [ False, False, False, False] ):
#         self.sides = sides
#
#     #op: False - clear, True - build
#     def wall(self,  op = False, sides = (0,1,2,3)):
#         for side in sides:
#             self.sides[side] = op




class maze:
    #class cell:

        # def __init__(self, sides=[False, False, False, False]):
        #     self.sides = sides
        #
        # # op: False - clear, True - build
        # def wall(self, op=False, sides=[]):
        #     for side in sides:
        #         self.sides[side] = op


    def __init__(self, M = [], w = 10, h = 10):


        if M == []:
            self.w = w
            self.h = h
            M = np.array([[[False, False, False, False]]*self.h for _ in range(self.w)])
        else:
            self.w = len(M)
            self.h = len(M[0])
        self.M = M
        self.visited = []

    def getcell(self, x,y):
        return self.M[x][y]

    def setcell(self, x,y, op = False, sides=[] ):

        print('cell (%i,%i) ->' % (x, y), self.M[x][y])
        print('setting up cell (%i,%i)'%(x,y))
        if sides != []:
            self.M[x][y] = []


        print('cell (%i,%i) ->'%(x,y), self.M[x][y] )
    def blank(self):


        for x in range(self.w):
             for y in range(self.h):
                 self.M[x][y] = [False, False, False, False]
    def getfreedirs(self, x, y):
        dirs_free = []
        dirs_unv = []
        for dir in range(4):
            if not self.M[x][y][dir]:
                dirs_free.append(dir)
                if (xy_movein_dir(dir,x,y)) not in self.visited:
                    dirs_unv.append(dir)

        return (dirs_free,dirs_unv)

    def gen_rdfs( self, draw_visited=False): #randomized depth-first search

        n = 0
        self.visited = []
        #     print(*line[side])
        y = randint(0,self.h-1)
        x = randint(0,self.w-1)
        x,y = 2,2
        self.pos = self.canv.create_oval(x * self.cell_size, y * self.cell_size, (x + 1) * self.cell_size,
                                         (y + 1) * self.cell_size)

        while True:
            if len(self.visited) == self.w * self.h: break
            dirs_free = []

            if n == 70:
                break
            elif n%5==4:
                for j in range(self.w):
                    for i in range(self.h):

                        self.draw_cell(j,i)

            for dir in range(4):
                x_s,y_s = xy_movein_dir(dir, x, y)
                xy_s = (x_s,y_s)

                if 0 <= x_s and x_s < self.w and 0 <= y_s and y_s < self.h:
                    # print(self.M[x_s][y_s])
                    if True not in self.M[x_s][y_s] and xy_s not in self.visited:


                        dirs_free.append(dir)
                    else:
                        if self.M[x_s][y_s][(dir+2)%4]:self.M[x][y][dir] = True
                            # self.M[x][y][dir] = True
                else:
                    self.M[x][y][dir] = True



            #     #print(self.getcell(x, y)[i])

            # print(self.M[x][y])


            if dirs_free != []:
                dir_i = randint(0, len(dirs_free)-1)
                print('DIGGER: free directions:', dirs_free,'...\nThe chosen one is:', dirs_free[dir_i])

                if self.M[x][y][dirs_free[dir_i]]:
                    self.M[x][y][dirs_free[dir_i]] = False
                    self.M[x_prev][y_prev][(dirs_free[dir_i]+2)%4] = False

                x_prev, y_prev = x, y

                (x, y) = xy_movein_dir(dirs_free.pop(dir_i), x, y)
                print(x_prev,y_prev,"->",x,y)

                for dir in dirs_free:
                    self.M[x_prev][y_prev][dir] = True

            else:

                (dirs_free, dirs_unv) = self.getfreedirs(x,y)

                x_pp,y_pp =x_prev,y_prev
                x_prev, y_prev = x, y
                if len(dirs_unv) == 0:

                    self.canv.delete('vis','adit')
                    sleep(1)
                    break
                match len(dirs_free):
                    case 0: break
                    case 1:

                        self.visited.append((x_prev,y_prev))
                        x, y = xy_movein_dir(dirs_free.pop(), x, y)

                        if draw_visited:
                            self.canv.create_rectangle((x_prev+0.2)*self.cell_size,
                                                       (y_prev+0.2)*self.cell_size,
                                                       (x_prev+0.8)*self.cell_size,
                                                       (y_prev+0.8)*self.cell_size,
                                                       fill="grey",tag='vis')

                    case 2:

                        for dir in dirs_free:
                            if (xy_movein_dir(dir,x_prev,y_prev)) not in self.visited:
                                x, y = xy_movein_dir(dir, x_prev, y_prev)
                                if len(dirs_unv) == 1:
                                    if draw_visited:
                                        self.canv.create_rectangle((x_prev + 0.2) * self.cell_size,
                                                                   (y_prev + 0.2) * self.cell_size,
                                                                   (x_prev + 0.8) * self.cell_size,
                                                                   (y_prev + 0.8) * self.cell_size,
                                                                   fill="grey",tag='vis')
                                    self.visited.append((x_prev,y_prev))

                    case _:
                        n_visited = 0

                        for dir in dirs_free:

                            if xy_movein_dir(dir, x_prev, y_prev) not in self.visited and xy_movein_dir(dir, x_prev, y_prev) != (x_pp,y_pp):
                                x, y = xy_movein_dir(dir, x_prev, y_prev)
                            else:
                                n_visited += 1



                        if len(dirs_free)-n_visited == 1:
                            if draw_visited:
                                self.canv.create_rectangle((x_prev + 0.2) * self.cell_size,
                                                           (y_prev + 0.2) * self.cell_size,
                                                           (x_prev + 0.8) * self.cell_size,
                                                           (y_prev + 0.8) * self.cell_size,
                                                           fill="grey", tag='vis')
                            self.visited.append((x_prev, y_prev))

                print('RETURNATOR: Free dirs:', dirs_free,'\nCoord =',x,y,'\nVisited:',self.visited,'\nFree cells:')
                for dir in dirs_free:
                    print(*xy_movein_dir(dir,x,y))
            # print(self.M[x_prev][y_prev][xys_to_dir(x_prev,y_prev,x,y)])


            self.draw_cell(x_prev,y_prev)
            self.canv.coords( self.pos ,x * self.cell_size, y * self.cell_size, (x+1) * self.cell_size, (y+1) * self.cell_size )
            # self.canv.create_rectangle(x)
            # sleep(0.05)

    def solve(self,x0,y0,x1,y1):

        self.flood = np.array([[None]*self.h for _ in range(self.w)])
        self.flood[x0][y0] = 0
        i = 0
        run=True
        while run:
            input('...:')
            i +=1

            for y in range(self.h):
                for x in range(self.w):
                    if self.flood[x][y] != None:
                        self.flood[x][y] += 1

            for y in range(self.h):
                for x in range(self.w):
                    dirs_free = []
                    for dir in range(4):
                        x_s, y_s = xy_movein_dir(dir, x, y)
                        if 0 <= x_s < self.w and 0 <= y_s < self.h:


                            if self.flood[x_s][y_s] == None and not self.M[x][y][dir]:
                                if self.flood[x][y] == 1:
                                    self.flood[x_s][y_s] = 0
                                    self.canv.create_line(  (x+0.5) * self.cell_size,
                                                            (y+0.5) * self.cell_size,
                                                            (x_s+0.5) * self.cell_size,
                                                            (y_s+0.5) * self.cell_size,
                                                            fill= '#aaaaff',tag="floor",width=4)

                                    self.main.update()
                                    if (x1,y1) == (x_s,y_s): run = False
            for y in range(self.h):
                for x in range(self.w):
                    if self.flood[x][y] != None:
                        print("%3i  " %(self.flood[x][y]),end="")
                    else:
                        print(' --- ',end="")
                print('')
            sleep(0.1)

            # for id in self.canv.find_withtag('floor')
            #         id.fill()
        self.canv.delete('floor')
        sleep(1)
        x,y = x1,y1
        while (x,y) != (x0,y0)  in range(i):

            for dir in range(4):
                x_s,y_s = xy_movein_dir(dir,x,y)
                if 0 <= x_s < self.w and 0 <= y_s < self.h:
                    if self.flood[x_s][y_s] > self.flood[x][y]:
                        self.canv.create_line((x + 0.5) * self.cell_size,
                                              (y + 0.5) * self.cell_size,
                                              (x_s + 0.5) * self.cell_size,
                                              (y_s + 0.5) * self.cell_size,
                                              fill='green', tag="shortest")
                        x,y = x_s,y_s
            self.main.update()

        self.main.update()



    def draw_init(self,cell_size=50):
        self.cell_size = cell_size
        self.main = tk.Tk()
        self.main.geometry('%ix%i' %(self.cell_size*self.w+1, self.cell_size*self.h+1))
        self.canv = tk.Canvas( self.main, width = self.w*self.cell_size, height = self.h*self.cell_size, background='white')
        self.canv.pack()
    def draw_cell(self,x,y, redraw = True):
        line = ( ( x * self.cell_size +1,      (y) * self.cell_size +1,   (x+1) * self.cell_size -1, (y) * self.cell_size +1),
                 ( (x) * self.cell_size +1,    (y) * self.cell_size +1,   (x) * self.cell_size +1,   (y+1) * self.cell_size -1),
                 ( x * self.cell_size +1,      (y+1) * self.cell_size -1, (x+1) * self.cell_size -1, (y+1) * self.cell_size -1),
                 ( (x+1) * self.cell_size -1,  y * self.cell_size +1,     (x+1) * self.cell_size -1, (y+1) * self.cell_size -1))

        for side in range(4):
            if (0, 0) <= (x,y) and (x,y) < (self.w, self.h):
                if self.M[x][y][(side+2)%4]:
                    self.canv.create_line(*line[side], fill='black',tag='cell')
                elif redraw:
                    self.canv.create_line(*line[side], fill='white',tag='cell')
                # if self.M[x][y][side] == True:
                #     self.canv.create_line(*line[side], fill='black')
                #
                # elif self.M[x][y][(side+2)%4] == False:
                #     self.canv.create_line(*line[side], fill='white')

            else:
                self.canv.create_line(*line[side], fill='black',tag='cell')


        self.main.update()

maze = maze(w= 15, h= 10)
maze.blank()
maze.draw_init(cell_size=26)
sleep(0.5)
maze.gen_rdfs(draw_visited=True)

# print('cans objcts IDs:',maze.canv.find_all())
# for id in maze.canv.find_withtag('vis'):
#     maze.canv.delete()
maze.canv.delete('vis','cell')
maze.main.update()

# maze.M[x][y] = [True, True, False, False]

# maze.M[x][y].wall(True, [2,3])
# maze.M[x][y].wall(True,[2,1])
for x in range(maze.w):

    for y in range(maze.h):
        # print('cell (%i, %i) ->' %(x,y),maze.getcell(x,y))
        # maze.M[x][y].sides = [True, False, True, False]

        maze.draw_cell(x,y,redraw = False)
maze.main.update()

maze.solve(0,0, maze.w - 1, maze.h -1)

maze.main.update()
sleep(15)
maze.main.quit()


#
# print(len(maze.M))
# print('cell 0,0:',maze.getcell(0,0))