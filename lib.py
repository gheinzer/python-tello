"""
Library for controlling the Tello EDU.
"""

import socket
import sys
import time
import threading
import json
from console_progressbar import ProgressBar

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
    def __init__(self, port=8889, address="192.168.10.1"):
        host = '0.0.0.0'
        port = 8890
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
            states = self.state_decoder(data)
            self.battery = int(states[14][1])
            print("BATTERY STATE: " + str(self.battery) + "%")
        except:
            pass
    def cmd(self, cmd, print=0):
        # Send data
        cmd_old = cmd
        cmd = cmd.encode(encoding="utf-8") 
        sent = self.sock.sendto(cmd, self.tello_address)
        if(print == 1):
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
                states = self.state_decoder(data)
                print(str(data))
                if(int(states[0][1]) > -1):
                    print("MissionPad discovered. MissionPad-ID: " + data)
            except:
                pass
            x = x + 1
    def mid(self):
        self.tello_address2 = ("192.168.10.1", 8890)
        ok = ""
        data, server = self.sock.recvfrom(1518)
        try:
            states = self.state_decoder(data)
            if(int(states[0][1]) > -1):
                return int(states[0][1])
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
    def MP_registrator(self, battery=1):
        
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
        x = 0
        logged_battery_30 = 0
        logged_battery_20 = 0
        while 1:
            data, server = self.sock.recvfrom(1518)
            try:
                states = self.state_decoder(data)
                if(int(states[0][1]) > -1):
                    mid = states[0][1]
                    x = states[1][1]
                    y = states[2][1]
                    z = states[3][1]
                    if(not(str(mid) in self.missionpads)):
                        print("MissionPad " + str(mid) + " registrated at:\nx: " + x + "\ny: " + y + "\nz: " + z)
                    self.missionpads[str(mid)] = {
                        "x-position":x,
                        "y-position":y,
                        "z-position":z
                        }
                self.battery = int(states[14][1])
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
    def goToMP(self, mid, speed):
        mx = self.missionpads[str(mid)]["x-position"]
        my = self.missionpads[str(mid)]["y-position"]
        mz = self.missionpads[str(mid)]["z-position"]
        mid = "m" + str(mid)
        drone.cmd("go " + mx + " "  + my + " " + mz + " " + speed + " " + mid)
    def MPR(self):
        MissionPadThread = threading.Thread(target=self.MP_registrator)
        MissionPadThread.start()
