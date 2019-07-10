from napalm import get_network_driver
import os
import shutil
import re
from datetime import datetime
from grepfunc import grep #its needed for the mynaplmfunctions, you can more than likely delete this line.
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

today = datetime.now
startfolder = r"D:\Testing\{}".format(today().strftime('%m-%d-%Y-')) + serialnum

if os.path.exists('D:\Testing') == False: #this is checking to see if the sub folder exists
    os.mkdir('D:\Testing')

elif os.path.exists('D:\Testing') == True:
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


#Sending configuration commands below this line:
driver = get_network_driver('junos')
device = driver(ipaddr, username, password)
device.open()
device.load_merge_candidate(config="set interfaces lo0 unit 0 family inet address 1.1.1.4/24")
#device.load_replace_candidate(filename=) #beta feature not supported yet. To replace the current configuration with a new configuration.
device.commit_config()
device.close()

print("BING, DONE! Have a NiCe DaY!")
