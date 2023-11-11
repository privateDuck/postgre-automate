from psycopg2 import *


def find_in_file(lines, str):
    for line in lines:
        if line.find(str) > -1:
            line = line.replace('\n', '').replace(' ', '').split(':')
            appnd = line[1].split('#')[0]
            return appnd


file = open("data.txt", 'r')
total_lines = file.readlines()
file.close()

# login data for the database session
host = find_in_file(total_lines, "host")
port = find_in_file(total_lines, "port")
user = find_in_file(total_lines, "user")
password = find_in_file(total_lines, "password")

# database to connect to
database = find_in_file(total_lines, "database")
# name of the table
table = find_in_file(total_lines, "table")

conn = connect(host=host, port=port, user=user, password=password, database=database)
curs = conn.cursor()

curs.execute(format(
    "select column_name from information_schema.columns where table_schema = 'public' and table_name = '%s';" % table))

tuples = []
fetched_col = curs.fetchall()
table_cols = []

for i in range(len(fetched_col)):
    table_cols.append((fetched_col[i][0]))

n_val = len(find_in_file(total_lines, table_cols[0].__str__()).split(','))
n_col = len(table_cols)

for i in range(n_val):
    tuple = []
    for col in table_cols:
        data = find_in_file(total_lines, col.__str__()).split(',')
        tuple.append(data[i])
    tuples.append(tuple)

print("tuples: ", tuples)
print("")

for j in range(n_val):
    exec_str = format("INSERT INTO %s VALUES(" % table)
    for i in range(n_col):
        exec_str += tuples[j][i].__str__()
        if i < n_col - 1:
            exec_str += ','
        else:
            exec_str += ')'
    print(exec_str)
    try:
        curs.execute(exec_str)
    except:
        conn.commit()
        print("error")

conn.commit()
curs.execute(format("select * from %s" % table))
fetch = curs.fetchall()
conn.close()

print("\nTable: %s" % table)
for row in fetch:
    print(row)

