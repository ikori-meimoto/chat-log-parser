from html.parser import HTMLParser
import os
import datetime
import csv
import json
import re

# ----------------------------------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------------------------------
fileName = "Legend of the Paladins_ The Forge - Special Channels - special-rp [541292593695293470].html" 
output = "output.txt"
output_debug = "output-debug.txt"
csv_output = "output.csv"

# Global data structure to hold parsed messages
chatLog = []
message_id_counter = 0

# ----------------------------------------------------------------------------------------------------

class MyHTMLParser(HTMLParser):
    def __init__(self, output_file, debug_file):
        super().__init__()
        # State variables
        self.in_author = False
        self.in_content = False
        self.current_author = ""
        self.current_content = ""
        self.last_author = ""  # New: Stores the author of the last message group
        self.output_file = output_file
        self.debug_file = debug_file
        self.msg_id = 0
        self.message_parts = []
        
    def _is_class(self, attrs, class_name):
        """Helper to check if a specific class exists in the attributes list."""
        for attr, value in attrs:
            if attr == 'class':
                # Discord HTML often has multiple classes; we check if our target is present
                return class_name in value.split()
        return False

    def handle_starttag(self, tag, attrs):
        # 1. Start of Author Name (Found only in the first message of a group)
        if tag == 'span' and self._is_class(attrs, 'chatlog__author'):
            self.in_author = True
            self.current_author = "" # Reset author for the new message
            
        # 2. Start of Message Content
        elif tag == 'span' and self._is_class(attrs, 'chatlog__markdown-preserve'):
            self.in_content = True
            self.current_content = "" # Reset content for the new message
            
        # 3. Handle special tags within the message content
        if self.in_content:
            if tag == "em":
                self.current_content += "*"
            elif tag == "a":
                # Add a space before links to separate them from previous text
                self.current_content += " "

    def handle_endtag(self, tag):
        # 1. End of Author Name
        if self.in_author and tag == 'span':
            self.in_author = False
        
        # 2. End of Message Content
        elif self.in_content and tag == 'span':
            self.in_content = False

        # 3. Finalize and Write Message
        # The 'chatlog__message' div closes the individual message wrapper.
        # This is a better trigger for finalizing a message than 'chatlog__message-primary'
        # because the latter is sometimes missing for non-primary grouped messages.
        if tag == 'div' and self._is_class([('class', 'chatlog__message')], 'chatlog__message'):
            self.finalize_message()

        # 4. Handle special tags within the message content
        # Note: We keep the closing formatting outside of in_content state check for consistency
        if tag == "em":
            self.current_content += "*"
        # For links, we may just leave the URL which is handled by handle_data/finalize

    def handle_data(self, data):
        # Clean up data (strip leading/trailing whitespace, but preserve internal newlines)
        cleaned_data = data.strip()
        
        if self.in_author:
            # Append author name parts. This updates the author for the current message and the group.
            self.current_author += data.strip()
            # Update last_author immediately upon finding an author
            self.last_author = self.current_author
            
        elif self.in_content:
            # Append message content parts
            self.current_content += data
            
        # Debugging output
        if cleaned_data:
            self.debug_file.write(f"[{self.in_author}][{self.in_content}] Data: {repr(data)}\n")

    def finalize_message(self):
        """Assembles the current message and writes it to the output file and chatLog."""
        global message_id_counter
        
        # If current_author is empty (subsequent message in a group), use the last known author.
        author = self.current_author.strip()
        if not author:
            author = self.last_author.strip()

        content = self.current_content.strip()
        
        # Ensure we have both author (from current message or fallback) and content before logging
        if author and content:
            # Write to output.txt in the requested format
            formatted_message = f"{author}: {content}\n"
            self.output_file.write(formatted_message)
            
            # Add to the global chatLog structure for CSV export
            chatLog.append({
                'id': message_id_counter,
                'msgId': self.msg_id, # This is the message's position in the sequence
                'author': author,
                'data': content
            })
            message_id_counter += 1
            
        # Reset current message state, but preserve last_author for the next message in the group
        self.current_author = ""
        self.current_content = ""
        self.msg_id += 1 # Increment for every message processed, grouped or not


# ----------------------------------------------------------------------------------------------------
# Main Execution Logic
# ----------------------------------------------------------------------------------------------------

# Delete old output files if they exist
for f_path in [output, output_debug, csv_output]:
    if os.path.exists(f_path):
        os.remove(f_path)

print(f"Reading file: {fileName}...")

try:
    with open(fileName, "r", encoding="utf-8") as f_input:
        file_content = f_input.read()
except FileNotFoundError:
    print(f"Error: Input file '{fileName}' not found.")
    exit()
except Exception as e:
    print(f"Error reading input file: {e}")
    exit()

# Open output files
with open(output, "a", encoding="utf-8") as f_out, \
     open(output_debug, "a", encoding="utf-8") as f_debug:

    # Write current date/time to the top of the main output file
    today = datetime.datetime.now()
    f_out.write(today.strftime("%x") + '\n\n')

    # Initialize and feed the parser
    parser = MyHTMLParser(f_out, f_debug)
    parser.feed(file_content)
    parser.close()
    
    f_debug.write("\n--- Final chatLog JSON ---\n")
    f_debug.write(json.dumps(chatLog, indent=4))

print(f"Successfully created main output file: {output}")
print(f"Successfully created debug output file: {output_debug}")


# Write CSV file
with open(csv_output, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['id', 'msgId', 'author', 'data']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    # Use the structured data from chatLog
    for msg in chatLog:
        try:
            writer.writerow(msg)
        except Exception as e:
            print(f"Error writing message {msg['id']} to CSV: {e}")

print(f"Successfully created CSV output file: {csv_output}")

# ----------------------------------------------------------------------------------------------------
