import pandas as pd

fileName = "output.csv"
debugFileName = "chat_log_debug.txt"
outputHTMLFileName = "chat_log.html"
chatLog = []

main_html_content_begin = f"""
<!DOCTYPE html>
<head>
    <title>Chat Log</title>
</head>
<body>
"""
main_html_content_end = """
</body>
</html>
"""


df=pd.read_csv(fileName,header=0, index_col='id')
# print(df)

for index, row in df.iterrows():
    chatEntry = {
        "user": row['author'],
        "content": row['data']
    }
    # print(chatEntry)
    chatLog.append(chatEntry)

for entry in chatLog:
    msg_html_content = f"""
    <div class="chat-entry">
        <p><strong>{entry['user']}:</strong> {entry['content']}</p>
    </div>
    """
    main_html_content_begin += msg_html_content

main_html_content_begin += main_html_content_end

try:
    with open(outputHTMLFileName, "w") as f:
        f.write(main_html_content_begin)
    print(f"HTML file '{outputHTMLFileName}' generated successfully.")
except IOError as e:
    print(f"Error writing to file: {e}")


try:
    with open(debugFileName, "w") as f:
        for entry in chatLog:
            f.write(f"User: {entry['user']}\n")
            f.write(f"Content: {entry['content']}\n")
            f.write("-" * 40 + "\n")
    print("Debug file written successfully.")
except IOError as e:
    print(f"Error writing debug file: {e}")