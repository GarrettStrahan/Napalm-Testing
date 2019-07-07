from napalm import get_network_driver
import json

def writetohddwithdictionaryvar(interfaces, shrun):

    File_object = open("Interfaces.txt", "w")
    File_object.write(json.dumps(interfaces))
    print("The interfaces has been been written to Interfaces.txt")


    File_object2 = open("Running-Config.txt", "w")
    File_object2.write(json.dumps(shrun))
    print("The Running-configuration has been been written to Running-Config.txt")

ipaddr = input("What is the IP-Address?")
username = input("What is the username?")
password = input("What is the password?")


junos_driver = get_network_driver('junos')
junos_device = {'username': username, 'password': password, 'hostname': ipaddr}

with junos_driver(**junos_device) as junos:
  shrun = junos.get_config()

with junos_driver(**junos_device) as junos:
  interfaces = junos.get_interfaces()


writetohdd(interfaces, shrun)
