import serial
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from collections import deque
import statistics
import json

import multiprocessing

from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler

from flask import Flask, render_template, jsonify
app = Flask(__name__)

numberArray = [1,2,3,4]


print("Start")
port="/dev/tty.HC-06-DevB" #This will be different for various devices and on windows it will probably be a COM port.
bluetooth=serial.Serial(port, 9600)#Start communications with the bluetooth unit
print("Connected")
bluetooth.flushInput() #This gives the bluetooth a little kick


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/numbers')
def getNumbers():
    f = open('numbers.txt', 'r')
    x = f.read().split(',')
    f.close()
    return jsonify(x)

@app.route('/startprocess')
def startProcess():

    return 200

'''
class Serv(BaseHTTPRequestHandler):

    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        BaseHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        print(self)
        if self.path == '/':
            self.path = '/index.html'
        if self.path != '/testing':
            print("wrong place")
            try:
                file_to_open = open(self.path[1:]).read()
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.send_header('Access-Control-Allow-Origin', '*')
            #super(Serv, self).end_headers(self)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))
        else:
            print("Logging testing")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header('Content-type', 'application/json')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(json.dumps({'hello': 'world', 'received': 'ok'}), 'utf-8'))

'''




def getDistance():
    distance = 0
    try:
        input_data = bluetooth.readline()
        distance = round(float(input_data.decode()))
    except:
        print("Failed to convert distance")
    return distance

# Parameters
x_len = 200         # Number of points to display
y_range = [0, 256]  # Range of possible Y values to display

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, 200))
ys = [0] * x_len
ax.set_ylim(y_range)


# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys)

# Add labels
plt.title('Distance over Time')
plt.xlabel('Samples')
plt.ylabel('Distance (mm)')

distances = deque(10 * [0], 10)

def meanDistance():
    global distances
    distances.pop()
    distances.appendleft(getDistance())
    tot = distances.__getitem__(0) + distances.__getitem__(1) + distances.__getitem__(2) + distances.__getitem__(3) + distances.__getitem__(4) + distances.__getitem__(5) + distances.__getitem__(6) + distances.__getitem__(7) + distances.__getitem__(8) + distances.__getitem__(9)
    print(distances)
    med = statistics.median(list(distances))
    avg = tot//10
    print("avg: " + str(avg))
    print("med: " + str(med))
    return med



# This function is called periodically from FuncAnimation
def animate(i, ys):

    y = meanDistance()


    # Add y to list
    ys.append(y)

    # Limit y list to set number of items
    ys = ys[-x_len:]

    # Update line with new Y values
    line.set_ydata(ys)

    return line,

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig,
    animate,
    fargs=(ys,),
    interval=50,
    blit=True)

def startServer():
    app.run(host='0.0.0.0', port=80)
    '''
    httpd = HTTPServer(('localhost', 8000), Serv)
    httpd.serve_forever()
    '''


def startPlotting():
    i = 0
    f = open('numbers.txt', 'w')
    while i < 100:
        med = meanDistance()
        f.write(',')
        f.write('{}'.format(med))
        i += 1
    x = f.read().split(',')
    f.close()
    print(x)
    #plt.show()





def main():
    pool = multiprocessing.Pool(processes=4)
    pool.apply_async(startServer)
    res = pool.apply_async(startPlotting)
    print(res)
    pool.close()
    pool.join()



main()


#input_data = bluetooth.readline()
#print(input_data.decode())


