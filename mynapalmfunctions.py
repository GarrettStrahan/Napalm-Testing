from grepfunc import grep
import json
import re

def parsingdata(): #Data is parsed for serial#
    file_object = open("Commands.txt", 'r')
    data = file_object.readlines()
    data = json.dumps(data)
    new_data = re.findall(r"\b[A-Z0-9]{12}\b", data) #this looks for 12 digits or capital letters
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


def gethostname(shrun):
    hostname = grep(shrun, "host-name", "i=True")
    print("The hostname has been extracted.txt")
    print(hostname)
    return hostname
