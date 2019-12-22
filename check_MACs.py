#!/usr/bin/python3

import os
import nmap
from datetime import datetime
import argparse
import easygui

parser = argparse.ArgumentParser(description='To check MACs connected on our local net and compare them against a list of allowed MACs')
parser.add_argument("--macs", required=True, type=str, help="File with list of allowed MACs")
args = parser.parse_args()

macs_file = '/' + args.macs

def CheckMAC(mac):
    CurrentPath = os.path.dirname(os.path.abspath(__file__))
    with open(CurrentPath + macs_file) as f:
        datafile = f.readlines()
    f.close();
    print(datafile)
    found = False  
    for line in datafile:
        if mac in line:
            found = True 
    if found:
        print("MAC ", mac, " is in allowed list")
        log = open(CurrentPath + "/macs_log.txt", "a+")
        log.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ", MAC "+ mac + " is in allowed list \n")
        log.close()
    else:
        print("MAC ", mac, " is NOT in allowed list")
        easygui.msgbox("Found a MAC address no present in the alowed list!", title="WARNING!")
        log = open(CurrentPath + "/macs_log.txt", "a+")
        log.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ", MAC "+ mac + " is NOT in allowed list \n")
        log.close()
        
def FindConnectedMACs():
	nm = nmap.PortScanner()
	nm.scan(hosts = '192.168.1.0/24', arguments = '-sn')
	ConnectedMACsList = []
	for host in nm.all_hosts():
		if nm[host]['status']['state'] != "down":
			try:
				ConnectedMACsList.append(nm[host]['addresses']['mac'])
			except:
					mac = 'unknown'
		else:
			print ("Nothin here")
	return ConnectedMACsList

ConnectedMACs = FindConnectedMACs()
for mac in ConnectedMACs:
	print("Going to check a MAC")
	CheckMAC(mac)

