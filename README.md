# USB forwarding(USB IP)


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

