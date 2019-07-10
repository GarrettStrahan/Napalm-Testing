#Programmed with Python 3.7, with Windows 10. It might not work on Linux. I'll try to make a linux version later.
#version 0.5 is much faster

from napalm import get_network_driver
import os
import shutil
import re
from datetime import datetime
import mynapalmfunctions

ipaddr = input("What is the IP-Address?")
username = input("What is the username?")
password = input("What is the password?")

junos_driver = get_network_driver('junos')
junos_device = {'username': username, 'password': password, 'hostname': ipaddr}

log = ['show log']
commands = ['show version', 'show chassis hardware'] #These commands have the serial # + model #, just need to parse the data

with junos_driver(**junos_device) as junos:
  shrun = junos.get_config()
  interfaces = junos.get_interfaces()
  commands = junos.cli(commands)
  logs = junos.cli(log)

mynapalmfunctions.writetohdd(interfaces, shrun, logs, commands) #This is creating files with SSH data
serialnum = mynapalmfunctions.parsingdata() #This is getting serial #
serialnum = re.sub(r'[^\w]', ' ', serialnum)
serialnum = serialnum.strip()

foldercreation = r'D:\Testing' #change this variable and startfolder if you want to not have the outputted files in D:\Testing\
today = datetime.now
startfolder = r"D:\Testing\{}".format(today().strftime('%m-%d-%Y-')) + serialnum

if os.path.exists(foldercreation) == False: #this is checking to see if the sub folder exists
    os.mkdir(foldercreation)

elif os.path.exists(foldercreation) == True:
    if os.path.exists(startfolder) == False:
        os.mkdir(startfolder)


startfolder = startfolder + "\\"

newfilename = startfolder  + "Logs.txt"
shutil.move("Logs.txt", newfilename)
newfilename = startfolder + "Running-Config.txt"
shutil.move("Running-Config.txt", newfilename)
newfilename = startfolder + "Interfaces.txt"
shutil.move("Interfaces.txt", newfilename)
newfilename = startfolder  + "Commands.txt"
shutil.move("Commands.txt", newfilename)

print("Your files have been moved to D:\Testing")
