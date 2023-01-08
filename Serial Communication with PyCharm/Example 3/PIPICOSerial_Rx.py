# PyCharm: Plot DHT22 Sensor

# Additional Library
#    - pyserial, numpy, matplotlib

import serial
import time
#import matplotlib
import matplotlib.pyplot as plt
import numpy as np
#matplotlib.use("tkAgg")

# Serial Communication
pipico = serial.Serial(port='COM9', baudrate=115200)
pipico.flushInput()

# Matplotlib
plot_window = 20
y_varT = np.array(np.zeros([plot_window]))
y_varH = np.array(np.zeros([plot_window]))
plt.ion()
fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('DHT 22 Sensor')
ax1.set_xlabel('Sample')
ax1.set_title('Temperature (°C)')
ax1.set_ylabel('°C')
ax2.set_xlabel('Sample')
ax2.set_title('Humidity (%)')
ax2.set_ylabel('%')
lineT, = ax1.plot(y_varT)
lineH, = ax2.plot(y_varH)

# To "" or Not!
chkData = 0
savData = 1
pltData = 1

'''
# Uncomment This if Need to Create New File Name
if savData:
    print("Enter New File Name:")
    var = str(input())
    f = open(var + ".txt", "a")
'''
while True:
    try:
        # Read the Data with \n
        rx_byte = pipico.readline()
        #rx_byte_dec = float(rx_byte[0:len(rx_byte)].decode("utf-8"))
        rx_byte_dec = rx_byte.decode()
        # Example Our Data: 26.7,77.9
        temperature = rx_byte_dec[0:len(rx_byte)-6]
        humidity = rx_byte_dec[5:len(rx_byte)]

        # Check the Data
        if chkData:
            print(rx_byte_dec)
            print(temperature)
            print(humidity)

        # Save the Data
        if savData:
            f = open("test_data.txt", "a")
            # Uncomment below if Need to Create New File Name
            # f = open(var + ".txt", "a")
            sec = time.time()
            loc_time = time.ctime(sec)
            f.write(str(loc_time)+','+rx_byte_dec)

        # Plot the Data
        if pltData:
            y_varT = np.append(y_varT, float(temperature))
            y_varT = y_varT[1:plot_window + 1]
            lineT.set_ydata(y_varT)
            y_varH = np.append(y_varH, float(humidity))
            y_varH = y_varH[1:plot_window + 1]
            lineH.set_ydata(y_varH)

            ax1.relim()
            ax2.relim()
            ax1.autoscale_view()
            ax2.autoscale_view()
            fig.canvas.draw()
            fig.canvas.flush_events()
    except:
        print("Keyboard Interrupt")
        break

    time.sleep(2)
