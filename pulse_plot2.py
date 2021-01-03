import matplotlib.pyplot as plt
import numpy as np
import time
import time, random
import math
import serial
from collections import deque
from scipy import signal



#Display loading 
class PlotData:
    def __init__(self, max_entries=30):
        self.axis_x = deque(maxlen=max_entries)
        self.axis_y = deque(maxlen=max_entries)
        self.axis_y1 = deque(maxlen=max_entries)
    def add(self, x, y):
        self.axis_x.append(x)
        self.axis_y.append(y)
        self.axis_y1.append(y-np.mean(self.axis_y))
#z domain
a=[1]
p =[]
for i in range(50):
    p.append(1/50)
for i in range(49):
    a.append(0)
angle = np.linspace(-np.pi, np.pi, 50)
cirx = np.sin(angle)
ciry = np.cos(angle)
plt.figure(figsize=(8,8))
plt.plot(cirx, ciry,'k-')

a1 = np.roots(p)
a2 = np.roots(a)

plt.plot(np.real(a1), np.imag(a1), 'o', markersize=12)
plt.plot(np.real(a2), np.imag(a2), 'x', markersize=12)
plt.text(0.15,0.15,'49')
plt.grid()

plt.xlim((-2, 2))
plt.xlabel('Real')
plt.ylim((-2, 2))
plt.ylabel('Imag')
    


        
        
#initial
fig, (ax,ax2,ax3,ax4,ax5) = plt.subplots(5,1)
line,  = ax.plot(np.random.randn(100))
line2, = ax2.plot(np.random.randn(100))
line3, = ax3.plot(np.random.randn(100))
line4, = ax4.plot(np.random.randn(100))
line5, = ax5.plot(np.random.randn(100))
plt.show(block = False)
plt.setp(line2,color = 'r')
x=np.linspace(-50,50,500)


PData= PlotData(500)
ax.set_ylim(0,1000)
ax2.set_ylim(-10,10)
ax3.set_ylim(0,150)
ax4.set_ylim(-5,5)
ax5.set_ylim(0,150)


# plot parameters
print ('plotting data...')
# open serial port
strPort='com4'
ser = serial.Serial(strPort, 115200)
ser.flush()

start = time.time()
fs = 250
w_hat = np.arange(-np.pi, np.pi, np.pi/fs)
timeslot=0
currentuptime = 0
lastuptime = 0
global slope
i=1
while (True):
    
    for ii in range(10):

        try:
            data = float(ser.readline())
            PData.add(time.time() - start, data)
        except:
            pass
        
    if(len(PData.axis_y1)==500):
        y1f = np.fft.fftshift(np.fft.fft(PData.axis_y1))
        y_fir =signal.lfilter(p, 1, PData.axis_y1)
        y2f = np.fft.fftshift(np.fft.fft(y_fir))
        if(i==1):
            slope = -1
            i=0
        if(y_fir[499]-y_fir[498]<0):
            if(slope == 1):
                timeslot = currentuptime-lastuptime
                lastuptime = currentuptime
                if((60*1/timeslot)<120 and (int(60*1/timeslot)>0)):
                    print('heartbeat: '+ str(int(60*1/timeslot)))
            slope = -1
            
        elif(y_fir[499]-y_fir[498]>0):
            slope =1
            currentuptime = time.time()
        else:
            slope = 0
        

    ax.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    ax2.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    ax3.set_xlim(-250, 250)
    ax4.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    ax5.set_xlim(-250, 250)
    line.set_xdata(PData.axis_x)
    line.set_ydata(PData.axis_y)
    line2.set_xdata(PData.axis_x)
    line2.set_ydata(PData.axis_y1)
    
    if(len(PData.axis_y1)>=500):
        line3.set_xdata(x)
        line3.set_ydata(abs(y1f))
        line4.set_xdata(PData.axis_x)
        line4.set_ydata(y_fir)
        line5.set_xdata(x)
        line5.set_ydata(abs(y2f))
    
    fig.canvas.draw()
    fig.canvas.flush_events()
