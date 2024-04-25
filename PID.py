class PID():
    def __init__(self, KP, KI, KD, target=0):
        self.kp = KP
        self.ki = KI
        self.kd = KD
        self.sp = target
        self.error_last = 0
        self.integral_error = 0
        self.saturation_max = None
        self.saturation_min = None

    def compute(self, pos, sp, dt):
        # compute the error
        error = sp - pos
        # find the derivative of the error (how the error changes with time)
        derivative_error = (error - self.error_last) / dt
        # error build up over time
        self.integral_error += error * dt
        output = self.kp * error + self.ki * self.integral_error + self.kd * derivative_error
        self.error_last = error
        if output > self.saturation_max and self.saturation_max is not None:
            output = self.saturation_max
        elif output < self.saturation_min and self.saturation_min is not None:
            output = self.saturation_min
        return output

    """
    consider renaming the variables min and max as they are inbuilt functions in python
    """
    def setLims(self, min, max):
        self.saturation_max = max
        self.saturation_min = min
