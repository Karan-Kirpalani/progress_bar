from datetime import datetime

import pandas as pd

# Load the Google Sheets data
sheet_id = '1rpoTrB7wep7eA7MNyamobJ8ArYpNZ62iM5ufSQo75s0'
df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

# Initialize variables
weight = []
names = []
due_dates = []
priority = []

# Get the current time
current_time = datetime.now()

# Read and process the data from the DataFrame
rows, columns = df.shape

for i in range(rows):
    names.append(df.loc[i, 'Name'])
    weight.append(df.loc[i, 'Weight'])
    date = df.loc[i, 'Due Date']
    due_dates.append(datetime.strptime(date, '%d/%m/%Y %H:%M'))

# Calculate priority scores
for i in range(rows):
    importance = 5  # Base importance score

    # Adjust importance based on weight
    if weight[i] == "major assessment":
        importance += 5
    elif weight[i] == "minor assessment":
        importance += 3
    else:
        importance += 1

    # Calculate days left
    days_left = (due_dates[i] - current_time).days

    # Adjust importance based on due date
    if days_left < 0:
        importance += 5  # Overdue tasks get extra points
    else:
        importance += max(0, 30 - days_left)  # Closer deadlines get higher priority

    # Append the calculated priority
    priority.append(importance)

# Combine tasks into a list and rank them by priority
tasks = list(zip(names, due_dates, weight, priority))
tasks.sort(key=lambda x: x[3], reverse=True)  # Sort by priority (highest first)
task = []

# Print the ranked tasks
print("Ranked Tasks:")
for task in tasks:
    print(f"Name: {task[0]}, Due Date: {task[1]}, Weight: {task[2]}, Priority: {task[3]}")

# Print sorted due dates (if needed)
print("\nSorted Due Dates:")
print(sorted(due_dates))
with open("sorted.csv", "w") as f:
    f.write("Name,Due Date,Weight,Priority\n")
    for task in tasks:
        f.write(f"{task[0]},{task[1]},{task[2]},{task[3]}\n")

sd = pd.read_csv("sorted.csv")
sd.to_html("sorted.html")

with open("blank.html", "a") as main_file, open("sorted.html", "r") as append_file:
    # Read content from the file to be appended
    content_to_append = append_file.read()
    # Append the content to the main file
    main_file.write(content_to_append)

print("HTML content appended successfully.")

# Read content from sorted.html
try:
    with open("blank.html", "r", encoding="utf-8") as sorted_file:
        sorted_content = sorted_file.read()
except FileNotFoundError:
    print("Error: blank.html not found.")
    exit(1)

try:
    with open("index.html", "w", encoding="utf-8") as index_file:
        index_file.write(sorted_content)
    print("Content has been successfully copied to index.html.")
except Exception as e:
    print(f"Error writing to index.html: {e}")


source_file2 = "extra.html"
target_file2 = "blank.html"

try:
    with open(source_file2, "r") as source:
        content = source.read()  # Read content from the source file

    with open(target_file2, "w") as target:
        target.write(content)  # Overwrite the target file with the content

    print(f"The contents of '{target_file2}' have been replaced with those from '{source_file2}'.")
except Exception as e:
    print(f"An error occurred: {e}")

