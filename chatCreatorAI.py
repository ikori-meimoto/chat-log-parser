import pandas as pd
import re
import hashlib # For a stable color generation based on character name

fileName = "output.csv"
debugFileName = "chat_log_debug.txt"
outputHTMLFileName = "chat_log.html"
chatLog = []
all_extracted_characters = set()

# --- Predefined list of colors (you can extend this!) ---
# These are Tailwind CSS text colors for easy integration.
# You could also use hex codes like '#FF0000'
COLOR_PALETTE = [
    "text-red-700", "text-blue-700", "text-green-700", "text-purple-700",
    "text-yellow-700", "text-indigo-700", "text-pink-700", "text-teal-700",
    "text-orange-700", "text-cyan-700", "text-lime-700", "text-fuchsia-700"
]

# --- 1. Read CSV and Populate chatLog ---
try:
    df = pd.read_csv(fileName, header=0, index_col='id')
except FileNotFoundError:
    print(f"Error: Input file '{fileName}' not found. Please ensure it exists.")
    exit()

for index, row in df.iterrows():
    if 'author' in row and 'data' in row:
        chatEntry = {
            "user": row['author'],
            "content": row['data']
        }
        chatLog.append(chatEntry)
    else:
        print(f"Warning: Row {index} missing 'author' or 'data' column.")

# --- 2. Extract Characters from Dialogue Content ---
pattern = r"^(.*?): "

EXCLUDED_PHRASES = {
    "(I forgot to put this in, and entirely up to you, but the song that would play when I was speaking",
    "*Aiden guides the group some distance, eventually traveling into the valleys and hills beyond the city. It is not until another sudden wave if heat passes the area that it is obvious everyone is closing in. Eventually Aiden stops everyone, pointing to a large opening in the side of one of the mountains. It is an elegant structure, to say the least, and has colored banners outside similar to that of my own colors",
    "*It's a cold, however not so peaceful night. The streets outside of the castle are filled with people, all of them holding different forms of weaponry, *other soldiers join as well*",
    "other soldiers join as well",
    "aiden"
}
EXCLUDED_PHRASES_LOWER = tuple(phrase.lower().strip() for phrase in EXCLUDED_PHRASES)

for entry in chatLog:
    matches = re.findall(pattern, entry['content'], re.MULTILINE)
    for character_name in matches:
        clean_name = character_name.strip()
        if clean_name and clean_name.lower() not in EXCLUDED_PHRASES_LOWER:
            all_extracted_characters.add(clean_name)

unique_characters = sorted(list(all_extracted_characters))

# --- NEW: Generate a stable color map for each character ---
character_color_map = {}
for i, char_name in enumerate(unique_characters):
    # Use hashlib to create a consistent, hash-based index for color
    # This ensures "Me" always gets the same color, "Aurra" always gets another, etc.,
    # regardless of their order in 'unique_characters' if the list ever shifts
    hash_object = hashlib.md5(char_name.encode())
    hash_int = int(hash_object.hexdigest(), 16)
    color_index = hash_int % len(COLOR_PALETTE)
    character_color_map[char_name] = COLOR_PALETTE[color_index]


characters_list_str = ', '.join(unique_characters) if unique_characters else 'No dialogue characters found.'


# --- 3. HTML Generation ---
main_html_content_begin = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Log</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{ font-family: 'Inter', sans-serif; }}
        /* Specific styles for character names (if you want more than just the text color) */
        .character-name {{ font-weight: bold; }}
    </style>
</head>
<body class="bg-gray-50 p-6 md:p-10">
    <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl font-extrabold text-gray-900 mb-6 border-b pb-2">Chat Log Transcript</h1>

        <div class="bg-indigo-50 p-4 rounded-lg shadow-md mb-8 border-l-4 border-indigo-400">
            <h2 class="text-xl font-semibold text-indigo-700 mb-2">Characters Identified:</h2>
            <p class="text-indigo-800 font-mono text-base break-words">
                {characters_list_str}
            </p>
        </div>

        <div class="space-y-4">
"""
main_html_content_end = """
        </div>
    </div>
</body>
</html>
"""

# Append chat entries to the beginning content
current_html_content = main_html_content_begin
for entry in chatLog:
    # Escape HTML special characters for safe rendering
    content_raw = entry['content']
    
    # Process content to color character names
    processed_content_lines = []
    for line in content_raw.split('\n'):
        match = re.match(pattern, line) # Use the same pattern to identify character lines
        if match:
            char_name_in_line = match.group(1).strip()
            
            # Check if this is an identified character and has a color mapping
            if char_name_in_line in character_color_map:
                color_class = character_color_map[char_name_in_line]
                dialogue_part = line[len(match.group(0)):].strip() # Get text after "Name: "
                
                # Apply color to the character name and potentially the entire line
                # I'm applying it to the whole line for simplicity, but you could target just the name.
                # For example: <span class="{color_class}">{char_name_in_line}:</span> {dialogue_part}
                
                # Escape dialogue part for HTML safety
                escaped_dialogue_part = dialogue_part.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

                processed_content_lines.append(
                    f'<span class="character-name {color_class}">{char_name_in_line}:</span> '
                    f'<span class="text-gray-800">{escaped_dialogue_part}</span>' # Dialogue in a neutral color
                )
            else:
                # If not a recognized character or not a character line, just escape and add
                processed_content_lines.append(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
        else:
            # If line doesn't match the character pattern, just escape and add
            processed_content_lines.append(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
            
    # Join processed lines back with <br> for HTML newlines
    content_html = "<br>".join(processed_content_lines)

    msg_html_content = f"""
    <div class="chat-entry p-4 bg-white rounded-lg shadow-sm border border-gray-200">
        <p class="text-sm text-gray-500 mb-1">Source Author: <strong class="text-gray-700">{entry['user']}</strong></p>
        <p class="text-gray-800 leading-relaxed">{content_html}</p>
    </div>
    """
    current_html_content += msg_html_content

current_html_content += main_html_content_end

# --- 4. Write HTML File ---
try:
    with open(outputHTMLFileName, "w") as f:
        f.write(current_html_content)
    print(f"HTML file '{outputHTMLFileName}' generated successfully.")
except IOError as e:
    print(f"Error writing HTML file: {e}")


# --- 5. Write Debug File ---
try:
    with open(debugFileName, "w") as f:
        f.write(f"--- Identified Characters ({len(unique_characters)} total) ---\n")
        f.write(f"{characters_list_str}\n\n")
        f.write(f"--- Character Color Map ---\n")
        for char, color in character_color_map.items():
            f.write(f"{char}: {color}\n")
        f.write("-" * 50 + "\n\n")

        for entry in chatLog:
            f.write(f"Source User: {entry['user']}\n")
            f.write(f"Content:\n{entry['content']}\n")
            f.write("-" * 40 + "\n")
    print("Debug file written successfully.")
except IOError as e:
    print(f"Error writing debug file: {e}")