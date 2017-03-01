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



fig=plt.figure()


start=time.time()
voltage=[0]
t=[1]

line,=plt.plot(t,voltage,'r-')
print('start :  {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
print(start)

def update(x):
    multimeter.write(("MEAS:VOLT:DC?\n").encode("ascii"))
    value= multimeter.read_eager()
    value = value.decode("ascii")
    value = re.search(r'\d.{13}', value)

    # print(type(float(value)))
    try:
        if value==None:
            #checks for an unmatching string, usually ''
            voltage.append(0)
        elif float(value.group(0))>1000:
            #checks to make sure the overload isnt reached. overload = 9.9E37
            voltage.append(0)
        else:
            print(value.group(0),time.time()-start)
            voltage.append(float(value.group(0)))
        t.append(time.time()-start)
    except Exception as e:
        print("couldnt append data values:\n",e)

    line.set_data(t,voltage)
    plt.xlim(0, max(t)*1.1)
    plt.ylim(0, max(voltage)*1.1)
    return line,




try:
    line_ani = animation.FuncAnimation(fig, update, interval=1000)
    plt.show()
except KeyboardInterrupt:

    multimeter.close()

print('end   :  {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
#closes the multimeter
multimeter.close()
