#!/usr/bin/python3

import os
import nmap
from datetime import datetime

def CheckMAC(mac):
    CurrentPath = os.path.dirname(os.path.abspath(__file__))
    with open(CurrentPath + "/MACs.txt") as f:
        datafile = f.readlines()
    f.close();
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
	CheckMAC(mac)

