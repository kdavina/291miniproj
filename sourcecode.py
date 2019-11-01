import sqlite3
import getpass
import re

def main():
    global conn, c 
    # path = sysargv[1] 
    # conn = sqlite3.connect(path)
    conn = sqlite3.connect('./database_test.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON; ')
    conn.commit()

    # LOGIN SCREEN
    print("Login Here!")
    username = input("Enter username: ")
    password = input("Enter Password: ")
    
    # re.match is checking if our username and password contains alphabet, numbers and underscores ONLY
    if re.match("^[A-Za-z0-9_]*$", username) and re.match("^[A-Za-z0-9_]*$", password):
        c.execute('SELECT uid FROM users WHERE uid=? and pwd=?;', (username, password)) == None
            
        
    else:
        print("login failed")
    
        
    
if __name__ == "__main__":
    main()