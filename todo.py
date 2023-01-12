import sqlite3
import argparse
import sys

def create_todo(task):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("INSERT INTO todos (task) VALUES (?)", (task,))
    conn.commit()
    last_row_id = c.lastrowid
    print(f"Task '{task}' has been added to the list!, the ID is {last_row_id}")
    conn.close()

def update_todo(task_id, task):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("UPDATE todos SET task = ? WHERE id = ?", (task, task_id))
    conn.commit()
    print(f"Task with ID {task_id} has been updated!")
    conn.close()

def delete_todo(task_id):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("DELETE FROM todos WHERE id = ?", (task_id,))
    conn.commit()
    print(f"Task with ID {task_id} has been deleted!")
    conn.close()

def list_todos():
    try:
        import prettytable
    except:
        print('请先安装 prettytable 库!')
        import sys
        sys.exit()
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("SELECT * FROM todos")
    todos = c.fetchall()
    x = prettytable.PrettyTable()
    x.field_names = ["ID", "Task"]
    x.hrules = prettytable.ALL
    for todo in todos:
        x.add_row(todo)
    print(x)
    conn.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', '-l', action='store_true', help='list all tasks')
    parser.add_argument('--add', '-a', help='add a task')
    parser.add_argument('--update', '-u', nargs=2, help='update a task')
    parser.add_argument('--delete', '-d', type=int, help='delete a task')
    args = parser.parse_args()

    if args.list:
        list_todos()
    elif args.add:
        create_todo(args.add)
    elif args.update:
        update_todo(args.update[0], args.update[1])
    elif args.delete:
        delete_todo(args.delete)

if __name__ == '__main__':
    path = sys.argv[0].replace('todo.py','todo.db')
    main()