#import os imports the os module and checks if the file is an existing one
import os

#imports the datetime modle and adds timestamps
from datetime import datetime

TODO_FILE = "Your To-Do List.txt"

#Loads tasks from file if it exists and adds/supports timestamps and completion status
def load_tasks():
    tasks = []
    #if the TODO FILE doesnt exists then it returns to the existing/current task list (this prevents it from opning a file that doesnt exist and causing an error!)
    if not os.path.exists(TODO_FILE):
        return tasks
    
    with open(TODO_FILE, "r") as file:
        for line in file.readlines():
            parts = line.strip().split("|")
            if len(parts) == 4:
                task, category, completed_str, timestamp = parts
                completed = True if completed_str == "True" else False
                tasks.append({
                    "task" : task,
                    "category" : category,
                    "completed" : completed,
                    "timestamp" : timestamp
                })
    return tasks

#Saves tasks to a file
def save_tasks(tasks):
    with open(TODO_FILE, "w") as file:
        for t in tasks:
            # store one task per line, fields separated by |
            file.write(f"{t['task']}|{t['category']}|{t['completed']}|{t['timestamp']}\n")

#Color Codes to be used for the project (its all pink sorry. Note that his part is fully customizable to your preferred color scheme!)
Red = '\033[91m'
BabyPink = '\033[38;5;218m'
DarkPink = '\033[38;5;162m'
Pink = '\033[38;5;213m'
Orchid = '\033[38;5;164m'
IndianaPink = '\033[38;5;131m'
RESET = '\033[0m'

#Tasks displayed in a table
def show_tasks(tasks):
    if not tasks:
        print(Red + "You have no tasks to do for the time being!" + RESET)
        return
    
    #Table header
    print(DarkPink + "\n==========")
    print(" YOUR TO-DO LIST")
    print("==========" + RESET)

    #Rows
    print(Pink + f"{'No.':<5}{'Task':<30}{'Category':<12}{'Done':<6}" + RESET)
    print(BabyPink + "-" * 60 + RESET)
    for i, t in enumerate(tasks, 1):
        done_status = "Yes" if t.get("completed") else "No"
        print(f"{DarkPink}{str(i)+ '.':<5}{RESET} {t['task']:<30} {t['category']:<12} {done_status:<6}")
        print(Pink + "." * 60 + RESET)

#Adding a new task with category
def add_task(tasks):
    task_name = input("Input task name: ").strip()
    if not task_name:
        print(Red + "Your Task name cannot be blank!" + RESET)
        return
    category = input("Enter the task category: ").strip() or "other"

    tasks.append({
        "task": task_name,
        "category": category,
        "completed": False,
        "timestamp": str(datetime.now())
    })
    
    print(Orchid + f"Task '{task_name}' added under '{category}'." + RESET)
    
#Edit a task
def edit_task(tasks):
    show_tasks(tasks)

    print("\n ❤️ Please Edit your Task ❤️ ")
    print("You can update the following: Task name, category and or both!")
    print("Note: Leave a field blank if you want to keep it the same.")

    try:
        index = int(input("Enter the number of the task in order to edit it: ")) - 1

        if 0 <= index < len(tasks):
            new_name = input(Pink + "New task name (leave blank if want to keep current): " + RESET).strip()

            print("\n Suggested Categories for you:")
            print("• work\n• self-care\n• errands\n• shopping\n• health\n• appointments")
            new_category = input(Pink + "New category (leave blank if want to keep current): " + RESET).strip()

            # Apply updates only if user typed something
            if new_name:
                tasks[index]["task"] = new_name
            if new_category:
                tasks[index]["category"] = new_category

            print(Orchid + "\n Your Task has been updated successfully! You're doing good!" + RESET)
        else:
            print(Red + "Not a valid task number. Please try again!" + RESET)

    except ValueError:
        print(Red + "Please enter a valid number" + RESET)

#Mark Task as completed
def completed_task(tasks):
    show_tasks(tasks)
    try:
        index = int(input("Enter the number of the task you want to mark as complete: ")) - 1
        if 0 <= index < len(tasks):
            tasks[index]["completed"] = True
            print(Orchid + f"Task '{tasks[index]['task']}' marked as completed! Great job!" + RESET)
        else:
            print(Red + "INVALID task number. Please enter a valid one." + RESET)
    except ValueError:
        print(Red + "Please enter a valid number." + RESET)                 

#Deleting a task or multiple tasks
def delete_task(tasks):
    show_tasks(tasks)
    try:
        indexes_input = input("Enter the task number/s to delete (comma separated): ")
        if not indexes_input.strip():
            print(Red + "No task numbers entered." + RESET)
            return
        indexes = []
        for part in indexes_input.split(","):
            part = part.strip()
            if not part:
                continue
            try:
                idx = int(part) - 1
            except ValueError:
                print(Red + f"Invalid number: {part}" + RESET)
                continue
            if 0 <= idx < len(tasks):
                indexes.append(idx)
            else:
                print(Red + f"Invalid task number: {part}" + RESET)
        # remove duplicates and delete from highest index to lowest so earlier deletions don't shift indices
        indexes = sorted(set(indexes), reverse=True)
        for idx in indexes:
            removed = tasks.pop(idx)
            print(Orchid + f"Removed task: {removed['task']}" + RESET)
    except ValueError:
        print(Red + "Please enter valid number(s)." + RESET)
        
#Search
def search_tasks(tasks):
    term = input("Enter your search term here: ").lower()
    filtered = [t for t in tasks if term in t['task'].lower() or term in t['category'].lower()]
    if not filtered:
        print(Red + "No tasks found matching your search term." + RESET)
    else:
        show_tasks(filtered)    

#Sorting
def sort_tasks(tasks):
    print("\n ❤️ Sorting Options ❤️")
    print("1. Sort by Task Name (A–Z)")
    print("2. Sort by Task Name (Z–A)")
    print("3. Sort by Category (A–Z)")
    print("4. Sort by Completion Status")
    print("5. Sort by Timestamp (Oldest → Newest)")
    print("6. Sort by Timestamp (Newest → Oldest)")

    choice = input("\nChoose sorting option (1-6): ").strip()

    if choice == "1":
        tasks.sort(key=lambda x: x['task'].lower())
        print(Orchid + "Tasks sorted A–Z!" + RESET)

    elif choice == "2":
        tasks.sort(key=lambda x: x['task'].lower(), reverse=True)
        print(Orchid + "Tasks sorted Z–A!" + RESET)

    elif choice == "3":
        tasks.sort(key=lambda x: x['category'].lower())
        print(Orchid + "Tasks sorted by category!" + RESET)

    elif choice == "4":
        tasks.sort(key=lambda x: x['completed'])
        print(Orchid + "Tasks sorted by completion status!" + RESET)

    elif choice == "5":
        tasks.sort(key=lambda x: datetime.fromisoformat(x['timestamp']))
        print(Orchid + "Tasks sorted from oldest to newest!" + RESET)

    elif choice == "6":
        tasks.sort(key=lambda x: datetime.fromisoformat(x['timestamp']), reverse=True)
        print(Orchid + "Tasks sorted from newest to oldest!" + RESET)

    else:
        print(Red + "Invalid choice. Please choose a number between 1 and 6." + RESET)


# Main menu
def main():
    tasks = load_tasks()

    while True:
        print(DarkPink + "\n==========")
        print("   TO-DO MENU")
        print("==========" + RESET)
        print(Pink + "1. View Tasks")
        print("2. Add Task")
        print("3. Edit Task")
        print("4. Mark Task as Completed")
        print("5. Delete Task")
        print("6. Search Tasks")
        print("7. Sort Tasks")
        print("8. Save & Exit" + RESET)

        choice = input("\nSelect an option (1-8): ")

        if choice == "1":
            show_tasks(tasks)

        elif choice == "2":
            add_task(tasks)

        elif choice == "3":
            edit_task(tasks)

        elif choice == "4":
            completed_task(tasks)

        elif choice == "5":
            delete_task(tasks)

        elif choice == "6":
            search_tasks(tasks)

        elif choice == "7":
            sort_tasks(tasks)

        elif choice == "8":
            save_tasks(tasks)
            print(Orchid + "Your tasks have been saved! Goodbye! 💖" + RESET)
            break

        else:
            print(Red + "Invalid choice! Please select between 1–8." + RESET)


# Run program
if __name__ == "__main__":
    main()
    
