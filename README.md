# Remotely Operated Underwater Vehicle
This is the major project of students of ZHCET, AMU under the aegis of MTS AUV ZHCET Club. This repository is an effort to design the first generation of software for Remotely Operated Underwater Vehicle. The software system can be broken down into two major parts; 1). The Vehicle Side and 2). The Base Station Side.

1. **The Vehicle Side:**

   The vehicle side of the program is simple, it does two tasks: generate controls for the thrusters and send feedback data ( camera-feed and generated control values) to be displayed back to BS. It contains the following:
   
   |  
   |  
    ------> Control.py  
   |  
    ------> cam_vehicle.py
   * Control.py : This file employs Multithreading in a producer-consumer fashion; here the *GUI* function is the consumer thread and *run*
                  function as the producer thread. The run function generates the control and pushes their values on the queue. The thread-                    safe queue is then accessed by the GUI function which encodes and transmit the data back to BS using UDP protocol.

   
    
     





## USB forwarding(USB IP)


### On the server side(linux):

1. ```sudo apt-get install linux-tools-generic```

2. ```sudo modprobe usbip_host```

3. ```sudo nano /etc/modules```

4. add ```usbip_host``` to the end of texts

5. ```lsusb``` to see a list of attached USB devices

6. ```sudo usbip list -p -l```

7. ```sudo usbip bind --busid="Bus ID"``` enter busid from the above list command

8. ```sudo usbipd```

### On the client side(rpi):
0. On RaspberryPi before using Pip first do 
     ```sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED```
1. ```wget http://raspbian.mirror.net.in/raspbian/raspbian/pool/main/l/linux/usbip_2.0+5.10.158-2+rpi1_armhf.deb```

2. ```make the folder executable using chmod +x Folder Name```

2. ```sudo apt install ./usbip_2.0+5.10.158-2+rpi1_armhf.deb```

3. ```sudo modprobe vhci-hcd```

4. ```sudo nano /etc/modules```

5. add ```vhci-hcd``` to the end of texts

6. ```sudo usbip attach -r "IP Address" -b "Bus ID"```

