import unittest
import subprocess
import os


class TestTodoListTerminal(unittest.TestCase):

    def setUp(self):
        self.todo_list_executable = 'python3 main.py'
        self.solution_executable = 'python3 solution.py'
        self.filename = 'todo.csv'
        self.addCleanup(self.cleanup)

        with open('../main.py', 'rb') as a:
            data = a.read()
            with open('main.py', 'wb') as b:
                b.write(data)

    def cleanup(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def run_command(self, executable, command):
        return subprocess.run(f'{executable} {command}', shell=True, capture_output=True, text=True)

    def test_create_task(self):
        result = self.run_command(self.todo_list_executable, 'create "Test Task 1"')
        self.assertEqual('Task "Test Task 1" created successfully.', result.stdout.strip())
        with open('todo.csv', 'r') as file:
            self.assertEqual(file.readlines()[0].strip(), 'Test Task 1,Medium,0')

        result = self.run_command(self.todo_list_executable, 'create "Test Task 2" Low 1')
        self.assertEqual('Task "Test Task 2" created successfully.', result.stdout.strip())
        with open('todo.csv', 'r') as file:
            self.assertEqual(file.readlines()[1].strip(), 'Test Task 2,Low,1')

    def test_update_task(self):
        self.run_command(self.todo_list_executable, 'create "Test Task"')
        result = self.run_command(self.todo_list_executable, 'update "Test Task" done 1')
        self.assertEqual('Task "Test Task" updated successfully.', result.stdout.strip())
        with open('todo.csv', 'r') as file:
            self.assertEqual(file.readlines()[0].strip(), 'Test Task,Medium,1')

    def test_list_tasks(self):
        result = self.run_command(self.todo_list_executable, 'list')
        self.assertEqual('No tasks found.', result.stdout.strip())

        self.run_command(self.todo_list_executable, 'create "Test Task 1"')
        self.run_command(self.todo_list_executable, 'create "Test Task 2"')
        self.run_command(self.todo_list_executable, 'create "Test Task 3" High 1')
        self.run_command(self.todo_list_executable, 'update "Test Task 1" priority Low')

        result = self.run_command(self.todo_list_executable, 'list')
        expected_output = '''Task List:
Index  Title           Priority   Done      
1      Test Task 1     Low        0         
2      Test Task 2     Medium     0         
3      Test Task 3     High       1'''
        self.assertEqual(expected_output, result.stdout.strip())

    def test_delete_task(self):
        self.run_command(self.todo_list_executable, 'create "Test Task 1"')
        self.run_command(self.todo_list_executable, 'create "Test Task 2"')

        result = self.run_command(self.todo_list_executable, 'delete "Test Task 1"')
        self.assertEqual('Task "Test Task 1" deleted successfully.', result.stdout.strip())
        with open('todo.csv', 'r') as file:
            self.assertEqual(file.readlines()[0].strip(), 'Test Task 2,Medium,0')

        result = self.run_command(self.todo_list_executable, 'delete "Test Task 1"')
        self.assertEqual('Invalid title.', result.stdout.strip())
        with open('todo.csv', 'r') as file:
            self.assertEqual(file.readlines()[0].strip(), 'Test Task 2,Medium,0')

    def test_clear_list(self):
        self.run_command(self.todo_list_executable, 'create "Test Task 1"')
        self.run_command(self.todo_list_executable, 'create "Test Task 2"')

        result = self.run_command(self.todo_list_executable, 'clear')
        self.assertEqual('To-do list cleared successfully.', result.stdout.strip())
        with open('todo.csv', 'r') as file:
            self.assertEqual(file.read().strip(), '')


if __name__ == '__main__':
    unittest.main()
