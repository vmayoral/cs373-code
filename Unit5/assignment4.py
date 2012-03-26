# --------------
# User Instructions
# 
# Define a function cte in the robot class that will
# compute the crosstrack error for a robot on a
# racetrack with a shape as described in the video.
#
# You will need to base your error calculation on
# the robot's location on the track. Remember that 
# the robot will be traveling to the right on the
# upper straight segment and to the left on the lower
# straight segment.
#
# --------------
# Grading Notes
#
# We will be testing your cte function directly by
# calling it with different robot locations and making
# sure that it returns the correct crosstrack error.  

from math import *
import random


# ------------------------------------------------
# 
# this is the robot class
#

class robot:
    
    # --------
    # init: 
    #    creates robot and initializes location/orientation to 0, 0, 0
    #
    
    def __init__(self, length = 20.0):
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.steering_drift = 0.0
    
    # --------
    # set: 
    #	sets a robot coordinate
    #
    
    def set(self, new_x, new_y, new_orientation):
        
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation) % (2.0 * pi)
    
    
    # --------
    # set_noise: 
    #	sets the noise parameters
    #
    
    def set_noise(self, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)
    
    # --------
    # set_steering_drift: 
    #	sets the systematical steering drift parameter
    #
    
    def set_steering_drift(self, drift):
        self.steering_drift = drift
    
    # --------
    # move: 
    #    steering = front wheel steering angle, limited by max_steering_angle
    #    distance = total distance driven, most be non-negative
    
    def move(self, steering, distance, 
             tolerance = 0.001, max_steering_angle = pi / 4.0):
        
        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        if distance < 0.0:
            distance = 0.0
        
        
        # make a new copy
        res = robot()
        res.length         = self.length
        res.steering_noise = self.steering_noise
        res.distance_noise = self.distance_noise
        res.steering_drift = self.steering_drift
        
        # apply noise
        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)
        
        # apply steering drift
        steering2 += self.steering_drift
        
        # Execute motion
        turn = tan(steering2) * distance2 / res.length
        
        if abs(turn) < tolerance:
            
            # approximate by straight line motion
            
            res.x = self.x + (distance2 * cos(self.orientation))
            res.y = self.y + (distance2 * sin(self.orientation))
            res.orientation = (self.orientation + turn) % (2.0 * pi)
        
        else:
            
            # approximate bicycle model for motion
            
            radius = distance2 / turn
            cx = self.x - (sin(self.orientation) * radius)
            cy = self.y + (cos(self.orientation) * radius)
            res.orientation = (self.orientation + turn) % (2.0 * pi)
            res.x = cx + (sin(res.orientation) * radius)
            res.y = cy - (cos(res.orientation) * radius)
        
        return res
    
    
    
    
    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]'  % (self.x, self.y, self.orientation)
    
    
    ############## ONLY ADD / MODIFY CODE BELOW THIS LINE ####################
    
    def cte(self, radius):
        '''
            Define 4 paths:
            
            1st: x < radius
                                  
                     /
                    |
                     \

            2nd: x > radius, x < 3*radius, y = 50

                    ----------- (->)

            3rd: x > 3*radius

                    \
                     |
                    /

            4th: x > radius, x < 3*radius, y = 0

                    ------------ (<-)
        '''

        cte = 0.0
        # First think is to identify the robot position
        if self.x < radius and self.y < 2*radius:      # 1st path
            #print '1st path'
            if self.y < 0:
                xpos = radius      
            else:
                xpos = radius - sqrt(radius**2 - (self.y - radius)**2)      # position where the robot should be
            cte = xpos - self.x
            #path_left.append([self.x, self.y])
        elif self.x > 3*radius and self.y <= 2*radius:  # 3rd path
            #print '3rd path'
            if self.y < 0:
                xpos = 3*radius
            else:
                xpos = 3*radius + sqrt(radius**2 - (self.y - radius)**2)      # position where the robot should be
            cte = self.x - xpos
            #path_right.append([self.x, self.y])
        elif self.y < radius:    # 4th path
            #print '4th path'
            cte = -self.y
            #path_bottom.append([self.x, self.y])
        else:              # 2nd path
            #print '2nd path'
            cte = self.y - 2*radius
            #path_top.append([self.x, self.y])
        #print 'CTE=', cte
	gpath.append([self.x, self.y])
        return cte

############## ONLY ADD / MODIFY CODE ABOVE THIS LINE ####################




# ------------------------------------------------------------------------
#
# run - does a single control run.


def run(params, radius, printflag = False):
    myrobot = robot()
    myrobot.set(0.0, radius, pi/ 2.0)
    speed = 1.0 # motion distance is equal to speed (we assume time = 1)
    err = 0.0
    int_crosstrack_error = 0.0
    N = 200
    
    crosstrack_error = myrobot.cte(radius) # You need to define the cte function!
    
    for i in range(N*2):
        diff_crosstrack_error = - crosstrack_error
        crosstrack_error = myrobot.cte(radius)
        diff_crosstrack_error += crosstrack_error
        int_crosstrack_error += crosstrack_error
        steer = - params[0] * crosstrack_error \
            - params[1] * diff_crosstrack_error \
            - params[2] * int_crosstrack_error
        myrobot = myrobot.move(steer, speed)
        if i >= N:
            err += crosstrack_error ** 2
        if printflag:
            print myrobot
    return err / float(N)

# ----------------------------------------
# some globals
path_left = []
path_top = []
path_right = []
path_bottom = []
gpath = []
# ----------------------------------------

radius = 25.0
params = [10.0, 15.0, 0]
err = run(params, radius, True)
print '\nFinal paramaeters: ', params, '\n ->', err

# ----------------------------------------
import matplotlib.pyplot as plt
plt.figure()
plt.hold(True)

def plotpath(path, label="path") :
    plt.plot([p[0] for p in path], [p[1] for p in path],
             label=label)
'''
plotpath(path_left, "left")
plotpath(path_top, "top")
plotpath(path_right, "right")
plotpath(path_bottom, "bottom")
'''
plotpath(gpath, 'path')

plt.legend()
plt.show()
# ----------------------------------------
