import pigpio
import numpy as np
import pygame
from PID import PID
import time
import threading
import queue
import socket
import json


class Controller(object):
    STICK_DEADBAND = .05

    def __init__(self, axis_map):
        self.joystick = None
        self.axis_map = axis_map

    def update(self):
        pygame.event.pump()

    def getThrottle(self):
        return self._getAxis(0)

    def getRoll(self):
        return self._getAxis(1)

    def getPitch(self):
        return self._getAxis(2)

    def getYaw(self):
        return self._getAxis(3)

    def _getAxis(self, k):
        j = self.axis_map[k]
        val = self.joystick.get_axis(abs(j))
        if abs(val) < Controller.STICK_DEADBAND:
            val = 0
        return (-1 if j < 0 else +1) * val


class _GameController(Controller):

    def __init__(self, axis_map, button_id):
        Controller.__init__(self, axis_map)
        self.button_id = button_id

    def _getAuxValue(self):
        return self.joystick.get_button(self.button_id)

    def getAux(self):
        return self._getAuxValue()


controllers = {
    '2In1 USB Joystick':
        _GameController((-1, 2, -3, 0), 5),

    'Logitech Logitech Extreme 3D':
        _GameController((-3, 0, -1, 2), 0),
}


class Control(Controller):

    def __init__(self, THRUSTER_1, THRUSTER_2, THRUSTER_3, THRUSTER_4) -> None:
        self.THRUSTER_1 = THRUSTER_1
        self.THRUSTER_2 = THRUSTER_2
        self.THRUSTER_3 = THRUSTER_3
        self.THRUSTER_4 = THRUSTER_4
        self.control_queue = queue.Queue()

        thruster_pins = [THRUSTER_1, THRUSTER_2, THRUSTER_3, THRUSTER_4]
        thvalue = [1500, 1500, 1500, 1500]
        pi = pigpio.pi()
        for item in thruster_pins:
            pi.set_servo_pulsewidth(item, 1500)

    def get_controller(self):

        # Initialize pygame for joystick support
        pygame.display.init()
        pygame.joystick.init()
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        # Find your controller
        controller_name = joystick.get_name()
        if controller_name not in controllers.keys():
            print('Unrecognized controller: %s' % controller_name)
            exit(1)
        controller = controllers[controller_name]
        controller.joystick = joystick

        return controller

    def map_values(self, value):
        if value < -1 or value > 1:
            return None
        return int(1500 + (value * 300))

    def map_values_depth(self, value):
        if value < -1 or value > 1:
            return None
        else:
            return int(1700 + (value * 200))

    def sig(self, value):
        if value < -1 or value > 1:
            return None
        elif value == 0:
            return 1500
        else:
            return int((np.sign(value) * (27 ** (abs(value)) - 1) / (27 ** (1) - 1)) * 300 + 1500)


def run(control):
    # t = 0
    # t_prev = 0

    # Dcontrol = PID()

    con = control.get_controller()
    Depth = con.getThrottle()
    pi = pigpio.pi()
    print("Starting Control Loop")
    time.sleep(2)
    while (1):
        con.update()
        # t = time.time()
        # dt = t-t_prev
        # pos = 0 #Get from Depth Sensor
        # sp  = 0 # Get fro Joystick Slider
        # Depth = Dcontrol.compute(pos, sp, dt)
        move = control.map_values(con.getPitch())
        turn = control.sig(con.getYaw())
        depth = control.map_values_depth(con.getThrottle())
        control.control_queue.put((move, turn, depth))

        if move & turn == 1500:

            pi.set_servo_pulsewidth(control.THRUSTER_1, 1500)
            pi.set_servo_pulsewidth(control.THRUSTER_2, 1500)
            pi.set_servo_pulsewidth(control.THRUSTER_3, depth)
            pi.set_servo_pulsewidth(control.THRUSTER_4, depth)

        elif move != 1500:
            pi.set_servo_pulsewidth(control.THRUSTER_1, move)
            pi.set_servo_pulsewidth(control.THRUSTER_2, move)
            pi.set_servo_pulsewidth(control.THRUSTER_3, depth)
            pi.set_servo_pulsewidth(control.THRUSTER_4, depth)

        elif turn != 1500:
            pi.set_servo_pulsewidth(control.THRUSTER_1, turn)
            pi.set_servo_pulsewidth(control.THRUSTER_2, 3000 - turn)
            pi.set_servo_pulsewidth(control.THRUSTER_3, depth)
            pi.set_servo_pulsewidth(control.THRUSTER_4, depth)

            # t_prev = t
        # time.sleep(0.01)


def GUI(control):
    print(GUI)
    time.sleep(2)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)

    server_ip = "169.254.88.156"
    server_port = 7777

    while True:
        # Get control values from the queue
        move, turn, depth = control.control_queue.get()

        data = json.dumps({"move": move, "turn": turn, "depth": depth})
        s.sendto(data.encode(), (server_ip, server_port))
        print("DATA SENT")


if __name__ == '__main__':
    control = Control(9, 11, 16, 8)

    control_thread = threading.Thread(target=run, args=(control,))
    gui_thread = threading.Thread(target=GUI, args=(control,))

    control_thread.start()
    gui_thread.start()

    control_thread.join()
    gui_thread.join()
