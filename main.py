import csv
import os
import sys


class Task:
    def __init__(self, title, priority='Medium', done=False):
        self.title = title
        self.priority = priority
        self.done = done


class TodoList:

    def __init__(self):
        self.file_name = 'todo.csv'
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                reader = csv.reader(file)
                self.tasks = [Task(row[0], row[1], bool(int(row[2]))) for row in reader]

    def save_tasks(self):
        with open(self.file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows([(task.title, task.priority, int(task.done)) for task in self.tasks])

    def create_task(self, title, priority='Medium', done=False):
        self.tasks.append(Task(title, priority, done))
        self.save_tasks()
        print(f'Task "{title}" created successfully.')

    def update_task(self, title, field, edit):
        if field == 'done':
            edit = bool(int(edit))
        for task in self.tasks:
            if task.title == title:
                setattr(task, field, edit)
                self.save_tasks()
                print(f'Task "{title}" updated successfully.')
                break
        else:
            print('Invalid index.')

    def list_tasks(self):
        if not self.tasks:
            print('No tasks found.')
        else:
            print('Task List:')
            print("{:<6} {:<15} {:<10} {:<10}".format('Index', 'Title', 'Priority', 'Done'))
            for index, task in enumerate(self.tasks):
                print("{:<6} {:<15} {:<10} {:<10}".format(index + 1, task.title, task.priority, task.done))

    def delete_task(self, title):
        for task in self.tasks:
            if task.title == title:
                self.tasks.remove(task)
                self.save_tasks()
                print(f'Task "{title}" deleted successfully.')
                break
        else:
            print('Invalid title.')

    def clear_list(self):
        self.tasks = []
        self.save_tasks()
        print('To-do list cleared successfully.')

    def get_task(self, title):
        for task in self.tasks:
            if task.title == title:
                print("{:<15} {:<10} {:<10}".format('Title', 'Priority', 'Done'))
                print("{:<15} {:<10} {:<10}".format(task.title, task.priority, task.done))


def main():
    todo_list = TodoList()

    command = sys.argv
    try:
        if command[1] == 'create':
            todo_list.create_task(command[2], *command[3:])
        elif command[1] == 'update':
            todo_list.update_task(command[2], command[3], command[4])
        elif command[1] == 'delete':
            todo_list.delete_task(command[2])
        elif command[1] == 'list':
            todo_list.list_tasks()
        elif command[1] == 'clear':
            todo_list.clear_list()
        elif command[1] == 'search':
            todo_list.get_task(command[2])
        else:
            print('Invalid command.')
    except IndexError:
        print('Invalid command.')


if __name__ == "__main__":
    main()
