"""
Library for controlling the Tello EDU.
"""
import socket
import sys
import time
import threading

class tello():
    missionpads = {}
    battery = -1
    def recv(self):
        count = 0
        while True: 
            try:
                data, server = self.sock.recvfrom(1518)
                print(data.decode(encoding="utf-8"))
            except Exception:
                print ('\nExit . . .\n')
                break
    def __init__(self, port=8890, address="192.168.10.1"):
        host = '0.0.0.0'
        port = port
        locaddr = (host,port) 


        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.tello_address = (address, 8889)

        self.sock.bind(locaddr)

        self.cmd("command")

        print("Tello is ready for Commands")

        #recvThread = threading.Thread(target=self.recv)
        #recvThread.start()
        #MissionPadThread = threading.Thread(target=self.state)
        #MissionPadThread.start()

        #self.sock.recvfrom(1518)
        data, server = self.sock.recvfrom(1518)
        data, server = self.sock.recvfrom(1518)
        try:
            infos = self.state_decoder(data)
            self.battery = int(infos[14][1])
            #print("BATTERY STATE: " + str(self.battery) + "%")
        except:
            pass
    def cmd(self, cmd, printcmd=0):
        # Send data
        cmd_old = cmd
        cmd = cmd.encode(encoding="utf-8") 
        sent = self.sock.sendto(bytes(cmd), self.tello_address)
        if(printcmd == 1):
            print(str(cmd))
    def read_battery_level(self):
        self.cmd("battery?")
        data, server = self.sock.recvfrom(1518)
        battery_level = data.decode(encoding="utf-8")
        time.sleep(0.4)
        self.cmd("battery?")
        data, server = self.sock.recvfrom(1518)
        battery_level = data.decode(encoding="utf-8")
        return battery_level
    def state(self):
        self.tello_address2 = ("192.168.10.1", 8890)
        x = 0
        while 1:
            ok = ""
            data, server = self.sock.recvfrom(1518)
            try:
                infos = self.state_decoder(data)
                print(str(data))
                if(int(infos[0][1]) > -1):
                    print("MissionPad discovered. MissionPad-ID: " + data)
            except:
                pass
            x = x + 1
    def mid(self):
        self.tello_address2 = ("192.168.10.1", 8890)
        ok = ""
        data, server = self.sock.recvfrom(1518)
        try:
            infos = self.state_decoder(data)
            if(int(infos[0][1]) > -1):
                return int(infos[0][1])
            else:
                return -1
        except:
            pass
    def state_decoder(self, state):
        state = str(state)
        state = state.split(";")
        y = 0
        for x in state:
            state[int(y)] = x.split(":")
            y += 1
        return state
    def _MP_registrator(self):
        self.cmd("mon")
        time.sleep(1)
        self.cmd("mdirection 2")
        print("MissionPad registration is enabled")
        """
        MissionPad-Dictionary (missionpads) Format:
        {
        "1":
            {
                "x-position": 0
                "y-position": 0
                "z-position": 0
            }
        "2":
            {
                "x-position": 5
                "y-position": -3
                "z-position": 12
            }
        }
        """
        """
        MissionPad Information Table (Only important data)
        
        Array ID   | Data
        -----------+----------------------------------------
        0          | MissionPad ID
        -----------+----------------------------------------
        1          | x Position of the MissionPad
        -----------+----------------------------------------
        2          | y Position of the MissionPad
        -----------+----------------------------------------
        3          | z Position of the MissionPad
        -----------+----------------------------------------
        14         | Battery Level (%)

        Each of the items is an array, the first item returns the key, the second the value.
        """
        self.tello_address2 = ("192.168.10.1", 8890)
        logged_battery_30 = 0
        logged_battery_20 = 0
        while 1:
            data, server = self.sock.recvfrom(1518)
            try:
                infos = self.state_decoder(data)
                if(int(infos[0][1]) > -1):
                    mid = infos[0][1]
                    x = infos[1][1]
                    y = infos[2][1]
                    z = infos[3][1]
                    if(not(str(mid) in self.missionpads)):
                        print("MissionPad " + str(mid) + " registrated at:\nx: " + x + "\ny: " + y + "\nz: " + z)
                    self.missionpads[str(mid)] = {
                        "x-position":x,
                        "y-position":y,
                        "z-position":z
                        }
            except:
                pass
    def _BatteryChecker(self):
        logged_battery_30 = 0
        logged_battery_20 = 0
        while 1:
            data, server = self.sock.recvfrom(1518)
            try:
                infos = self.state_decoder(data)
                if(int(infos[0][1]) > -1):
                    mid = infos[0][1]
                    x = infos[1][1]
                    y = infos[2][1]
                    z = infos[3][1]
                    if(not str(mid) in self.missionpads):
                        print("MissionPad " + str(mid) + " registrated at:\nx: " + x + "\ny: " + y + "\nz: " + z)
                    self.missionpads[str(mid)] = {
                        "x-position":x,
                        "y-position":y,
                        "z-position":z
                        }
                self.battery = int(infos[14][1])
                if(int(self.battery) < 30 and logged_battery_30 == 0):
                    print("WARNING: The Battery level of your Tello EDU is under 30 %. If it sinks under 20 %, the drone will land automatically")
                    logged_battery_30 = 1
                if(int(self.battery) < 20 and logged_battery_30 == 0):
                    print("WARNING: The Battery level of your Tello EDU is under 20 %. The drone stops and lands automatically.")
                    self.cmd("stop")
                    time.sleep(1)
                    self.cmd("land")
                    logged_battery_20 = 1
            except:
                pass
    def takeoff(self):
        self.cmd("takeoff")
    def land(self):
        self.cmd("land")
    def goToMP(self, mid, speed=100):
        if(str(mid) in self.missionpads):
            mx = self.missionpads[str(mid)]["x-position"]
            my = self.missionpads[str(mid)]["y-position"]
            mz = self.missionpads[str(mid)]["z-position"]
            mid = "m" + str(mid)
            self.cmd("go " + str(mx) + " "  + str(my) + " " + str(mz) + " " + str(speed) + " " + str(mid))
        else:
            raise Exception("MissionPad " + str(mid) + " is not registered.")
    def MPR(self):
        MPRThread = threading.Thread(target=self._MP_registrator)
        MPRThread.start()
    def startBatteryChecker(self):
        BatterryCheckerThread = threading.Thread(target=self._BatteryChecker)
        BatterryCheckerThread.start()
    def setSpeed(self, speed):
        if(speed < 101 and speed > 9):
            self.cmd("speed " + str(speed))
        else:
            raise ValueError("Not in range")
    def up(self, distance):
        if(distance < 501 and distance > 19):
            self.cmd("up " + str(distance))
        else:
            raise ValueError("Not in range")
    def down(self, distance):
        if(distance < 501 and distance > 19):
            self.cmd("down  " + str(distance))
        else:
            raise ValueError("Not in range")
    def left(self, distance):
        if(distance < 501 and distance > 19):
            self.cmd("left " + str(distance))
        else:
            raise ValueError("Not in range")
    def right(self, distance):
        if(distance < 501 and distance > 19):
            self.cmd("right " + str(distance))
        else:
            raise ValueError("Not in range")
    def forward(self, distance):
        if(distance < 501 and distance > 19):
            self.cmd("forward " + str(distance))
        else:
            raise ValueError("Not in range")
    def backward(self, distance):
        if(distance < 501 and distance > 19):
            self.cmd("back  " + str(distance))
        else:
            raise ValueError("Not in range")
    def flip(self, direction):
        if(direction == "r" or direction == "l" or direction == "f" or direction == "b"):
            self.cmd("flip " + str(direction))
        else:
            raise ValueError("Please type 'f' (forward), 'b' (backward), 'r' (right) or 'l' (left) as flip direction.")
    def rotate(self, direction, degrees):
        if(direction == "cw" or direction == "ccw"):
            if(degrees < 361 and degrees > 0):
                self.cmd(str(direction) + " " + str(degrees))
            else:
                raise ValueError("Degrees are not in range")
        else:
            raise Exception("Please type 'cw' (Clockwise) or 'ccw' (Counterclockwise) as rotate direction.")
