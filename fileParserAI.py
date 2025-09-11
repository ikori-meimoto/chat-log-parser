from html.parser import HTMLParser
import os
import datetime
import csv
import re
import json

fileName = "Legend of the Paladins_ The Forge - Special Channels - special-rp [541292593695293470].html"
output = "output.txt"
output_debug = "output-debug.txt"
csv_output = "output.csv"

alias = [
    "Lex, Just The King",
    "The Plague Bearer",
    "King in Yellow",
    "Deleted User"
]

chatLog = {}
current_user = None
current_datetime = None
newLine = '\n'

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current_tag = None
        self.intId = 0
        self.msgId = 0

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag == "em":
            self.f_TWO.write("*")
        elif tag == "a":
            self.f_TWO.write(newLine)

    def handle_endtag(self, tag):
        if tag == "em":
            self.f_TWO.write("*")
        elif tag == "a":
            self.f_TWO.write(newLine)
        self.current_tag = None

    def handle_data(self, data):
        global current_user
        global current_datetime

        if re.search(r"|".join(alias), data):
            if current_user != data.strip():
                current_user = data.strip()
                current_datetime = None  # Reset datetime when the user changes
                self.msgId += 1
                self.f_TWO.write(data + newLine)  # Write user and add newline
            self.debug.write("name: ")
        elif re.search(r"\d", data):
            if current_datetime != data.strip():
                current_datetime = data.strip()
            self.debug.write("date&time: ")
        elif data.strip() == "":
            self.debug.write(" ")
            return
        else:
            self.debug.write("text: ")

        self.update_chat_log(data)
        self.debug.write(data + newLine)
        if re.search(r"|".join(alias), data) is None:  # Ensure we don't write an extra newline after the user
            self.f_TWO.write(data)

    def update_chat_log(self, data):
        if data.strip() and data.strip() != newLine:
            self.intId += 1
            chatLog[self.intId] = {'id': self.intId, 'msgId': self.msgId, 'data': data}

def parse_html(fileName, output, output_debug, csv_output):
    with open(fileName, "r") as f:
        file_data = f.read()

    if os.path.exists(output):
        os.remove(output)

    if os.path.exists(output_debug):
        os.remove(output_debug)

    with open(output, "a") as f_TWO, open(output_debug, "a") as debug:
        parser = MyHTMLParser()
        parser.f_TWO = f_TWO
        parser.debug = debug

        today = datetime.datetime.now().strftime("%x")
        f_TWO.write(today + newLine)
        parser.feed(file_data)

    with open(csv_output, 'w', newline='') as csvfile:
        fieldnames = ['id', 'msgId', 'data']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in chatLog.values():
            writer.writerow(item)

parse_html(fileName, output, output_debug, csv_output)
