import copy
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from graphviz import render , Source
import os



# goal = [[1, 2, 3, 4],
#         [12, 13, 14, 5],
#         [11, 0, 15, 6],
#         [10, 9, 8, 7],
#         ]
# start = [[1, 3, 4, 5],
#         [12, 2, 14, 6],
#         [0, 11, 8, 15],
#         [10,13, 9, 7],
#         ]


def h1(arr,goal):
    h = 0
    i = 0
    j = 0
    while(i<len(arr)):
        j = 0
        while(j<len(arr[0])):

            if(arr[i][j] != goal[i][j]):
                h+=1
            j+=1
        i+=1
    return h




def h2(arr,goal):
    i = 0
    j = 0
    h_sum = 0
    while(i<len(arr)):
        j=0
        while(j<len(arr[0])):
            m = 0
            n = 0
            while(m<len(goal)):
                n=0
                while(n<len(goal[0])):
                    if(arr[i][j] == goal [m][n] and arr[i][j] != 0):

                        h_sum += abs((i-m)) + abs((j-n))
                    #print(goal[m][n])
                    n+=1
                m+=1
            j+=1
        i+=1
    return h_sum





def get_2d_ind(arr,num):
    i = 0
    j = 0
    while (i < len(arr)):
        j = 0
        while (j < len(arr[0])):

            if (arr[i][j] == num):
                return (i,j)
            j += 1
        i += 1

    return -1



def swap(arr,i,j,m,n):
    temp = arr[i][j]
    arr[i][j] = arr[m][n]
    arr[m][n] = temp


def getArrStr(arr):
    arrStr = " "
    for row in arr:
        arrStr += " ".join(map(str, row)) + '\n'

    return arrStr


def best_first_search(start, goal):
    count = 0
    start = start.tolist()
    #path = "BFS Start:--------------\n"
    root = Node(getArrStr(start))
    child = root
    h1_values = {}
    arr_choices = {}
    previous={'up': False, 'down': False, 'right': False, 'left': False}
    h2_values = {}
    while(start != goal):
        ind = get_2d_ind(start, 0)
        i = ind[0]
        j = ind[1]

        if(i-1 >= 0 and not previous['down']):
            #up
            arr_choices['up_arr'] = copy.deepcopy(start)
            swap(arr_choices['up_arr'],i-1,j,i,j)
            h2_values['up'] = h2(arr_choices['up_arr'],goal)
            #h1_values['up'] = h1(arr_choices['up_arr'],goal)

        if (i+1 < len(start) and not previous['up']):
            #down
            arr_choices['down_arr'] = copy.deepcopy(start)
            swap(arr_choices['down_arr'], i + 1, j, i, j)
            h2_values['down'] = h2(arr_choices['down_arr'],goal)
            #h1_values['down'] = h1(arr_choices['down_arr'],goal)


        if (j+1 < len(start[0]) and not previous['left']):
            #right
            arr_choices['right_arr'] = copy.deepcopy(start)
            swap(arr_choices['right_arr'], i, j + 1, i, j)
            h2_values['right'] = h2(arr_choices['right_arr'],goal)
            #h1_values['right'] = h1(arr_choices['right_arr'],goal)


        if (j-1 >= 0 and not previous['right']):
            #left
            arr_choices['left_arr'] = copy.deepcopy(start)
            swap(arr_choices['left_arr'], i, j-1, i, j)
            h2_values['left'] = h2(arr_choices['left_arr'],goal)
            #h1_values['left'] = h1(arr_choices['left_arr'],goal)



        min_h2 = min(h2_values, key=h2_values.get)
        start = arr_choices[min_h2 + '_arr']
        count+=1
        # h1_values = {}
        h2_values = {}
        arr_choices = {}
        previous = {'up': False, 'down': False, 'right': False, 'left': False}
        previous[min_h2] = True

        child = Node(getArrStr(start), parent=child)

    #DotExporter(root).to_dotfile('tree.dot')


    return (root,count)
    #     path += "[\n"
    #     for row in start:
    #         path += str(row)
    #         path += "\n"
    #
    #
    #     path += "]\n\n"
    #
    #     if(start != goal):
    #
    #         path += "|\n"
    #         path += "|\n"
    #         path += "|\n"
    #         path += "V\n\n"
    #
    # path += "BFS End:---------------"



























# import numpy as np
# goal_state = np.array([1,2,3,4,12,13,14,5,11,0,15,6,10,9,8,7]).reshape((4,4))
# arr =  np.array([1,3,4,5,12,2,14,6,11,0,8,15,10,13,9,7]).reshape((4,4))
# # initial_path = initial_path.tolist()
# arr = arr.tolist()
# goal_state =goal_state.tolist()
#
# print(best_first_search(arr,goal_state))
        # DotExporter(root).to_picture("udo.png")
    #     path += "[\n"
    #     for row in start:
    #         path += str(row)
    #         path += "\n"
    #
    #
    #     path += "]\n\n"
    #
    #     if(start != goal):
    #
    #         path += "|\n"
    #         path += "|\n"
    #         path += "|\n"
    #         path += "V\n\n"
    #
    # path += "BFS End:---------------"
