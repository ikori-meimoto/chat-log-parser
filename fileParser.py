from html.parser import HTMLParser
from enum import Enum
import os
import datetime
import csv
import re

# ----------------------------------------------------------------------------------------------------

newLine = '\n'

# To use this, replace fileName with the name of the HTML file you want to parse string from.
# The output file is called output.txt
fileName = "Legend of the Paladins_ The Forge - Special Channels - special-rp [541292593695293470].html" 
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

id = 0

# ----------------------------------------------------------------------------------------------------

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        # print("Encountered an attribute: ", attrs)
        # debugWrite1(tag)

        # for attr in attrs:
        #     this = attr[1]
            
        #     print("attr[1]: ", attr[1])
        #     debugWrite2(attr)


        # PRESERVE THE ACTION SYNTAX FROM THE CHAT
        if(tag == "em"):
            f_TWO.write("*")
        if tag == "a":
            f_TWO.write(newLine)

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        # debugWrite1(tag)

        # PRESERVE THE ACTION SYNTAX FROM THE CHAT
        if(tag == "em"):
            f_TWO.write("*")
        if tag == "a":
            f_TWO.write(newLine)
        

    def handle_data(self, data):
        # print(newLine)
        # print("Encountered some data  :", data)

        dtReg = "(\d{1}|\d{2})/(\d{1}|\d{2})/(\d{4}) (\d{1}|\d{2}):(\d{2}):(\d{2}) AM|(\d{1}|\d{2})/(\d{1}|\d{2})/(\d{4}) (\d{1}|\d{2}):(\d{2}):(\d{2}) PM"

        user1 = re.search(alias[0], data)
        user2 = re.search(alias[1], data)
        user3 = re.search(alias[2], data)
        user4 = re.search(alias[3], data)
        dateTime = re.search("\d", data)

        if user1 != None:
            ugh(NAME, data)

            # print("user ", 1, ": ", user1)
            debug.write("name: ")
            # print("name: ", data)

        elif user2 != None:
            ugh(NAME, data)

            # print("user ", 2, ": ", user2)
            debug.write("name: ")
            # print("name: ", data)

        elif user3 != None:
            ugh(NAME, data)

            # print("user ", 3, ": ", user3)
            debug.write("name: ")
            # print("name: ", data)

        elif user4 != None:
            ugh(NAME, data)

            # print("user ", 4, ": ", user4)
            debug.write("name: ")
            # print("name: ", data)

        elif dateTime != None:
            ugh(DATE_TIME, data)

            # print("dateTime: ", dateTime)
            debug.write("date&time: ")
            # print("date&time: ", data)

        elif data != " ":
            ugh(TEXT, data)

            # print("This is text")
            debug.write(" ")
            # print("text: ", data)
        
        elif data != newLine:
            ugh(TEXT, data)

            # print("This is text")
            debug.write("---")
            # print("text: ", data)

        debug.write(data)
        debug.write(newLine)

        # WRITES THE DATA TO THE OUTPUT FILE
        f_TWO.write(data)

# ----------------------------------------------------------------------------------------------------

def ugh(type, data):
    msg = [
        id
    ]

    if(type == NAME):
        msg.append(data) 
    elif type == DATE_TIME:
        msg.append(data)
    elif type == TEXT:
        msg.append(data)

    chatLog.update({id:msg})
    # print(chatLog.get(id))
    # print(" compare to ")
    # print(msg)

    
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
f_TWO.write(today.strftime("%x"))
f_TWO.write(newLine)
for x in f:
    # NEW MESSAGE TO PUT IN CSV FILE  
    parser.feed(x)
    f_TWO.write(newLine)
    id+=1
    parser.close()

with open('output.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'msg']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(chatLog)