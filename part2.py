# these should be the only imports you need
import sys
import sqlite3

# write your code here
#grab args
arg = sys.argv[1]
if len(sys.argv) > 2:
    arg2 = sys.argv[2]
else:
    arg2 = "N/A"
# usage should be
#  python3 part2.py customers
if arg == "customers":
    connection = sqlite3.connect('Northwind_small.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT Id, CompanyName FROM Customer")
    print("ID        Customer Name")
    for i,n in cursor.fetchall():
        print(i + "     " + n)
    cursor.close()
    connection.close()
#  python3 part2.py employees
if arg == "employees":
    connection = sqlite3.connect('Northwind_small.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT Id, FirstName, LastName FROM Employee")
    print("ID    Employee Name")
    for x,y,z in cursor.fetchall():
        print(str(x) + "     " + y + " " + z)
    cursor.close()
    connection.close()
#  python3 part2.py orders cust=<customer id>
if arg == "orders" and arg2[0:5] == "cust=":
    cust_id = arg2[5:]
    connection = sqlite3.connect('Northwind_small.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT OrderDate from 'Order' WHERE CustomerId = ?", [cust_id])
    print("Order dates")
    for x in cursor.fetchall():
        print(x[0])
#  python3 part2.py orders emp=<employee last name>
if arg == "orders" and arg2[0:4] == "emp=":
    last_name = arg2[4:]
    connection = sqlite3.connect('Northwind_small.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT OrderDate from 'Order' WHERE EmployeeID = (SELECT Id from Employee WHERE LastName = ?)", [last_name])
    print("Order dates")
    for x in cursor.fetchall():
        print(x[0])
    cursor.close()
    connection.close()
