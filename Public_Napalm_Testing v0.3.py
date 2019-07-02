from napalm import get_network_driver
import json
import os
import shutil
import re
from datetime import datetime


def parsingdata(): #Data is parsed for serial#
    file_object = open("Commands.txt", 'r')
    data = file_object.readlines()

    # print(data)
    print("Converting")
    data = json.dumps(data)
    new_data = re.findall(r"\b[A-Z0-9]{12}\b", data) #this looks for 12 digits or capital letters
    print(new_data)
    return str(new_data)

def writetohdd(interfaces, shrun, logs, commands):
    File_object = open("Interfaces.txt", "w")
    interfaces = json.dumps(interfaces)
    interfaces = interfaces.replace(",", "\n")
    interfaces = interfaces.replace("}", "} \n")
    File_object.write(interfaces)
    print("The interfaces has been been written to Interfaces.txt")


    File_object2 = open("Running-Config.txt", "w")
    shrun = json.dumps(shrun)
    shrun = shrun.replace('\\n', '\n')
    File_object2.write(shrun)
    print("The Running-configuration has been been written to Running-Config.txt")

    File_object3 = open("Logs.txt", "w")
    logs = json.dumps(logs)
    File_object3.write(logs)
    print("The Logs have been written to Logs.txt")

    File_object4 = open("Commands.txt", "w")
    commands = json.dumps(commands)
    File_object4.write(commands)
    print("The command outputs have been written to Commands.txt")

ipaddr = input("What is the IP-Address?")
username = input("What is the username?")
password = input("What is the password?")

# with junos_driver(**junos_device) as junos:
#   version = junos.cli(command="show system version")
# print(version)

junos_driver = get_network_driver('junos')
junos_device = {'username': username, 'password': password, 'hostname': ipaddr}

with junos_driver(**junos_device) as junos:
  shrun = junos.get_config()


with junos_driver(**junos_device) as junos:
  interfaces = junos.get_interfaces()

log = ['show log']
with junos_driver(**junos_device) as junos:
    logs = junos.cli(log)

commands = ['show version', 'show chassis hardware'] #These commands have the serial # + model #, just need to parse the data

with junos_driver(**junos_device) as junos:
    commands = junos.cli(commands)

writetohdd(interfaces, shrun, logs, commands) #This is creating files with SSH data
serialnum = parsingdata() #This is getting serial #
serialnum = re.sub(r'[^\w]', ' ', serialnum)
serialnum = serialnum.strip()

today = datetime.now
startfolder = r"D:\Testing\{}".format(today().strftime('%d-%m-%Y-'))
if os.path.exists('D:\Testing') == "False": #this is checking to see if the sub folder exists
    os.mkdir('D:\Testing')

elif os.path.exists('D:\Testing') == "True":
    if os.path.exists(startfolder = r"D:\Testing\{}".format(today().strftime('%d-%m-%Y-'))) == "false":
        startfolder = r"D:\Testing\{}".format(today().strftime('%d-%m-%Y-'))

# os.mkdir(FILLTHISOUTLATER) #You want folder to be Hostname.MODEL#.SERIAL  #WILL DO THIS LATER WITH ANOTHER LATER VERSION, SERIAL CHECK! NEED HOSTNAME + MODEL#s

startfolder2 =  startfolder + serialnum + "/"

newfilename = startfolder2  + "Logs.txt"
shutil.move("Logs.txt", newfilename)
newfilename = startfolder2 + "Running-Config.txt"
shutil.move("Running-Config.txt", newfilename)
newfilename = startfolder2 + "Interfaces.txt"
shutil.move("Interfaces.txt", newfilename)