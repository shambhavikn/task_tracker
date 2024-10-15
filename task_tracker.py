#!/usr/bin/env python3

import sys
import json
import os
from datetime import datetime
import argparse


def load_tasks():
    if not os.path.exists('tasks.json'):
        return []
    try:
        with open('tasks.json','r') as file:
            content=file.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        print("Error: 'tasks.json' contains invalid JSON")
        return []
    
def save_tasks(tasks):
    with open('tasks.json','w') as file:
        json.dump(tasks,file,indent=4)


def main():
    parser=argparse.ArgumentParser(description='Task Tracker CLI')
    subparsers=parser.add_subparsers(dest='command',help='Available commands')
    parser_add=subparsers.add_parser('add',help='Add a new task')
    parser_add.add_argument('-description',type=str,help='Description of the task')

    parser_list=subparsers.add_parser('list',help='list all tasks')

    parser_update=subparsers.add_parser('update')
    parser_update.add_argument('-n',type=int,help='An integer argument')
    parser_update.add_argument('-s',type=str,help='A string argument')
    
    parser_delete=subparsers.add_parser('delete')
    parser_delete.add_argument('-n',type=int,help='An integer argument')
    
    parser_mark_in_progress=subparsers.add_parser('mark-in-progress')
    parser_mark_in_progress.add_argument('-n',type=int)

    parser_mark_done=subparsers.add_parser('mark-done')
    parser_mark_done.add_argument('-n',type=int)

    args=parser.parse_args()

    print(sys.argv[0],len(sys.argv))
    if len(sys.argv)<2:
        #print("Usage: task-cli <command> [options]")
        return
    
    command=sys.argv[1]

    if args.command=='add':
        add_task(args.description)
    elif args.command=="list":
        list_tasks()
    elif args.command=="update":
        update_task(args.n,args.s)
    elif args.command=='delete':
        delete_task(args.n)
    elif args.command=='mark-in-progress':
        mark_in_progress(args.n)
    elif args.command=='mark-done':
        mark_done(args.n)
    else:
        print("Unknown command")


def add_task(description):
    tasks=load_tasks()

    if tasks:
        new_id=max(task['id'] for task in tasks)+1
    else:
        new_id=1

    current_time=datetime.now().isoformat()

    new_task={
        'id':new_id,
        'description':description,
        'status':'todo', #default is todo,
        'createdAt':current_time,
        'updatedAt':current_time
    }

    tasks.append(new_task)

    save_tasks(tasks)

    print(f"Task added successfully (ID: {new_id})")

def list_tasks():
    tasks=load_tasks()

    if not tasks:
        print('No tasks found')
        return
    
    for task in tasks:
        print(f"ID: {task['id']}")
        print(f"Description: {task['description']}")
        print(f"Status: {task['status']}")
        print(f"Created At: {task['createdAt']}")
        print(f"Updated At: {task['updatedAt']}")
        print("-"*30)

def update_task(id,description):
    tasks=load_tasks()

    task_found=False
    for task in tasks:
        if task['id']==id:
            task['description']=description
            task['updatedAt']=datetime.now().isoformat()
            task_found=True
            break

    if task_found:
        save_tasks(tasks)
        print(f"Updated task Id: {id}")
    else:
        print(f"Tasks with ID {id} not found")

def delete_task(id):
    tasks=load_tasks()

    task_found=False
    for task in tasks:
        if task['id']==id:
            tasks.remove(task)
            task_found=True
            break

    if task_found:
        save_tasks(tasks)
        print(f"Deleted task Id: {id}")
    else:
        print(f"Task with ID: {id} not found")  

def mark_in_progress(id):
    tasks=load_tasks()

    task_found=False
    for task in tasks:
        if task['id']==id:
            task['status']='in-progress'
            task['updatedAt']=datetime.now().isoformat()
            task_found=True
            break

    if task_found:
        save_tasks(tasks)
        print(f"Task ID {id} marked as 'in-progress'.")
    else:
        print(f"Task with ID {id} not found")

def mark_done(id):
    tasks=load_tasks()

    task_found=False
    for task in tasks:
        if task['id']==id:
            task['status']='done'
            task['updatedAt']=datetime.now().isoformat()
            task_found=True
            break

    if task_found:
        save_tasks(tasks)
        print(f"Task ID {id} marked as done")
    else:
        print(f"Task with ID {id} not found")

if __name__=='__main__':
    main()