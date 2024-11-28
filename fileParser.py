from html.parser import HTMLParser
from enum import Enum
import os
import datetime
import csv
import re
import json

# ----------------------------------------------------------------------------------------------------

newLine = '\n'

# To use this, replace fileName with the name of the HTML file you want to parse string from.
# The output file is called output.txt
fileName = "test.html" 
output = "output.txt"
output_debug = "output-debug.txt"
csv_output = "output.csv"

users = [
    'attorney_lucifer',
    'ikori_coolguy',
    'pat.jesus',
    'Deleted User'
]

alias = [
    "Lex, Just The King",
    "The Plague Bearer",
    "King in Yellow",
    "Deleted User"
]

strsToLookFor = [
    "chatlog__timestamp",
    "chatlog__markdown-preserve",
    "chatlog__short-timestamp"
]

chatLog = {}

NAME = 1
DATE_TIME = 2
TEXT = 3


# ----------------------------------------------------------------------------------------------------

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # PRESERVE THE ACTION SYNTAX FROM THE CHAT
        if(tag == "em"):
            f_TWO.write("*")
        if tag == "a":
            f_TWO.write(newLine)

    def handle_endtag(self, tag):
        # PRESERVE THE ACTION SYNTAX FROM THE CHAT
        if(tag == "em"):
            f_TWO.write("*")
        if tag == "a":
            f_TWO.write(newLine)
        

    def handle_data(self, data):
        user1 = re.search(alias[0], data)
        user2 = re.search(alias[1], data)
        user3 = re.search(alias[2], data)
        user4 = re.search(alias[3], data)
        dateTime = re.search("\d", data)

        if user1 != None:
            debug.write("name: ")

        elif user2 != None:
            debug.write("name: ")

        elif user3 != None:
            debug.write("name: ")

        elif user4 != None:
            debug.write("name: ")

        elif dateTime != None:
            debug.write("date&time: ")

        elif data != " ":
            debug.write(" ")
        
        elif data != newLine:
            debug.write("---")


        updateChatLog(data)
        debug.write(data)
        debug.write(newLine)

        # WRITES THE DATA TO THE OUTPUT FILE
        f_TWO.write(data)

# ----------------------------------------------------------------------------------------------------

def updateChatLog(data):
    if(data != " " or data != newLine):
        print("Updating chatLog with ")
        print(data)
        print(" at id: ")
        print(intId)
        chatLog['id':intId] = {'msgId':msgId,'data':data}
        intId+=1

    
# ----------------------------------------------------------------------------------------------------

# READ THE GIVEN FILENAME
f = open(fileName, "r")
print("Reading file now...")

# IF OLD OUTPUT FILE IS STILL THERE, REPLACE IT
if os.path.exists(output):
  print("Deleting old output file...")
  os.remove(output)

# CREATE OUTPUT FILE
f_TWO = open(output, "a")
print("Created output file")

# OPEN HTML PARSER
parser = MyHTMLParser()

if os.path.exists(output_debug):
    print("Deleting old output debug file...")
    os.remove(output_debug)

debug = open(output_debug, "a")
print("Created debug output file")

# GRAB CURRENT DATE AND TIME
today  = datetime.datetime.now()
print(today)


# START WRITING TO FILE
msgId = 0
intId = 0
f_TWO.write(today.strftime("%x"))
f_TWO.write(newLine)
for x in f:
    # NEW MESSAGE TO PUT IN CSV FILE  
    parser.feed(x)
    f_TWO.write(newLine)
    msgId+=1
    parser.close()

debug.write(json.dumps(chatLog,indent=4))

with open(csv_output, 'w', newline='') as csvfile:
    fieldnames = ['id','msgId','data']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(chatLog)