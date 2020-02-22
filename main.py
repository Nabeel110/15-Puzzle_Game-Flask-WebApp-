from flask import Flask, render_template,url_for, request, redirect
import numpy as np
import puzzle as pz
import AStarWithBackTrack as astar
from IPython.display import Image, display
from anytree.exporter import DotExporter
from graphviz import render , Source
import os
from PIL import Image
from random import shuffle
from math import sqrt
import numpy as np
import random
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["PATH"] += os.pathsep +'.heroku-buildpack-graphviz/usr/bin'
from graphviz import Digraph


Tree_Images = os.path.join('static', 'images')
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = Tree_Images

# ///////////////////// Random state  Method /////////////////////////////

def random_state():

    fin_st = np.array([1, 2, 3, 4, 12, 13, 14, 5, 11, 0, 15, 6, 10, 9, 8, 7]).reshape(4, 4)
    qty = random.randrange(1, 5)
    for i in range(qty):
        ind_zero = np.where(fin_st == 0)
        x = ind_zero[0][0]
        y = ind_zero[1][0]
        mov = random.randrange(1, 4)
        if (i + 1) % 4 == 1:
            range_up = x
            if x - mov < 0:
                mov = range_up
            for j in range(mov):
                fin_st[x][y], fin_st[x - 1][y] = fin_st[x - 1][y], fin_st[x][y]
                x = x - 1
        elif (i + 1) % 4 == 2:
            range_left = y
            if y - mov < 0:
                mov = range_left
            for j in range(mov):
                fin_st[x][y - 1], fin_st[x][y] = fin_st[x][y], fin_st[x][y - 1]
                y = y - 1
        elif (i + 1) % 4 == 3:
            range_down = 3 - x
            if x + mov > 3:
                mov = range_down
            for j in range(mov):
                fin_st[x][y], fin_st[x + 1][y] = fin_st[x + 1][y], fin_st[x][y]
                x = x + 1
        elif (i + 1) % 4 == 0:
            range_rgt = 3 - y
            if y + mov > 3:
                mov = range_rgt
            for j in range(mov):
                fin_st[x][y + 1], fin_st[x][y] = fin_st[x][y], fin_st[x][y + 1]
                y = y + 1

    return fin_st


arr = random_state()
@app.route("/", methods = ['POST', 'GET'])
def home():
    # arr = randomize()
    global arr
    goal_state =np.array([1,2,3,4,12,13,14,5,11,0,15,6,10,9,8,7]).reshape((4,4))
    # goal_state = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]).reshape((4,4))

    if 'random' in request.form:
        arr = random_state()
        return render_template('test.html',arr=arr)
    elif 'custom' in request.form:
        var  = request.form['textbox']
        ls = var.split(',')
        results = list(map(int, ls))
        arr = np.array(results).reshape((4,4))
        print("arr",arr)
        goal_state = goal_state.tolist()
        return render_template('test.html',arr=arr)


    #
    if request.form.get('bfs') == '1' and request.form['search'] == 'find':
        # arr = arr.tolist()
        goal_state = goal_state.tolist()
        print('Goal State :', goal_state)
        path , count = pz.best_first_search(arr,goal_state)
        print(path)
        DotExporter(path).to_picture("static/images/tree.png")
        make_transparent()
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'tree2.png')
        print(full_filename)
        return render_template('test.html', tree=full_filename , arr = goal_state, count = count)


    if request.form.get('bfs') == '2' and request.form['search'] == 'find':
        # arr =  np.array([1,3,4,5,12,2,14,6,11,0,8,15,10,13,9,7]).reshape((4,4))
        arr = np.array(arr)
        Puzzle1 = astar.Puzzle()
        path,counter = Puzzle1.process(arr,goal_state)
        print(path)
        DotExporter(path).to_picture("static/images/tree.png")
        # make_transparent()
        fname = os.path.join(app.config['UPLOAD_FOLDER'], 'tree.png')
        print(fname)
        # im = Image(path.create_png())
        # display(im)
        return render_template('test.html', tree= fname, arr= goal_state, count = counter)


        # pass # do something
    # elif 'watch' in request.form:
        # pass # do something else
    return render_template('test.html', arr= arr)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


def make_transparent():
    img = Image.open('static/images/tree.png')
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save('static/images/tree2.png', "PNG")

def randomize():
    arr = np.arange(16).reshape((4, 4))
    np.random.shuffle(arr)
    return arr

@app.before_request
def before_request():
    # When you import jinja2 macros, they get cached which is annoying for local
    # development, so wipe the cache every request.
    if 'localhost' in request.host_url or '0.0.0.0' in request.host_url:
        app.jinja_env.cache = {}


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)
