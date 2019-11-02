import sqlite3
import getpass
import re
import datetime
def main():
    global conn, c 
    # path = sysargv[1] 
    # conn = sqlite3.connect(path)
    conn = sqlite3.connect('./database_test.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON; ')
    conn.commit()
    login_screen = False

    # LOGIN SCREEN
    """
    while login_screen == False:
        login_screen = login()
    """
        
    #USER MENU
    print("To register a birth, type in 1")
    print("To register a marriage, type in 2")
    print("To renew a vehicle registration, type in 3")
    print("To process a bill of sale, type in 4")
    print("To process a payment, type in 5")
    print("To get a driver abstract,type in 6")
    print("To issue a ticket, type in 7")
    print("To find a car owner, type in 8")
    action = input("Choose a task: ")
    
    if int(action) == 1: one()
    elif int(action) == 2: two()
    elif int(action) == 3: three()
    elif int(action) == 4: four()
    elif int(action) == 5: five()
    elif int(action) == 6: six()
    elif int(action) == 7: seven()
    elif int(action) == 8: eight()
    
        

def login():
    print("Login Here!")
    username = input("Enter username: ")
    password = getpass.getpass("Enter Password: ")
    
    # re.match is checking if our username and password contains alphabet, numbers and underscores ONLY
    if re.match("^[A-Za-z0-9_]*$", username) and re.match("^[A-Za-z0-9_]*$", password):
        c.execute('SELECT uid FROM users WHERE uid=? and pwd=?;', (username, password))
        if c.fetchone() != None:
            print("Login Success.")
            return True
        else:
            print("Login failed. Try again")
            return False
    else:
        print("Login failed. Try again")
        return False
    
def one():
    print("You have chosen to register a birth")
    """
    while True:
        fname = input("Please provide a first name: ")
        if fname != '' and fname.isalpha() == True:
            break
        else:
            print("Incorrect format")
    
    while True:
        lname = input("Please provide a last name: ")
        if lname != '' and lname.isalpha() == True:
            break 
        else:
            print("Incorrect format")
            
    while True:
        gender = input("Please provide the gender (M/F): ")
        if gender.upper() == 'F' or gender.upper() == 'M':
            break
      
    while True:
        bdate = input("Please provide a birth date (YYYY-MM-DD): ")
        try:
            year, month, day = bdate.split('-')
            datetime.datetime(int(year),int(month),int(day))
            break
        except ValueError:
            print("Invalid Date")
    
    
    
    while True:
        bplace = input("Please provide a birth place: ")
        if bplace != '' and bplace.isalpha():
            break      
    """    
    while True:
        mot_fname = input("Please provide mother's first name: ")
        if mot_fname != '' and mot_fname.isalpha():
            break  
        
    while True:
        mot_lname = input("Please provide mother's last name: ")
        if mot_lname != '' and mot_lname.isalpha():
            break     
    """   
    while True:
        fat_fname = input("Please provide father's first name: ")
        if fat_fname != '' and fat_lname.isalpha():
            break     
        
    while True:
        fat_lname = input("Please provide father's last name: ")
        if fat_lname != '' and fat_lname.isalpha():
            break  
    """
    if find_parent(mot_fname, mot_lname) == None:
        missing_parent_info(mot_fname, mot_lname)
        
    elif find_parent(fat_fname, fat_lname) == None:
        missing_parent_info(fat_fname, fat_lname)
    
        
        
def find_parent(fname, lname):
    c.execute('SELECT fname, lname FROM persons WHERE fname =? and lname=?;', (fname, lname))
    return c.fetchone()

# we need first name, last name, birth date, birth place, address and phone. for each parent any column other than first and last can be null
def missing_parent_info(fname, lname):
    print("There seems to be no record of {} {} in our database".format(fname,lname))
    print("Please fill out the information down below. \nHit enter if you do not want to fill this out.")  
    while True:
        bdate = input("Please provide a birth date (YYYY-MM-DD): ")
        if bdate == '':
            bdate =  'NULL'
            break
        else:
            try:
                year, month, day = bdate.split('-')
                datetime.datetime(int(year),int(month),int(day))
                break
            except ValueError:
                print("Invalid Date")
    
    while True:
        bplace = input("Please provide a birth place: ")
        if bplace == '':
            bplace = 'NULL'
            break
        else:
            if bplace.isalpha():
                break      
            else:
                print("Invalid input")
                
    while True:
        address = input("Please provide an address: ")
        if address == '':
            address = 'NULL'
            break
        else:
            if address.isalpha() and len(address) < 30:
                break      
            else:
                print("Invalid input")        
                
    while True:
        phone_number = input("Please provide a phone number (123-456-7890): ")
        if phone_number == '':
            phone_number = 'NULL'
            break
        else:
            if phone_number.isalpha() and len(phone_number) < 12:
                break      
            else:
                print("Invalid input")         
    parent_register = 'INSERT INTO persons(fname, lname, bdate, bplace, address, phone) VALUES (?,?,?,?,?,?)'
    c.execute(''' INSERT INTO persons(fname, lname, bdate, bplace, address, phone)
                  VALUES
                  (?,?,?,?,?,?)''', (fname, lname, bdate, bplace, address, phone_number))
    conn.commit()
       

    
    
def two():
    pass
def three():
    pass
def four():
    pass
def five():
    pass
def six():
    pass
def seven():
    pass
def eight():
    pass

if __name__ == "__main__":
    main()