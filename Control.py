import pigpio
import numpy as np
import pygame



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

    'Logitech Extreme 3D':
    _GameController((-3, 0, -1, 2), 0),
}




class Control(Controller): 
    
    def __init__(self,THRUSTER_1, THRUSTER_2, THRUSTER_3,THRUSTER_4) -> None:
        self.THRUSTER_1 = THRUSTER_1
        self.THRUSTER_2 = THRUSTER_2
        self.THRUSTER_3 = THRUSTER_3
        self.THRUSTER_4 = THRUSTER_4
        
        
        thruster_pins = [THRUSTER_1, THRUSTER_2, THRUSTER_3,  THRUSTER_4]
        thvalue = [1500,1500,1500,1500] 
        pi = pigpio.pi()
        for item in thruster_pins:
            pi.set_servo_pulsewidth(item,1500)
        
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
        elif value == 0:
            return 1500
        else:
            return int(1500 + (value * 300))     

    def sig(value):
        if value < -1 or value > 1:
            return None
        elif value == 0:
            return 1500
        else:
            return int((np.sign(value) * (27**(abs(value)) - 1) / (27**(1) - 1)) * 300 + 1500)  
          
        


def run():
    control = Control(9, 11, 16, 8)
   
    con = control.get_controller()
    pi = pigpio.pi()
    while(1):
        con.update()
        move = control.map_values(con.getPitch())
        turn = control.sig(con.getPitch())
        
        if move == 1500:
            print('static')

        elif move != 1500:
             pi.set_servo_pulsewidth(control.THRUSTER_1, move) 
             pi.set_servo_pulsewidth(control.THRUSTER_2, move) 
             print(move) 

        elif turn != 1500:
             pi.set_servo_pulsewidth(control.THRUSTER_3, turn)     
             pi.set_servo_pulsewidth(control.THRUSTER_4, turn)     

    
    
if __name__=='__main__' :
    run()