from napalm import get_network_driver
import json #its needed for the mynaplmfunctions, you can more than likely delete this line.
import os
import shutil
import re
from datetime import datetime
from grepfunc import grep #its needed for the mynaplmfunctions, you can more than likely delete this line.
import mynapalmfunctions
import sys

ipaddr = input("What is the IP-Address?")
username = input("What is the username?")
password = input("What is the password?")


junos_driver = get_network_driver('junos')

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


#BELOW THIS LINE IS BETA IT DOES NOT WORK AS OF YET!

cmd = "set interfaces lo0 unit 0 family inet address 1.1.1.1/32" #does not help


#merge config
with junos_driver(**junos_device) as junos:
#    optional_args={'inline_transfer': True} #might have to delete this, it was from a forum has not seemed to help.
#    junos_driver.load_merge_candidate(filename=r'C:\Users\garre\PycharmProjects\NAPALM_Testing\config.txt', config=None)
#    junos_driver.load_merge_candidate(filename='conf.cfg') #This file is on the root of the SRX210, failed!
#    junos_driver.load_merge_candidate(filename='conf.txt') #This file is in the project folder, failed!
    junos_driver.load_merge_candidate(config='set interfaces lo0 unit 0 family inet address 1.1.1.1/32')
#    junos_driver.load_merge_candidate(config=cmd) #this is a variable, failed!
    diffs = junos_driver.compare_config()
    if diffs == "":
        print("Configuration already applied")
        junos_driver.discard_config()
    else:
        print(diffs)
        yesno = input('\nApply changes? [y/N] ').lower()
        if yesno == 'y' or yesno == 'yes':
            print("Applying changes...")
            junos_driver.commit_config()
        else:
            print("Discarding changes...")
            junos_driver.discard_config()


#replacing configuration
'''
with junos_driver(**junos_device) as junos:
    junos_driver.load_replace_candidate(filename='config')
    diffs = junos_driver.compare_config()
    if diffs == "":
        print("Configuration already applied")
        junos_driver.discard_config()
    else:
        print(diffs)
        yesno = input('\nApply changes? [y/N] ').lower()
        if yesno == 'y' or yesno == 'yes':
            print("Applying changes...")
            junos_driver.commit_config()
        else:
            print("Discarding changes...")
            junos_driver.discard_config()
'''

print("BING, DONE! Have a NiCe DaY!")

#https://github.com/ksator/junos-automation-with-NAPALM/wiki/How-to-use-NAPALM-with-Python
#https://github.com/napalm-automation/napalm-ios/issues/168
#load_merge_candidate(filename=None, config=None)
#load_replace_candidate(filename=None, config=None)
#https://napalm.readthedocs.io/en/latest/tutorials/first_steps_config.html
#https://web.archive.org/web/20181006052856/http://www.networktocode.com/labs/tutorials/how-to-use-napalm-python-library-to-manage-ios-devices/
#https://projectme10.wordpress.com/2015/12/07/adding-cisco-ios-support-to-napalm-network-automation-and-programmability-abstraction-layer-with-multivendor-support/
#https://www.bernhard-ehlers.de/blog/2017/07/04/napalm-cisco-juniper.html
