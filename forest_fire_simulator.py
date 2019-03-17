import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PIL import Image as im
import imageio as imo
import scipy as sci
import random as ran
import os
import sys
import matplotlib.cm as cm
from pathlib import Path


def save_picture_as_gray(path_o, path_s):
    color_image = im.open(path_o)
    grey = color_image.convert('L')
    grey.save(path_s)
    return None

def random_fire(array, size_x, size_y, i):
        
    for j in range(i):
        
        while True:
            x = ran.randint(0, size_x-1)
            y = ran.randint(0, size_y-1)
        
            if array[x][y] == 1:
                array[x][y] = 2
                break

    while True:
        x1 = ran.randint(0, size_x-1)
        y1 = ran.randint(0, size_y-1)
        
        if array[x1][y1] == 1:
            array[x1][y1] = 3
            
            return array

def change_trees_health(array0, array_t, size_x, size_y):
    for i in range(size_x):
        for j in range(size_y):
            if array0[i][j] == 2:
                array_t[i][j] += 1
    return array_t

def firefighting(array0, array_t, size_x, size_y):
    array1 = array0 *1

    global changes
    changes = 0

    for i in range(size_x):
        for j in range(size_y):
            if array0[i][j] == 2:
                if ran.random() < effectiveness:
                    array1[i][j] = 1
                    changes += 1

    return array1
    
def next_day(array0, array_t, size_x, size_y, ash_after):
    array1 = array0 *1
        
    s1 = 0
    s2 = 0
    s3 = 0

    global changes

    for i in range(size_x):
        for j in range(size_y):

            if array0[i][j] == 0:
                None
                
            elif array0[i][j] == 1:
                s1 += 1
                
                ip = i + 1
                im = i - 1
                jp = j + 1
                jm = j - 1
                if ip >=size_x:
                    ip = im
                if im < 0:
                    im = ip
                if jp >=size_y:
                    jp = jm
                if jm < 0:
                    jm = jp
      
                if array0[ip][j] == 2 or array0[im][j] == 2 or array0[i][jp] == 2 or array0[i][jm] == 2:
                    if ran.random() < chance_to_ignite:
                        array1[i][j] = 2
                        s2 += 1
                        changes += 1

            elif array0[i][j] == 2:
                if array_t[i][j] > ash_after:
                    array1[i][j] = 3
                    changes += 1
            
            elif array0[i][j] == 3:
                s3 += 1


    
    global y1
    global y2
    global y3

    y1.append(s1)
    y2.append(s2)
    y3.append(s3)
                
    return array1

def show(array, time_interval):
    plt.clf()
    plt.imshow(array, interpolation='nearest', cmap=cm.RdYlGn_r)
    plt.pause(time_interval)

def show_summary_graph():
    plt.clf()
    plt.plot(x1, y1, 'r-', label='flameable')
    plt.plot(x2, y2, 'g-', label='fire')
    plt.plot(x3, y3, 'b-', label='ash')
    plt.legend()
    plt.show()


# STATE OF TREE CELL
# 0 - nonflammable
# 1 - flameable
# 2 - fire
# 3 - ash

print('WELCOME TO THE FOREST FIRE SIMULATOR \n')

current_path = Path.cwd()

#IT MUST BE IN THE SAME LOCATION) 
print('IMAGE NAME (e.g sample.png): ', end="")
file_name = input()
image_path = current_path / file_name
gray_image_path = current_path / str('grey_' + file_name)

try:
    save_picture_as_gray(image_path, gray_image_path)
except Exception as e:
    print('FILE NOT FOUND, PRESS ENTER TO EXIT', end="")
    input()
    sys.exit(22)

threshold = 80

#store state od cell
im_array = (imo.imread(gray_image_path) > threshold).astype(np.uint8)

#dimensions
size_x = im_array.shape[0]
size_y = im_array.shape[1]

#store time of trees on fire
im_array_time = np.zeros(shape = (size_x, size_y), dtype = np.uint8)


#config
print('DATA FILE NAME (e.g data.txt) [0 - TO SET HERE]: ', end="")
data_path = current_path / input()

if(data_path == current_path / '0'):
    print('NUMBER OF INITIAL FIRES: ', end="")
    init_fire_size = int(input())

    print('CHANCE FOR RANDOM IGNITION [%]: ', end="")
    random_fire_chance = float(input()) / 100

    print('AFTER HOW MANY DAYS FOREST TURNS INTO ASH: ', end="")
    ash_after = int(input()) - 1

    print('FIREFIGHTERS EFFECTIVENESS [%]: ', end="")
    effectiveness = float(input()) / 100

    print('CHANCE TO IGNITE THE NEIGHBORING TREE [%]: ', end="")
    chance_to_ignite = float(input()) / 100

    print('MINIMUM TIME INTERVAL BETWEEN CHANGING ANIMATION [MS]: ', end="")
    time_interval = float(input())/1000

else:
    try:
        f = open(data_path,"r")
        
        f_lines = f.readlines()
        di = 0
        tab = []
        
        for x in f_lines:
            e_i = x.find("=")+1
            tab.append(x[e_i:])

        if len(tab) != 6:
            print(di, ' CORRUPT FILE, PRESS ENTER TO EXIT', end="")
            input()
            sys.exit(33)
        else:
            try:
                init_fire_size = int(tab[0])
                random_fire_chance = float(tab[1]) / 100
                ash_after = int(tab[2])
                effectiveness = float(tab[3]) / 100
                chance_to_ignite = float(tab[4]) / 100
                time_interval = float(tab[5])/1000
                print('NUMBER OF INITIAL FIRES: ', init_fire_size)
                print('CHANCE FOR RANDOM IGNITION: ', random_fire_chance*100, "%")
                print('AFTER HOW MANY DAYS FOREST TURNS INTO ASH: ', ash_after)
                print('FIREFIGHTERS EFFECTIVENESS: ', effectiveness*100, "%")
                print('CHANCE TO IGNITE THE NEIGHBORING TREE: ', chance_to_ignite*100, "%")
                print('MINIMUM TIME INTERVAL BETWEEN CHANGING ANIMATION: ', time_interval*1000, "S")
                
            except Exception as e:
                print('WRONG DATA, PRESS ENTER TO EXIT', end="")
                input()
                sys.exit(33)
            
    except Exception as e:
        print('FILE NOT FOUND, PRESS ENTER TO EXIT ', end="")
        input()
        sys.exit(33)

#list for summary
x1 = []
y1 = []

x2 = []
y2 = []

x3 = []
y3 = []

changes = 5
day_counter = 1

#arson of the forest
im_array = random_fire(im_array, size_x, size_y, init_fire_size)

#start animation
plt.ion()
plt.figure()

#main loop
while changes != 0:

    print('DAY ', day_counter)
    show(im_array, time_interval)
        
    x1.append(day_counter)
    x2.append(day_counter)
    x3.append(day_counter)
    
    im_array_time = change_trees_health(im_array, im_array_time, size_x, size_y)
    
    if effectiveness >= 0.0001:
        im_array = firefighting(im_array, im_array_time, size_x, size_y)
    
    if chance_to_ignite >= 0.0001:
        im_array = next_day(im_array, im_array_time, size_x, size_y, ash_after)

    if ran.random() < random_fire_chance:
        im_array = random_fire(im_array, size_x, size_y, init_fire_size)
        
    day_counter += 1
  
print('\nPRESS ENTER TO SHOW SUMMARY GRAPH', end="")
input()
show_summary_graph()

print('PRESS ENTER TO EXIT', end="")
input()
