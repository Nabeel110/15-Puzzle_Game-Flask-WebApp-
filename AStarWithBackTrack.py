import random
import numpy as np
from anytree import Node as ATNode
from graphviz import Digraph
import os
from anytree.dotexport import RenderTreeGraph

os.environ["PATH"] += os.pathsep +'.heroku-buildpack-graphviz/usr/bin'

class Node:

    def __init__(self, data, level, fval):

        self.data = data
        self.level = level
        self.fval = fval

    def find(self, mat, x):

        ind = np.where(mat == x)
        ind_x = ind[0][0]
        ind_y = ind[1][0]
        return ind_x, ind_y

    def shuffle(self, puz, x1, y1, x2, y2):

        if x2 >= 0 and x2 < 4 and y2 >= 0 and y2 < 4:
            temp_puz = np.copy(puz)
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            return None

    def generate_child(self):

        x, y = self.find(self.data, 0)
        val_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        children = []
        for i in val_list:
            child = self.shuffle(self.data, x, y, i[0], i[1])
            if child is not None:
                child_node = Node(child, self.level + 1, 0)
                children.append(child_node)
        return children

def toStr(arr):

    b = '\n'.join('\t'.join('%d' % x for x in y) for y in arr)
    return b


class Puzzle:

    def __init__(self):

        temp = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
        random.shuffle(temp)
        self.init_arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 14, 12, 0, 13, 10, 15]).reshape(4, 4)
        self.final_arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]).reshape(4, 4)
        self.open = []
        self.closed = []
        self.track = []

    def h(self, start, goal):

        temp = 0
        for i in range(4):
            for j in range(4):
                if start[i][j] != goal[i][j] and start[i][j] != 0:
                    temp += 1
        return temp

    def f(self, start, goal):

        return self.h(start.data, goal) + start.level

    def inList(self, array, list):

        for element in list:
            if np.array_equal(element.data, array):
                return True
        return False

    def inTrack(self, array, track):

        for x in track:
            if np.array_equal(x.name, array):
                return True
        return False

    def find_index(self, at_node, lis):

        arr = at_node.name
        for i in range(len(lis)):
            if np.array_equal(arr, lis[i].name):
                return i
        return -1

    def process(self,initial_state,goal_state):

        print("Goal State:\n")
        print(goal_state)
        print("\nInitial State:\n")
        print(initial_state)
        start = initial_state
        goal = goal_state
        start = Node(start, 0, 0)
        start.fval = self.f(start, goal)
        self.open.append(start)
        print("\n")
        # root = ATNode(self.init_arr) #object of nparray
        # self.track.append(root)
        counter = 0
        while self.open:
            cur = self.open[0]
            dyn_root = ATNode(cur.data)
            if not self.inTrack(dyn_root.name, self.track):
                self.track.append(dyn_root)
            ind = self.find_index(dyn_root, self.track)
            print("")
            print("  | ")
            print(" \\\'/ \n")
            print(cur.data)
            if (self.h(cur.data, goal) == 0):
                print("---------------Achieved!!!---------------")
                break
            for i in cur.generate_child():
                i.fval = self.f(i, goal)
                self.open.append(i)
                if not self.inTrack(i.data, self.track):
                    self.track.append(ATNode(i.data, parent=self.track[ind]))
                    counter+=1
            self.closed.append(cur)
            del self.open[0]

            self.open = [x for x in self.open if not self.inList(x.data, self.closed)]
            self.open.sort(key=lambda x: x.fval, reverse=False)
        #RenderTreeGraph(self.track[0]).to_picture("Gr.png")
        return (self.track[0],counter)
