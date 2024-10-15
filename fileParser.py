from html.parser import HTMLParser

# To use this, replace fileName with the name of the HTML file you want to parse string from.
# The output file is called output.txt

class MyHTMLParser(HTMLParser):
    # def handle_starttag(self, tag, attrs):
    #     # print("Encountered a start tag:", tag)

    # def handle_endtag(self, tag):
    #     # print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)
        ftwo.write(data)

fileName = "Legend of the Paladins_ The Forge - Special Channels - special-rp [541292593695293470].html"
output = "output.txt"

f = open(fileName, "r")
ftwo = open(output, "a")
parser = MyHTMLParser()

for x in f:
    parser.feed(x)
    