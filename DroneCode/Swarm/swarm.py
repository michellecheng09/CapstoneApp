from asyncio import timeout
import sys
import time
from tello import *
import queue
import traceback
import time
import os
import binascii
from contextlib import suppress



class SwarmUtil(object):
    """
    Swarm utility class.
    """

    @staticmethod
    def create_execution_pools(num):
        """
        Creates execution pools.

        :param num: Number of execution pools to create.
        :return: List of Queues.
        """
        return [queue.Queue() for x in range(num)]


    @staticmethod
    def drone_handler(tello, queue):
        """
        Drone handler.

        :param tello: Tello.
        :param queue: Queue.
        :return: None.
        """
        while True:
            while queue.empty():
                pass
            command = queue.get()
            tello.send_command(command)


    @staticmethod
    def all_queue_empty(pools):
        """
        Checks if all queues are empty.

        :param pools: List of Queues.
        :return: Boolean indicating if all queues are empty.
        """
        for queue in pools:
            if not queue.empty():
                return False
        return True


    @staticmethod
    def all_got_response(manager):
        """
        Checks if all responses are received.

        :param manager: TelloManager.
        :return: A boolean indicating if all responses are received.
        """
        for log in manager.get_last_logs():
            if not log.got_response():
                return False
        return True


    @staticmethod
    def create_dir(dpath):
        """
        Creates a directory if it does not exists.

        :param dpath: Directory path.
        :return: None.
        """
        if not os.path.exists(dpath):
            with suppress(Exception):
                os.makedirs(dpath)

    @staticmethod
    def save_log(manager):
        """
        Saves the logs into a file in the ./log directory.

        :param manager: TelloManager.
        :return: None.
        """
        dpath = './log'
        SwarmUtil.create_dir(dpath)

        start_time = str(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time())))
        fpath = f'{dpath}/{start_time}.txt'

        with open(fpath, 'w') as out:
            log = manager.get_log()
            for cnt, stats in enumerate(log.values()):
                out.write(f'------\nDrone: {cnt + 1}\n')

                s = [stat.get_stats_delimited() for stat in stats]
                s = '\n'.join(s)

                out.write(f'{s}\n')
        
        print(f'[LOG] Saved log files to {fpath}')


    @staticmethod
    def check_timeout(start_time, end_time, timeout):
        """
        Checks if the duration between the end and start times
        is larger than the specified timeout.

        :param start_time: Start time.
        :param end_time: End time.
        :param timeout: Timeout threshold.
        :return: A boolean indicating if the duration is larger than the specified timeout threshold.
        """
        diff = end_time - start_time
        time.sleep(0.1)
        return diff > timeout

class Swarm(object):
    """
    Tello Edu swarm.
    """

    def __init__(self, fpath):
        """
        Ctor.

        :param fpath: Path to command text file.
        """
        self.ENU=1
        self.home_x=0
        self.home_y=0
        self.home_z=0
        
        self.fpath = fpath
        self.commands = self._get_commands(fpath)
        self.manager = TelloManager()
        self.tellos = []
        self.pools = []
        self.sn2ip = {
            '0TQZK7NED02VMT': '192.168.0.100',
            '0TQZK7JED02TVJ': '192.168.0.101',
            '0TQZK5DED02KHL': '192.168.0.102',
        }
        self.id2sn = {
            0: '0TQZK7NED02VMT',
            1: '0TQZK7JED02TVJ',
            2: '0TQZK5DED02KHL',
        }
        self.ip2id = {
            '192.168.0.100': 0,
            '192.168.0.101': 1,
            '192.168.0.102': 2,
        }

    def start(self):
        """
        Main loop. Starts the swarm.

        :return: None.
        """
        def is_invalid_command(command):
            if command is None:
                return True
            c = command.strip()
            if len(c) == 0:
                return True
            if c == '':
                return True
            if c == '\n':
                return True
            return False
        
        try:
            for command in self.commands:
                if is_invalid_command(command):
                    continue

                command = command.rstrip()

                if '//' in command:
                    self._handle_comments(command)
                elif 'scan' in command:
                    self._handle_scan(command)
                elif '>' in command:
                    self._handle_gte(command)
                elif 'battery_check' in command:
                    self._handle_battery_check(command)
                elif 'delay' in command:
                    self._handle_delay(command)
                elif 'correct_ip' in command:
                    self._handle_correct_ip(command)
                elif '=' in command:
                    self._handle_eq(command)
                elif 'sync' in command:
                    self._handle_sync(command)
                elif 'read_pad' in command:
                    self._handle_read_pad(command)
                elif 'poly' in command:
                    self._handle_poly(command)
                elif 'vertical' in command:
                    self._handle_vertical(command)
                elif 'triangle' in command:
                    self._handle_triangle(command)
                elif 'wave' in command:
                    self._handle_wave(command)
                elif 'circle' in command:
                    self._handle_circle(command)

            self._wait_for_all()
        except KeyboardInterrupt as ki:
            self._handle_keyboard_interrupt()
        except Exception as e:
            self._handle_exception(e)
            traceback.print_exc()
        finally:
            SwarmUtil.save_log(self.manager)

    def _handle_read_pad(self):
        self.start()
        self.takeoff()
        mission_pad_number=self.get_mission_pad()
        print(str(mission_pad_number))
        self.land()
        
    def _wait_for_all(self):
        """
        Waits for all queues to be empty and for all responses
        to be received.

        :return: None.
        """
        while not SwarmUtil.all_queue_empty(self.pools):
            time.sleep(0.5)
        
        time.sleep(1)

        while not SwarmUtil.all_got_response(self.manager):
            time.sleep(0.5)

    def _get_commands(self, fpath):
        """
        Gets the commands.

        :param fpath: Command file path.
        :return: List of commands.
        """
        with open(fpath, 'r') as f:
            return f.readlines()

    def _handle_comments(self, command):
        """
        Handles comments.

        :param command: Command.
        :return: None.
        """
        print(f'[COMMENT] {command}')

    def _handle_scan(self, command):
        """
        Handles scan.

        :param command: Command.
        :return: None.
        """
        n_tellos = int(command.partition('scan')[2])

        self.manager.find_avaliable_tello(n_tellos)
        self.tellos = self.manager.get_tello_list()
        self.pools = SwarmUtil.create_execution_pools(n_tellos)

        for x, (tello, pool) in enumerate(zip(self.tellos, self.pools)):
            self.ip2id[tello.tello_ip] = x

            t = Thread(target=SwarmUtil.drone_handler, args=(tello, pool))
            t.daemon = True
            t.start()

            print(f'[SCAN] IP = {tello.tello_ip}, ID = {x}')

    def _handle_gte(self, command):
        """
        Handles gte or >.

        :param command: Command.
        :return: None.
        """
        id_list = []
        id = command.partition('>')[0]

        if id == '*':
            id_list = [t for t in range(len(self.tellos))]
        else:
            id_list.append(int(id)-1) 
        
        action = str(command.partition('>')[2])

        for tello_id in id_list:
            sn = self.id2sn[tello_id]
            ip = self.sn2ip[sn]
            id = self.ip2id[ip]

            self.pools[id].put(action)
            print(f'[ACTION] SN = {sn}, IP = {ip}, ID = {id}, ACTION = {action}')

    def _handle_battery_check(self, command):
        """
        Handles battery check. Raises exception if any drone has
        battery life lower than specified threshold in the command.

        :param command: Command.
        :return: None.
        """
        threshold = int(command.partition('battery_check')[2])
        for queue in self.pools:
            queue.put('battery?')

        self._wait_for_all()

        is_low = False

        for log in self.manager.get_last_logs():
            battery = int(log.response)
            drone_ip = log.drone_ip

            print(f'[BATTERY] IP = {drone_ip}, LIFE = {battery}%')

            if battery < threshold:
                is_low = True
        
        if is_low:
            raise Exception('Battery check failed!')
        else:
            print('[BATTERY] Passed battery check')

    def _handle_delay(self, command):
        """
        Handles delay.

        :param command: Command.
        :return: None.
        """
        delay_time = float(command.partition('delay')[2])
        print (f'[DELAY] Start Delay for {delay_time} second')
        time.sleep(delay_time)  

    def _handle_correct_ip(self, command):
        """
        Handles correction of IPs.

        :param command: Command.
        :return: None.
        """
        for queue in self.pools:
            queue.put('sn?') 

        self._wait_for_all()
        
        for log in self.manager.get_last_logs():
            sn = str(log.response)
            tello_ip = str(log.drone_ip)
            self.sn2ip[sn] = tello_ip

            print(f'[CORRECT_IP] SN = {sn}, IP = {tello_ip}')

    def _handle_eq(self, command):
        """
        Handles assignments of IDs to serial numbers.

        :param command: Command.
        :return: None.
        """
        id = int(command.partition('=')[0])
        sn = command.partition('=')[2]
        ip = self.sn2ip[sn]

        self.id2sn[id-1] = sn
        
        print(f'[IP_SN_ID] IP = {ip}, SN = {sn}, ID = {id}')

    def _handle_sync(self, command):

        
        """
        Handles synchronization.

        :param command: Command.
        :return: None.
        """
        timeout = float(command.partition('sync')[2])
        print(f'[SYNC] Sync for {timeout} seconds')

        time.sleep(1)

        try:
            start = time.time()
            
            while not SwarmUtil.all_queue_empty(self.pools):
                now = time.time()
                if SwarmUtil.check_timeout(start, now, timeout):
                    raise RuntimeError('Sync failed since all queues were not empty!')

            print('[SYNC] All queues empty and all commands sent')
           
            while not SwarmUtil.all_got_response(self.manager):
                now = time.time()
                if SwarmUtil.check_timeout(start, now, timeout):
                    raise RuntimeError('Sync failed since all responses were not received!')
            
            print('[SYNC] All response received')
        except RuntimeError:
            print('[SYNC] Failed to sync; timeout exceeded')
        return self.barrier.wait(timeout)

    def _handle_keyboard_interrupt(self):
        """
        Handles keyboard interrupt.

        :param command: Command.
        :return: None.
        """
        print('[QUIT_ALL], KeyboardInterrupt. Sending land to all drones')
        tello_ips = self.manager.tello_ip_list
        for ip in tello_ips:
            self.manager.send_command('land', ip)

    def _handle_exception(self, e):
        """
        Handles exception (not really; just logging to console).

        :param command: Command.
        :return: None.
        """
        print(f'[EXCEPTION], {e}')

    def _handle_vertical(self,command):
        """
        Handles vertical Formation
        Assumes start with horizontal line up
        """

        #Make horizontal line to vertical on x axis 
        coordinates={}
        
        coordinates.update([('x1',self.home_x-30),('y1',self.home_y+30),('z1',self.home_z),
                            ('x2',self.home_x),('y2',self.home_y),('z2',self.home_z),
                            ('x3',self.home_x+30),('y3',self.home_y-30),('z3',self.home_z)])

        self.loop(coordinates)

        #Add diagonal

        coordinates.clear()
        
        coordinates.update([('x1',self.home_x),('y1',self.home_y),('z1',self.home_z+30),
                            ('x2',self.home_x),('y2',self.home_y),('z2',self.home_z),
                            ('x3',self.home_x),('y3',self.home_y),('z3',self.home_z-30)])

        self.loop(coordinates)

        #move left right 
        coordinates.clear()
        
        coordinates.update([('x1',self.home_x),('y1',self.home_y-30),('z1',self.home_z),
                            ('x2',self.home_x),('y2',self.home_y),('z2',self.home_z),
                            ('x3',self.home_x),('y3',self.home_y)+30,('z3',self.home_z)])
        
        self.loop(coordinates)

        #Return to orginal position (horizontal formation)

        coordinates.clear()
        
        coordinates.update([('x1',self.home_x+30),('y1',self.home_x),('z1',self.home_z-30),
                            ('x2',self.home_x),('y2',self.home_y),('z2',self.home_z+0),
                            ('x3',self.home_x-30),('y3',self.home_y),('z3',self.home_z+30)])

        self.loop(coordinates)
        
    def _handle_wave(self,command):
        """
        Handles Wave Formation 
        Assume Horizontal Start 
        """

        #Make first wave 
        coordinates={}
        
        coordinates.update([('x1',self.home_x),('y1',self.home_y),('z1',self.home_z+30),
                            ('x2',self.home_x),('y2',self.home_y),('z2',self.home_z-30),
                            ('x3',self.home_x),('y3',self.home_y),('z3',self.home_z+30)])

        self.loop(coordinates)

        #Make Second wave 

        coordinates.clear()
        
        coordinates.update([('x1',self.home_x),('y1',self.home_y),('z1',self.home_z-60),
                            ('x2',self.home_x),('y2',self.home_y),('z2',self.home_z+60),
                            ('x3',self.home_x),('y3',self.home_y),('z3',self.home_z-60)])

        self.loop(coordinates)

        #Return to Original  
        coordinates.clear()
        
        coordinates.update([('x1',self.home_x),('y1',self.home_y),('z1',self.home_z+30),
                            ('x2',self.home_x),('y2',self.home_y),('z2',self.home_z-30),
                            ('x3',self.home_x),('y3',self.home_y),('z3',self.home_z+30)])
        self.loop(coordinates)

    def _handle_triangle(self,command):
        """
        Handles Triangle Formation
        Assume horizontal starting position
        """
          #Make triangle

        coordinates={}
        
        coordinates.update([('x1',self.home_x),('y1',self.home_y),('z1',self.home_z),
                            ('x2',self.home_x),('y2',self.home_y),('z2',self.home_z+70),
                            ('x3',self.home_x),('y3',self.home_y),('z3',self.home_z)])
        self.loop(coordinates)

        #Return to Original  
        coordinates.clear()
        
        coordinates.update([('x1',self.home_x),('y1',self.home_y),('z1',self.home_z),
                            ('x2',self.home_x),('y2',self.home_y),('z2',self.home_z-70),
                            ('x3',self.home_x),('y3',self.home_y),('z3',self.home_z)])
        self.loop(coordinates)

    def _handle_circle(self,command): 
        """
        Handles Circle Formation
        Assuming horizontal starting point and always returns to starting point 
        """
        coordinates={}

        coordinates.update([('x1',self.home_x),('y1',self.home_y-30),('z1',self.home_z+30),
                            ('x2',self.home_x),('y2',self.home_y),('z2',self.home_z),
                            ('x3',self.home_x),('y3',self.home_y+30),('z3',self.home_z+30)])
        
        self.circleloop(coordinates)


    def _handle_poly(self,command):
        """
        Handles Poly Formation 

        """
       # Swarm = TelloSwarm()
      #  Swarm.connect()

      #  for drone in Swarm.drones:
            #drone.takeoff()

        sides = int(command.partition('poly')[2])
        print(s)

        tello_ips = self.manager.tello_ip_list
        for ip in tello_ips:
            for s in range(sides):
                command= "forward 25" #to update 
                self.manager.send_command(command,ip)
                command2= ip+(f">ccw {(round(360/sides))}")
                self.manager.send_command(command2,ip)
            pass
        
    def loop(self,coordinates):
        id_list=[]
        id_list=[t for t in range(len(self.tellos))]
        num=0
        
        for tello_id in id_list:
            sn = self.id2sn[tello_id]
            ip = self.sn2ip[sn]
            if num==0:
                print(f'{str(num)}{str(ip)}')
                print(f'{coordinates["x1"]},{coordinates["y1"]},{coordinates["z1"]}')
                if(self.ENU==1):
                    self.moveNED(coordinates["x1"],coordinates["y1"],coordinates["z1"],ip)
                else:
                    self.moveENU(coordinates["x1"],coordinates["y1"],coordinates["z1"],ip)
            elif num==1:
                print(f'{str(num)}{str(ip)}')
                print(f'{coordinates["x2"]},{coordinates["y2"]},{coordinates["z2"]}')
                if(self.ENU==1):
                    self.moveNED(coordinates["x2"],coordinates["y2"],coordinates["z2"],ip)
                else:
                    self.moveENU(coordinates["x2"],coordinates["y2"],coordinates["z2"],ip)
            elif num==2:
                print(f'{str(num)}{str(ip)}')
                print(f'{coordinates["x3"]},{coordinates["y3"]},{coordinates["z3"]}')
                if(self.ENU==1):
                    self.moveNED(coordinates["x3"],coordinates["y3"],coordinates["z3"],ip)
                else:
                    self.moveENU(coordinates["x3"],coordinates["y3"],coordinates["z3"],ip)
            num=num+1
    
    def circleloop(self,coordinates):
        id_list=[]
        id_list=[t for t in range(len(self.tellos))]
        num=0
        
        for tello_id in id_list:
            sn = self.id2sn[tello_id]
            ip = self.sn2ip[sn]
            if num==0:
                print(f'{str(num)}{str(ip)}')
                print(f'{coordinates["x1"]},{coordinates["y1"]},{coordinates["z1"]}')
                self.makeCircle(coordinates["x1"],coordinates["y1"],coordinates["z1"],ip)

            elif num==1:
                print(f'{str(num)}{str(ip)}')
                print(f'{coordinates["x2"]},{coordinates["y2"]},{coordinates["z2"]}')
                self.makeCircle(coordinates["x2"],coordinates["y2"],coordinates["z2"],ip)
                
            elif num==2:
                print(f'{str(num)}{str(ip)}')
                print(f'{coordinates["x3"]},{coordinates["y3"]},{coordinates["z3"]}')
                self.makeCircle(coordinates["x3"],coordinates["y3"],coordinates["z3"],ip)
            num=num+1


    def makeCircle(self,x,y,z,ip):
        x2=x*-1
        y2=y*-1
        z2=z*-1

        self.manager.send_command("curve "+ str(x) + " " +str(y) + " " +str(z)
                                  +" "+ str(x2)+ " " +str(y2) + " "+str(z2),ip)

    def moveENU(self,x,y,z,ip):
        x2=x*-1
        y2=y*-1
        z2=z*-1

        if y>0:
            self.manager.send_command("forward "+str(y),ip)             
        elif y<0:
            self.manager.send_command("back "+str(y2),ip)

        if x>0:
            self.manager.send_command("right "+str(x),ip)
        elif x<0:
            self.manager.send_command("left "+str(x2),ip)

        if z>0:
            self.manager.send_command("up "+str(z),ip)
        elif z<0:
            self.manager.send_command("down "+str(z2),ip)

    def moveNED(self,x,y,z,ip):
        y2=y*-1
        x2=x*-1
        z2=z*-1

        if x>0:
            self.manager.send_command("forward "+str(x),ip)
        elif x<0:
            self.manager.send_command("back "+str(x2),ip)

        if y>0:
            self.manager.send_command("right "+str(y),ip)
        elif y<0:
            self.manager.send_command("left "+str(y2),ip)
    
        if z>0:
            self.manager.send_command("up "+str(z),ip)
        elif z<0:                                                                                                              
             self.manager.send_command("down "+str(z2),ip)
        

    