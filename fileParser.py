from html.parser import HTMLParser
from enum import Enum
import os
import datetime
import csv

newLine = '\n'

# To use this, replace fileName with the name of the HTML file you want to parse string from.
# The output file is called output.txt
fileName = "Legend of the Paladins_ The Forge - Special Channels - special-rp [541292593695293470].html" 
output = "output.txt"
csv_output = "output.csv"

chatLog = [
    ["NAME","DATE & TIME", "TEXT"]
]

users = [
    'attorney_lucifer',
    'ikori_coolguy',
    'pat.jesus',
    'Deleted User'
]

class msgData(Enum):
    name = 0
    dat = 1
    text = 2

class msgType(Enum):
    NAME = 1
    DATE_TIME = 2
    TEXT = 3

indicator = msgType.NAME

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        # print("Encountered an attribute: ", attrs)

        for user in users:
            if attrs['title'] == user:
                indicator = msgType.NAME
        if attrs['class'] == 'chalog__timestamp':
            print("Date & Time is ", attrs['title'])
            indicator = msgType.DATE_TIME
        else:
            indicator = msgType.TEXT
        # PRESERVE THE ACTION SYNTAX FROM THE CHAT
        if(tag == "em"):
            ftwo.write("*")

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        # PRESERVE THE ACTION SYNTAX FROM THE CHAT
        if(tag == "em"):
            ftwo.write("*")

    def handle_data(self, data):
        # print("Encountered some data  :", data)
        # WRITES THE DATA TO THE OUTPUT FILE

        if indicator == msgType.NAME:
            currentName = data
            ftwo.write(data)
            ftwo.write(" ")
        elif indicator == msgType.DATE_TIME:
            currentDAT = data
            ftwo.write(data) 
            ftwo.write(newLine)
        elif indicator == msgType.TEXT:
            currentText = data
            ftwo.write(data)
            ftwo.write(newLine)

        

# def csv_save(currentName, currentDAT, currentText):
#     currentMsg = [
#         currentName,
#         currentDAT,
#         currentText
#     ]

#         # Open the file in write mode
#     with open(csv_output, mode='w', newline='') as file:
#         # Create a csv.writer object
#         writer = csv.writer(file)
#         # Write data to the CSV file
#         writer.writerows(data)


# READ THE GIVEN FILENAME
f = open(fileName, "r")
print("Reading file now...")

# IF OLD OUTPUT FILE IS STILL THERE, REPLACE IT
if os.path.exists(output):
  print("Deleting old output file...")
  os.remove(output)

# CREATE OUTPUT FILE
ftwo = open(output, "a")
print("Created output file")

# OPEN HTML PARSER
parser = MyHTMLParser()

# GRAB CURRENT DATE AND TIME
today  = datetime.datetime.now()
print(today)


# START WRITING TO FILE
ftwo.write(today.strftime("%x"))
ftwo.write(newLine)
for x in f:
    # NEW MESSAGE TO PUT IN CSV FILE  
    parser.feed(x)
    ftwo.write(newLine)

    
parser.close()