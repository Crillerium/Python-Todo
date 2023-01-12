import sqlite3
from datetime import datetime, timedelta
import argparse
import sys
try:
    import prettytable
except:
    print('请先安装 prettytable 库!')
    sys.exit()

# Connect to SQLite database
conn = sqlite3.connect(sys.argv[0].replace('plan.py','plan.db'))
cursor = conn.cursor()

# Create argparse object
parser = argparse.ArgumentParser(description="A command line dateplanner")

# Add arguments
parser.add_argument('-a', '--add', dest='plan', help='Add new plan')
parser.add_argument('-t', '--time', dest='due_date', help='Due date of plan')
parser.add_argument('-l', '--list', action='store_true', help='List all plans')
parser.add_argument('-d', '--delete', dest='plan_id', type=int, help='Delete a plan')
parser.add_argument("-u", "--update", help="Id of the plan you want to modify", type=int)
parser.add_argument("-p", "--newplan", help="New plan", type=str)
parser.add_argument('--id', '-i', nargs=2, help='change a task id')

# Parse arguments
args = parser.parse_args()

# Add plan
if args.plan and args.due_date:
        due_date = args.due_date
        if len(due_date.split("-"))==1:
            due_date = datetime.now().strftime("%Y-%m-") + due_date
        elif len(due_date.split("-"))==2:
            due_date = datetime.now().strftime("%Y-") + due_date
        cursor.execute("INSERT INTO plans (plan, duedate) VALUES (?, ?)", (args.plan, due_date))
        conn.commit()
        print("Plan added successfully!")

# List plans
elif args.list:
    cursor.execute("SELECT * FROM plans")
    all_rows = cursor.fetchall()
    if len(all_rows)>0:
        table = prettytable.PrettyTable()
        table.field_names = ["ID", "Plan", "Due Date", "Days Left"]
        table.hrules = prettytable.ALL
        for row in all_rows:
            id, plan, duedate = row
            due_date = datetime.strptime(duedate, "%Y-%m-%d").date()
            days_left = (due_date - datetime.now().date()).days + 1
            if days_left < 1:
                cursor.execute("DELETE FROM plans WHERE id=?", (id,))
                conn.commit()
            else:
                table.add_row([id, plan, duedate, days_left])
        print(table)
    else:
        print("No plans found.")

# Delete plan
elif args.plan_id:
    cursor.execute("DELETE FROM plans WHERE id = ?", (args.plan_id,))
    conn.commit()
    print("Plan deleted successfully!")

elif args.update and (args.newplan or args.due_date):
    if args.newplan:
        cursor.execute("UPDATE plans SET plan = ? WHERE id = ?", (args.newplan, args.update))
    if args.due_date:
        due_date = args.due_date
        if len(due_date.split("-"))==1:
            due_date = datetime.now().strftime("%Y-%m-") + due_date
        elif len(due_date.split("-"))==2:
            due_date = datetime.now().strftime("%Y-") + due_date
        cursor.execute("UPDATE plans SET duedate = ? WHERE id = ?", (due_date, args.update))
    conn.commit()
    print("Plan modified successfully!")

elif args.id:
    cursor.execute("UPDATE plans SET id = ? WHERE id = ?", (args.id[1], args.id[0]))
    conn.commit()
    print(f"Plan ID {args.id[0]} has been updated!")

# Close database connection
conn.close()