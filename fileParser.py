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

class msgData(Enum):
    name = 0
    dat = 1
    text = 2

class msgType(Enum):
    NAME = 1
    DATE_TIME = 2
    TEXT = 3

indicator = msgType.NAME

# ----------------------------------------------------------------------------------------------------

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        debugWrite1(tag)

        print("Encountered an attribute: ", attrs)

        for attr in attrs:
            debugWrite2(attr)

        # PRESERVE THE ACTION SYNTAX FROM THE CHAT
        if(tag == "em"):
            f_TWO.write("*")

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        debugWrite1(tag)

        # PRESERVE THE ACTION SYNTAX FROM THE CHAT
        if(tag == "em"):
            f_TWO.write("*")
        if tag == "a":
            f_TWO.write(newLine)
        

    def handle_data(self, data):
        # print("Encountered some data  :", data)
        debugWrite3(data)

        # WRITES THE DATA TO THE OUTPUT FILE
        f_TWO.write(data)

# ----------------------------------------------------------------------------------------------------

def debugWrite1(tag):
    debug.write("tag: ")
    debug.write(tag)
    debug.write(newLine)   

def debugWrite2(attr):
    debug.write("attrible: ")
    debug.write(attr[1])
    debug.write(newLine)

def debugWrite3(data):
    debug.write("data: ")
    debug.write(data)
    debug.write(newLine)

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
print("Created output file")

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

    
parser.close()