import json
import os
from datetime import datetime
from colorama import Fore, Style, init
from plyer import notification
init()
tasks = []

def load():
    global tasks
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
    else:
        tasks = []

def save_tasks():
    with open("tasks.json", "w") as file: 
        json.dump(tasks, file, indent= 4)

def add_task():
    course= input("ENTER THE COURSE NAME: ")
    exam = input("ENTER THE NAME OF THE EXAM OR ASSIGNMENT: ")
    while True:

        date = input("ENTER THE DUE DATE (DD-MM-YYYY): ")
        try:
            datetime.strptime(date, "%d-%m-%Y")
            break
        except ValueError:
            print(Fore.RED+"Invalid date format! Enter DD-MM-YYYY"+ Style.RESET_ALL)

    task = {"course": course, "exam": exam, "due_date": date,"completed": False}
    tasks.append(task)
    save_tasks()
    print(Fore.GREEN+ "TASK ADDED SUCCESSFULLY!"+ Style.RESET_ALL)
    input("Press enter to continue--> ")

def viewtasks():
    incomp= [i for i in tasks if not i["completed"]]
    if not incomp:
        print(Fore.RED + "No tasks to show!" + Style.RESET_ALL)
        input("Press enter to continue--> ")
        return
    incomp.sort(key=lambda x: datetime.strptime(x['due_date'], "%d-%m-%Y"))
    print(Fore.CYAN + Style.BRIGHT + "\n📋 INCOMPLETE TASKS\n" + Style.RESET_ALL)
    for i, task in enumerate(incomp, start=1):
        if not task["completed"]:
            print(f"{i}. {Fore.GREEN}{task['exam']}{Style.RESET_ALL} | "f"Course: {task['course']} | "f"Due: {task['due_date']}")

def mark_completed():
    incomplete_tasks = [task for task in tasks if not task["completed"]]
    if not incomplete_tasks:
        print(Fore.RED + "No incomplete tasks to mark!" + Style.RESET_ALL)
        input("Press enter to continue--> ")
        return
    print(Fore.CYAN + Style.BRIGHT + "\n⏳ INCOMPLETE TASKS\n" + Style.RESET_ALL)
    
    for i, task in enumerate(incomplete_tasks, start=1):
        print(f"{i}. {Fore.GREEN}{task['exam']}{Style.RESET_ALL} | "f"Course: {task['course']} | Due: {task['due_date']}")
    choice = input("\nEnter the number of the task you completed: ")
    idx = int(choice) - 1

    completed_task = incomplete_tasks[idx]
    completed_task["completed"] = True

    print(Fore.GREEN + f"✅ '{completed_task['exam']}' marked as completed!" + Style.RESET_ALL)
    save_tasks()
    input("Press enter to continue--> ")

def completed_tasks():
    completed = [task for task in tasks if task["completed"]]
    if not completed:
        print(Fore.RED + "No completed tasks yet!" + Style.RESET_ALL)
        input("Press enter to continue--> ")
        return
    completed.sort(key=lambda x: datetime.strptime(x['due_date'], "%d-%m-%Y"))
    print(Fore.MAGENTA + Style.BRIGHT + "\n📦 COMPLETED TASKS\n" + Style.RESET_ALL)
    for j, task in enumerate(completed, start=1):
        print(f"{j}. {Fore.GREEN}{task['exam']}{Style.RESET_ALL} | "f"Course: {task['course']} | "f"Due: {task['due_date']} ✅")

    input("\nPress Enter to continue-->")
def notifs():
    if not tasks:
        return
    today= datetime.today()
    for i in tasks:
        if i["completed"]:
            due= datetime.strptime(i["due_date"], "%d-%m-%Y")
            remaining = (due-today).days

            if remaining<0:
                notification.notify(title = "🚨 ASSIGNMENT OVERDUE", message = f"{i['exam']} was due on {i['due']}", timeout= 4)
            elif remaining== 0:
                notification.notify(title="⏰ DUE TODAY",message=f"{i['exam']} DUE TODAY! HURRY UP",timeout=4)
            elif remaining <= 4:
                notification.notify(title="📅 DUE SOON",message=f"{i['exam']} due in {remaining} days",timeout=4)
def menu():
    print("**************************")
    print(Fore.BLUE + Style.BRIGHT+ "📚 Assignment PLANNER" + Style.RESET_ALL)
    print("**************************\n")
    print("1. " + Fore.GREEN + "➕ ADD" + Style.RESET_ALL + " assignments / exams")
    print("2. " + Fore.CYAN + "👀 VIEW" + Style.RESET_ALL + " tasks")
    print("3. " + Fore.YELLOW + "✅ COMPLETE" + Style.RESET_ALL + " a task")
    print("4. " + Fore.MAGENTA + "📦 VIEW" + Style.RESET_ALL + " completed tasks")
    print("5. " + Fore.RED + "🚪 EXIT" + Style.RESET_ALL + "\n")

def main():
    load()
    
    while True:
        notifs()
        menu()
        while True:
            try:
                user_input = int(input("Select an option from the menu: "))
                if 1<= user_input<=5:
                    break
                else:
                    print("Invalid choice! Select from 1-5: ")
            except ValueError:
                print(Fore.RED+"Invalid choice! Enter a number from 1-5: "+Style.RESET_ALL)
            
        if user_input == 1:
            add_task()
        elif user_input == 2:
            viewtasks()
        elif user_input == 3: 
            mark_completed()
        elif user_input ==4 :
            completed_tasks()
        elif user_input == 5:
            break
        else:
            print("Invalid choice: ")
if __name__ == "__main__": 
    main()
