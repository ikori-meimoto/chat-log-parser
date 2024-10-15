from html.parser import HTMLParser
import os
import datetime
import re

newLine = '\n'

# To use this, replace fileName with the name of the HTML file you want to parse string from.
# The output file is called output.txt
fileName = "Legend of the Paladins_ The Forge - Special Channels - special-rp [541292593695293470].html" 
output = "output.txt"

# 

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        if(tag == "em"):
            ftwo.write("*")

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        if(tag == "em"):
            ftwo.write("*")

    def handle_data(self, data):
        # print("Encountered some data  :", data)
        ftwo.write(data)

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
print("Current date is ")
print(today)
print(".")

# START WRITING TO FILE
ftwo.write(today.strftime("%x"))
ftwo.write(newLine)
for x in f:
    parser.feed(x)
    ftwo.write(newLine)
    