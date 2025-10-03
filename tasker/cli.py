import json
import argparse
import textwrap
from datetime import datetime
from tabulate import tabulate


import os

# Get the absolute path of the package directory (where cli.py is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.json")

def file_exists():
    if not os.path.isfile(DB_PATH):
        create_db()
    else:
        pass

def create_db():
    basic_strt = {
        "counter": 0,
        "properties": []
    }
    with open(DB_PATH, "w") as f:
        json.dump(basic_strt, f, indent=2)
        
def load_db():
    with open(DB_PATH) as f:
        return json.load(f)

def dump_db(file_name):
    with open(DB_PATH, "w") as f:
        json.dump(file_name, f, indent=2)

        
def tabular_view(task_id):
    database = load_db()
    for task in database["properties"]:
         if task["ID"] == task_id:
            view_task = [task]
    print(tabulate(view_task, tablefmt="heavy_grid", headers="keys"))

def add(status, args, date, time):
    status = status[0]
    
    database = load_db()
    database["counter"] += 1
    
    data = {
    "ID" : database["counter"],
    "Description" : args.task,
    "Status": status,
    "Created At": f"Date:-{date}, Time:-{time}",
    "Updated At": f"Date:-{date}, Time:-{time}"
    }
    database["properties"].append(data)
    dump_db(database)
    print(tabulate([data], tablefmt="heavy_grid", headers="keys"))

    print(f"Task added successfully! (ID: {data["ID"]})")
    
def update(args, date, time):
    database = load_db()
    for task in database["properties"]:
        if task["ID"] == args.ID:
            task["Description"] = args.updated_task
            task["Updated At"] = f"Date:-{date}, Time:-{time}"
    dump_db(database)
    
    tabular_view(args.ID)
    print("Task updated successfully!")
    
def delete(args):
    database = load_db()
    m = database["properties"]
    for j, task in enumerate(m , start=0):
        if task["ID"] == args.ID:
            del database["properties"][j]
    
    tabular_view(args.ID)
    dump_db(database)
    print(f"Task deleted successfully! (ID: {args.ID})")
    
def mark_in_progress(args):
    database = load_db()
    for task in database["properties"]:
        if task["ID"] == args.ID:
            task["Status"] = "in-progress"
    dump_db(database)
    
    tabular_view(args.ID)
    print("Status changed to 'in-progress' successfully!")
    
def mark_done(args):
    database = load_db()
    for task in database["properties"]:
        if task["ID"] == args.ID:
            task["Status"] = "done"
    dump_db(database)
    
    tabular_view(args.ID)
    print("Status changed to 'done' successfully!")
    
def list_all_tasks():
    database = load_db()
    print(tabulate(database["properties"], tablefmt="heavy_grid", headers="keys" ))
    
def list_done_tasks():
    database = load_db()
    done_tasks = []
    for task in database["properties"]:
        if task["Status"] == "done":
            done_tasks.append(task)
    print(tabulate(done_tasks, tablefmt="heavy_grid", headers="keys"))        

def list_todo_tasks():
    database = load_db()
    todo_tasks = []
    for task in database["properties"]:
        if task["Status"] == "todo":
            todo_tasks.append(task)
    print(tabulate(todo_tasks, tablefmt="heavy_grid", headers="keys"))
    
def list_in_progress_tasks():
    database = load_db()
    in_progress_tasks = []
    for task in database["properties"]:
        if task["Status"] == "in-progress":
            in_progress_tasks.append(task)
    print(tabulate(in_progress_tasks, tablefmt="heavy_grid", headers="keys"))   
      
    
def parsing():
    parser = argparse.ArgumentParser(prog="tasker",
        description=textwrap.dedent("""\
            Task Manager CLI
            -------------------
            A simple yet powerful command-line tool to manage your tasks efficiently.
            
            Features:
              - Add, update, and delete tasks
              - Mark tasks as in-progress or done
              - View tasks with filters (done/todo/in-progress)
              
            Use this CLI to stay organized and boost your productivity.
        """),
        epilog=textwrap.dedent("""\
            Examples:
              ➤ Add a new task:
                tasker add "Buy groceries"
              
              ➤ Update a task:
                tasker update 1 "Buy groceries and cook dinner"
              
              ➤ Delete a task:
                tasker delete 1
              
              ➤ Mark a task as in-progress or done:
                tasker mark-in-progress 2
                tasker mark-done 3
              
              ➤ List tasks:
                tasker list
                tasker list done
                tasker list in-progress
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", title="Available Commands")

    #add 
    add_task = subparsers.add_parser("add", help="Add a new task")
    add_task.add_argument("task", type=str, help="Description of the task to be added")
    
    #update
    update_task = subparsers.add_parser("update", help="Update an existing task")
    update_task.add_argument("ID", type=int, help="ID of the task to update")
    update_task.add_argument("updated_task", help="New description for the task")
    
    #delete
    delete_task = subparsers.add_parser("delete", help="Delete a task")
    delete_task.add_argument("ID", type=int, help="ID of the task to delete")
    
    #marking a task as 'in progress'
    mark_task_in_progress = subparsers.add_parser("mark-in-progress", help="Mark a task as in-progress'")
    mark_task_in_progress.add_argument("ID", type=int, help="ID of the task to mark as in-progress")
    
    #marking a task as 'done'
    mark_task_done = subparsers.add_parser("mark-done", help="Mark a task as done")
    mark_task_done.add_argument("ID", type=int, help="ID of the task to mark as 'done'")
    
    #listing all tasks
    list_all_task = subparsers.add_parser("list", help="List tasks (all or filtered by status)")
    list_all_task.add_argument("status", nargs="?", choices=["done", "todo", "in-progress"], help="Filter tasks by status")
    

    args = parser.parse_args()
    return args
    
           
def main():
    file_exists()
    dt_obj = datetime.now()
    str_dt = datetime.isoformat(dt_obj)
    date, time = str_dt.split("T")
    status = ["todo", "in-progress", "done"]
    args = parsing()
    if args.command == "add":
        add(status, args, date, time)
        
    elif args.command == "update":
        update(args, date, time)
    
    elif args.command == "delete":
        delete(args)
        
    elif args.command == "mark-in-progress":
        mark_in_progress(args)
    
    elif args.command == "mark-done":
        mark_done(args)
    
    elif args.command == "list" and args.status == None:
        list_all_tasks()
    
    elif args.command == "list" and args.status == "done":
        list_done_tasks()
    
    elif args.command == "list" and args.status == "todo":
        list_todo_tasks()
    
    elif args.command == "list" and args.status == "in-progress":
        list_in_progress_tasks()


def run():
    main()
    
    