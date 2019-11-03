import sqlite3
import getpass
import re
import datetime
import random

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
    
    while login_screen == False:
        login_screen, username = login()
        
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
    
    if int(action) == 1: one(username)
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
            return True, username
        else:
            print("Login failed. Try again")
            return False, username
    else:
        print("Login failed. Try again")
        return False, username
    
def one(user):
    print("You have chosen to register a birth")
    while True:
        fname = input("Please provide a first name: ")
        if fname != '' and fname.isalpha() == True and len(fname) <= 12:
            break
        else:
            print("Incorrect format")
    
    while True:
        lname = input("Please provide a last name: ")
        if lname != '' and lname.isalpha() == True and len(lname) <= 12 :
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
            if len(month) == 1:
                month = "0" + month
            break
        except ValueError:
            print("Invalid Date")
    
    
    
    while True:
        bplace = input("Please provide a birth place: ")
        if bplace != '' and bplace.isalpha():
            break      
       
    while True:
        mot_fname = input("Please provide mother's first name: ")
        if mot_fname != '' and mot_fname.isalpha():
            break  
        
    while True:
        mot_lname = input("Please provide mother's last name: ")
        if mot_lname != '' and mot_lname.isalpha():
            break     
    
    while True:
        fat_fname = input("Please provide father's first name: ")
        if fat_fname != '' and fat_fname.isalpha():
            break     
        
    while True:
        fat_lname = input("Please provide father's last name: ")
        if fat_lname != '' and fat_lname.isalpha():
            break  
    
    if find_parent(mot_fname, mot_lname) == None:
        missing_parent_info(mot_fname, mot_lname)
    
    if find_parent(fat_fname, fat_lname) == None:
        missing_parent_info(fat_fname, fat_lname)
     
    # REGISTER A PERSON FIRST
    # We need to grab address and phone number from mom
    # note that address and phone number is in an indexed list called result
    c.execute('SELECT address, phone FROM persons where fname = ? and lname = ?;', (mot_fname, mot_lname))
    result = c.fetchone()
    c.execute(''' INSERT INTO persons(fname, lname, bdate, bplace, address, phone)
                  VALUES
                  (?,?,?,?,?,?)''', (fname, lname, bdate, bplace, result[0], result[1]))
    conn.commit()
     
    
    # register the kid with all this info
    
    # fname, lname, gender, birth date, birth place, first name of parents, registration date, registration place,unique registration number
    # THIS IS FOR BIRTHS
    # use datetime function for registration date and use a query to find the regplace
    regdate = datetime.date.today()
    c.execute('SELECT city FROM users where uid = ?;', (user,))
    regplace = c.fetchone()[0]
    
    # grabbing a random and unique registration
    while True:
        reg_num = random.randint(1,99999999)
        reg_num = str(reg_num)
        c.execute('SELECT regno FROM births WHERE regno = ?;', (reg_num,))
        try:
            c.fetchone()[0]
        except TypeError:
            break
    
    c.execute(''' INSERT INTO births(regno, fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname)
                  VALUES (?,?,?,?,?,?,?,?,?,?)''', 
                (reg_num, fname, lname, regdate, regplace, gender,fat_fname, fat_lname, mot_fname, mot_lname))
    conn.commit()
    
        
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
    # Enter a first name and a last name to get a driver abstract
    # Driver abstract contains number of tickets, number of demerit notices, total number of demerit points received both within the past 2 years and within the lifetime. 
    # Given the option to see the tickets ordered from the latest to the oldest. 
    # For each ticket, you will report the ticket number, the violation date, the violation description, the fine, the registration number and the make and model of the car for which the ticket is issued. 
    # If there are more than 5 tickets, at most 5 tickets will be shown at a time, and the user can select to see more.
    f_name = input("Enter first name: ")
    l_name = input("Enter last name: ")
    
    
def seven():
    pass
def eight():
    pass

if __name__ == "__main__":
    main()