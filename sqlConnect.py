import mysql.connector
from sshtunnel import SSHTunnelForwarder


sql_hostname = '127.0.0.1'
sql_username = 'testU'
sql_password = 'passwordQ123.'
sql_main_database = 'testDB'
sql_port = 3306
ssh_host = 'sql.podor.ca'
ssh_user = 'root'
ssh_passwd = '3-qJ{ov_LH324aww'
ssh_port = 22
sql_ip = '1.1.1.1.1'

with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_password=ssh_passwd,
        remote_bind_address=(sql_hostname, sql_port)) as tunnel:
    conn = mysql.connector.connect(host='127.0.0.1', user=sql_username,
            passwd=sql_password, db=sql_main_database,
            port=tunnel.local_bind_port)

    mycursor = conn.cursor()


    sql_command = """CREATE TABLE emp2 (
    staff_number INTEGER PRIMARY KEY,
    fname VARCHAR(20),
    lname VARCHAR(30),
    gender CHAR(1),
    joining DATE);"""


    mycursor.execute(sql_command)
    sql_command = """INSERT INTO emp VALUES (23, "Rishabh", "Bansal", "M", "2014-03-28");"""
    mycursor.execute(sql_command)

    sql_command = """INSERT INTO emp VALUES (1, "Bill", "Gates", "M", "1980-10-28");"""
    mycursor.execute(sql_command)

    conn.commit()

    print(mycursor.rowcount, "record inserted.")

    conn.close()
