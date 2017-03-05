import telnetlib
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import re
###Notes from Felica###
#b'+9.90000000E+37\r\n'
#+9.90000000E+37
#This is the open circuit value for any measurements
#Set multimeter to DHCP and hard reset.
#Might have to change the IP to closer to your computer IP.

multimeter_address ="10.30.128.155"
#setup telnet
multimeter = telnetlib.Telnet()
#initialize the multimeter with the given settings
multimeter.open(multimeter_address,port=3490,timeout=3)
#set the multimeter into remote mode
multimeter.write(("SYST:REM\n").encode('ascii'))
multimeter.write(("CONF:SCAL:RES\n").encode("ascii"))




fig1=plt.figure()
start=time.time()
voltage=[0]
t=[1]

line,=plt.plot(t,voltage,'r-')
print('start :  {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
# print(start)

def update(x):
    multimeter.write(("READ?\n").encode("ascii"))
    time.sleep(0.001)
    # multimeter.write("*TRIG\n")
    value= multimeter.read_eager()
    value = value.decode("ascii")
    # print(value)
    value = value.replace("\r\n","")

    # print(type(float(value)))
    try:
        print(float(value),",",time.time()-start)
        voltage.append(float(value))
        t.append(time.time()-start)
    except Exception as e:
        print("couldnt append data values:\n",e)

    line.set_data(t,voltage)
    plt.xlim(0, max(t)*1.1)
    plt.ylim(min(voltage), max(voltage)*1.1)
    return line,




try:

    line_ani = animation.FuncAnimation(fig1, update, interval=1000)
    plt.show()
except KeyboardInterrupt:

    multimeter.close()

print('end   :  {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

#saves a final figure
fig=plt.figure()
ax1=plt.subplot(111)
ax1.plot(t,voltage,'-r')
ax1.set_title('start :  {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()), fontsize=10, y=1.05)
ax1.set_xlabel("Time (s)", fontsize=10)
ax1.set_ylabel("Voltage (V)", fontsize=10)
plt.savefig("test.png")
#closes the multimeter
multimeter.close()
