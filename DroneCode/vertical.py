#import modules
import tellopy
import time

#create three Tello objects
drone1 = tellopy.Tello()
drone2 = tellopy.Tello()
drone3 = tellopy.Tello()

#connect to each drone
drone1.connect()
drone2.connect()
drone3.connect()

drone1.takeoff()
drone2.takeoff()
drone3.takeoff()

#move each drone to its position in the vertical line 
drone1.go(0, 0, 25, 50)
drone2.go(0, 0, 50, 50)
drone3.go(0, 0, 75, 50)

#wait for drones to reach their position 
time.sleep(5)

#land each drone
drone1.land()
drone2.land()
drone3.land()

