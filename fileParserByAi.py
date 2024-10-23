import csv
import re

def parse_html_to_csv(input_html_file, output_csv_file):
    # Read the HTML file
    with open(input_html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Regular expressions to find required components
    author_regex = re.compile(r'<span[^>]*class="[^"]*chatlog__author[^"]*"[^>]*>(.*?)</span>', re.DOTALL)
    link_regex = re.compile(r'<a[^>]*href="([^"]*)"[^>]*>.*?</a>', re.DOTALL)
    message_regex = re.compile(r'<(span|div)[^>]*class="[^"]*chatlog__markdown-preserve[^"]*"[^>]*>(.*?)</\1>', re.DOTALL)

    # Extract data using regular expressions
    authors = author_regex.findall(html_content)
    links = link_regex.findall(html_content)
    messages = message_regex.findall(html_content)

    # Open CSV file for writing
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write the header row
        csvwriter.writerow(['Author', 'Link', 'Message'])

        # Calculate the length of the longest list to iterate all elements
        max_length = max(len(authors), len(links), len(messages))

        for i in range(max_length):
            author = authors[i].strip() if i < len(authors) else ''
            link = links[i].strip() if i < len(links) else ''
            message = messages[i][1].strip() if i < len(messages) else ''
            
            csvwriter.writerow([author, link, message])
    
    print(f"Data has been successfully written to {output_csv_file}")

if __name__ == "__main__":
    input_html_file = 'Legend of the Paladins_ The Forge - Special Channels - special-rp [541292593695293470].html'  # Replace with your input HTML file name
    output_csv_file = 'output.csv'  # Replace with your output CSV file name
    parse_html_to_csv(input_html_file, output_csv_file)