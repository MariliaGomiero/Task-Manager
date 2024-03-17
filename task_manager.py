# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

# Importing libraries
import os
from datetime import datetime

# Constants
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Function to register a new user
def register_user(username_password):
    """Function to register a new user."""
    while True:
        new_username = input("New Username: ")
        if new_username in username_password:
            print("Username already exists. Please choose a different username.")
        else:
            break

    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            user_data = [f"{k};{username_password[k]}" for k in username_password]
            out_file.write("\n".join(user_data))
    else:
        print("Passwords do not match")

# Function to add a new task
def add_task(username_password, task_list):
    """Function to add a new task."""
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    curr_date = datetime.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

# Function to view all tasks
def view_all(task_list):
    """Function to view all tasks."""
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

# Function to view tasks assigned to the current user
def view_mine(task_list, curr_user):
    """Function to view tasks assigned to the current user."""
    print("Tasks Assigned to You:")
    
    for i, t in enumerate(task_list, start=1):
        if t['username'] == curr_user:
            disp_str = f"{i}. Task: \t\t {t['title']}\n"
            disp_str += f"   Assigned to: \t {t['username']}\n"
            disp_str += f"   Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"   Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"   Task Description: \n {t['description']}\n"
            disp_str += f"   Completed: \t {'Yes' if t['completed'] else 'No'}\n"
            print(disp_str)

    while True:
        try:
            task_choice = int(input("Enter the number of the task to select (or -1 to return to the main menu): "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        if task_choice == -1:
            break
        elif 1 <= task_choice <= len(task_list):
            selected_task = task_list[task_choice - 1]

            if not selected_task['completed']:
                edit_choice = input("Do you want to mark this task as complete (enter 'complete') or edit it (enter 'edit'): ").lower()

                if edit_choice == 'complete':
                    selected_task['completed'] = True
                    print("Task marked as complete.")
                elif edit_choice == 'edit':
                    if input("Do you want to edit the username or due date? Enter 'username' or 'due date': ").lower() == 'username':
                        new_username = input("Enter the new username: ")
                        selected_task['username'] = new_username
                        print("Username updated.")
                    else:
                        while True:
                            try:
                                new_due_date = input("Enter the new due date (YYYY-MM-DD): ")
                                selected_task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                                print("Due date updated.")
                                break
                            except ValueError:
                                print("Invalid datetime format. Please use the format specified.")
                else:
                    print("Invalid choice. Please enter 'complete' or 'edit'.")
            else:
                print("This task is already completed and cannot be edited.")

# Function to generate reports
def generate_reports(task_list, username_password):
    """Function to generate reports."""
    print("Generating Reports:")

    # Task Overview Report
    total_tasks = len(task_list)
    completed_tasks = sum(task['completed'] for task in task_list)
    incomplete_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'].date() < datetime.now().date())

    with open("task_overview.txt", "w") as task_file:
        task_file.write("Task Overview Report\n\n")
        task_file.write(f"Total number of tasks: {total_tasks}\n")
        task_file.write(f"Total number of completed tasks: {completed_tasks}\n")
        task_file.write(f"Total number of uncompleted tasks: {incomplete_tasks}\n")
        task_file.write(f"Total number of overdue tasks: {overdue_tasks}\n")
        task_file.write(f"Percentage of tasks that are incomplete: {incomplete_tasks / total_tasks * 100:.2f}%\n")
        task_file.write(f"Percentage of tasks that are overdue: {overdue_tasks / incomplete_tasks * 100:.2f}%\n")

    # User Overview Report
    total_users = len(username_password)
    user_task_counts = {username: {'total': 0, 'completed': 0, 'incomplete': 0, 'overdue': 0} for username in username_password}

    for task in task_list:
        user_task_counts[task['username']]['total'] += 1
        if task['completed']:
            user_task_counts[task['username']]['completed'] += 1
        elif task['due_date'].date() < datetime.now().date():
            user_task_counts[task['username']]['overdue'] += 1
        else:
            user_task_counts[task['username']]['incomplete'] += 1

    with open("user_overview.txt", "w") as user_file:
        user_file.write("User Overview Report\n\n")
        user_file.write(f"Total number of registered users: {total_users}\n")
        user_file.write(f"Total number of tasks: {total_tasks}\n\n")

        for username, counts in user_task_counts.items():
            user_file.write(f"User: {username}\n")
            user_file.write(f"  Total number of tasks assigned: {counts['total']}\n")
            user_file.write(f"  Percentage of total tasks assigned: {counts['total'] / total_tasks * 100:.2f}%\n")
            user_file.write(f"  Percentage of tasks completed: {counts['completed'] / counts['total'] * 100:.2f}%\n")
            user_file.write(f"  Percentage of tasks to be completed: {counts['incomplete'] / counts['total'] * 100:.2f}%\n")
            user_file.write(f"  Percentage of overdue tasks: {counts['overdue'] / counts['incomplete'] * 100:.2f}%\n\n" if counts['incomplete'] != 0 else "  Percentage of overdue tasks: N/A\n\n")

    print("Reports generated and saved as task_overview.txt and user_overview.txt.")

# Function to display statistics
def display_statistics(task_list, username_password):
    """Function to display statistics."""
    print("Displaying Statistics:")
    
    # Check if task_overview.txt and user_overview.txt files exist
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        print("Reports not found. Generating reports...")
        generate_reports(task_list, username_password)

    # Read and display task overview report
    with open("task_overview.txt", "r") as task_file:
        task_overview_report = task_file.read()
        print("Task Overview Report:")
        print(task_overview_report)

    # Read and display user overview report
    with open("user_overview.txt", "r") as user_file:
        user_overview_report = user_file.read()
        print("\nUser Overview Report:")
        print(user_overview_report)

# Main Code

# Initialize curr_user
curr_user = None

# Check if user.txt file exists
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

# Login Section
logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

# Create the task file if it doesn't exist
task_file_path = "tasks.txt"
if not os.path.exists(task_file_path):
    print("Task file does not exist. Creating a new file...")
    try:
        # Create an empty task file
        with open(task_file_path, "w") as task_file:
            pass  # Do nothing, just create an empty file
    except IOError:
        print("Error: Unable to create task file.")
        # Handle the error appropriately, maybe exit the program or prompt the user to create the file manually

# Read existing task data
try:
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]
except IOError:
    print("Error: Unable to read task file.")
    task_data = []

# Initialize task_list
task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

# Main Menu Loop
while True:
    print()
    menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    gr - Generate reports
    ds - Display statistics
    e - Exit
    : ''').lower()

    if menu == 'r':
        register_user(username_password)

    elif menu == 'a':
        add_task(username_password, task_list)

    elif menu == 'va':
        view_all(task_list)

    elif menu == 'vm':
        view_mine(task_list, curr_user)

    elif menu == 'gr':
        generate_reports(task_list, username_password)

    elif menu == 'ds':
        display_statistics(task_list, username_password)

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")