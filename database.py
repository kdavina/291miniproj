import sqlite3
import time

conn = None
c = None

def connect(path):
    global conn, c

    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(' PRAGMA foreign_keys=ON;')
    conn.commit()
    return


def drop_tables():
   
    c.executescript('''
        drop table if exists demeritNotices;
        drop table if exists tickets;
        drop table if exists registrations;
        drop table if exists vehicles;
        drop table if exists marriages;
        drop table if exists births;
        drop table if exists payments;
        drop table if exists users;
        drop table if exists persons;
    ''')
    conn.commit()


def define_tables():
    c.executescript('''
        create table persons (
          fname		char(12),
          lname		char(12),
          bdate		date,
          bplace	char(20), 
          address	char(30),
          phone		char(12),
          primary key (fname, lname)
        );
        create table births (
          regno		int,
          fname		char(12),
          lname		char(12),
          regdate	date,
          regplace	char(20),
          gender	char(1),
          f_fname	char(12),
          f_lname	char(12),
          m_fname	char(12),
          m_lname	char(12),
          primary key (regno),
          foreign key (fname,lname) references persons,
          foreign key (f_fname,f_lname) references persons,
          foreign key (m_fname,m_lname) references persons
        );
        create table marriages (
          regno		int,
          regdate	date,
          regplace	char(20),
          p1_fname	char(12),
          p1_lname	char(12),
          p2_fname	char(12),
          p2_lname	char(12),
          primary key (regno),
          foreign key (p1_fname,p1_lname) references persons,
          foreign key (p2_fname,p2_lname) references persons
        );
        create table vehicles (
          vin		char(5),
          make		char(10),
          model		char(10),
          year		int,
          color		char(10),
          primary key (vin)
        );
        create table registrations (
          regno		int,
          regdate	date,
          expiry	date,
          plate		char(7),
          vin		char(5), 
          fname		char(12),
          lname		char(12),
          primary key (regno),
          foreign key (vin) references vehicles,
          foreign key (fname,lname) references persons
        );
        create table tickets (
          tno		int,
          regno		int,
          fine		int,
          violation	text,
          vdate		date,
          primary key (tno),
          foreign key (regno) references registrations
        );
        create table demeritNotices (
          ddate		date, 
          fname		char(12), 
          lname		char(12), 
          points	int, 
          desc		text,
          primary key (ddate,fname,lname),
          foreign key (fname,lname) references persons
        );
        create table payments (
          tno		int,
          pdate		date,
          amount	int,
          primary key (tno, pdate),
          foreign key (tno) references tickets
        );
        create table users (
            uid		char(8),
            pwd		char(8),
            utype	char(1),	
            fname	char(12),
            lname	char(12), 
            city	char(15),
            primary key(uid),
            foreign key (fname,lname) references persons
          );
  
       
        ''')

    conn.commit()

    return


def insert_data():
    global conn, c
    persons_sql = "INSERT INTO persons(fname, lname, bdate, bplace, address, phone) VALUES (?,?,?,?,?,?)"
    persons_values = [('Amanda', 'Nguyen', '1999-01-28', 'Edmonton', '16115 - 140 Street', '780 902 9107'), ('hai', 'nguyen', 'NULL', 'NULL', 'NULL','NULL'),('thuy', 'tran', 'NULL', 'NULL', 'NULL','NULL'),('Jim','Halpert','1950-01-01','Scranton','IDK', '123-456-7890'),('pam','halpert','1111-01-01','Scranton','NULL','123-456-7890'), ('Officer','Poopy','2010-05-04','Calgary','Happy Lane','123-456-7889'), ('miley', 'cyrus', 'NULL', 'NULL', 'NULL','NULL')]
    users_sql = "INSERT INTO users(uid, pwd, utype, fname, lname, city) VALUES (?, ?, ?, ?, ?, ?)"
    users_values = [('amanda6', 'password', 'a', 'Amanda', 'Nguyen', 'Edmonton'), ('officeruid', 'poopy', 'o', 'Officer', 'Poopy', 'Calgary')] 
    
    marriages_sql ="INSERT INTO marriages(regno,regdate,regplace,p1_fname,p1_lname,p2_fname,p2_lname) VALUES (?,?,?,?,?,?,?)"
    marriages_values = [(1,'1111-11-11', 'edmonton', 'Jim', 'Halpert','pam','halpert')]

    vehicles_sql = "INSERT INTO vehicles(vin,make,model,year,color) VALUES (?, ?, ?, ?, ?)"
    vehicles_values = [('U200', 'Chevrolet', 'Camaro', 1969, 'red'),('U300', 'Mercedes', 'SL 230', 1964, 'black'),('U400', 'Mercedes', 'SL 240', 1985, 'blue'), ('U500', 'Mercedes', 'MP 350', 2000, 'green'), ('U600', 'Mercedes', 'TY 678', 1999, 'black'), ('U700', 'Mercedes', 'HW 012', 2005, 'gold')]
    births_sql = 'INSERT INTO births(regno, fname, lname,regdate,regplace,gender,f_fname, f_lname, m_fname, m_lname) VALUES (?,?,?,?,?,?,?,?,?,?);'
    births_values = [(1,'miley','cyrus','1111-11-11','edmonton','m','hai','nguyen','thuy','tran')]
    registration_sql = "INSERT INTO registrations(regno, regdate, expiry, plate, vin, fname, lname) VALUES (?, ?, ?, ?, ?, ?, ?)"
    registration_values = [(300, '1964-05-26','1965-05-25', 'DISNEY','U200', 'Amanda', 'Nguyen'),(400, '2014-02-21', '2015-02-20', 'WREKT', 'U300', 'Amanda', 'Nguyen')]
    registration_values2 = [(500,'2020-01-01','2021-01-01','WREKT','U300','Jim','Halpert'),(600, '2030-05-23', '2031-05-23', 'BALLIN', 'U400', 'Jim', 'Halpert'), (700, '2010-03-04','1965-05-25', 'DISNEY','U500', 'pam', 'halpert'), (800, '2000-09-03','1965-05-25', 'DISNEY','U600', 'pam', 'halpert'), (900, '2019-08-12','1965-05-25', 'DISNEY','U700', 'miley', 'cyrus'), (1000, '2015-06-21','1965-05-25', 'DISNEY','U500', 'Amanda', 'Nguyen')]
    tickets_sql = "INSERT INTO tickets(tno,regno,fine,violation,vdate) VALUES (?, ?, ?, ?, ?)"
    tickets_values = [(400,300,4,'speeding','1964-08-20')]
    tickets_values2 = [(500, 400, 5, 'skidooshing', '2025-09-01')]
    tickets_values3 = [(600, 400, 2, 'crying', '2025-10-10')]
    tickets_values4 = [(700, 400, 2, 'cancelled', '2029-12-12')]
    tickets_values5 = [(800, 300, 1, 'flaking', '2030-01-01')]
    tickets_values6 = [(900, 300, 6, 'imtired', '2031-08-07')]
    demerits_sql = "INSERT INTO demeritNotices(ddate, fname, lname, points, desc) VALUES (?, ?, ?, ?, ?)"
    demerits_values = [('2018-07-20', 'Amanda', 'Nguyen', 4, 'Speeding')]
    demerits_values2 = [('2019-03-20', 'Amanda', 'Nguyen', 12, 'Driving armor vehicles')]
    demerits_values3 = [('2000-03-30', 'Amanda', 'Nguyen', 4, 'Speeding')]
    demerits_values4 = [('2001-03-29', 'Amanda', 'Nguyen', 2, 'Red light')]
    demerits_values5 = [('2016-02-20', 'Amanda', 'Nguyen', 2, 'Speeding')]
    demerits_values5 = [('2010-10-31', 'Amanda', 'Nguyen', 8, 'Drunk driving')]
    demerits_values6 = [('2019-09-28', 'Amanda', 'Nguyen', 12, 'Unlicenced driving')]
    demerits_values7 = [('2030-05-27', 'Jim', 'Halpert', 12, 'SKIING')]

    c.executemany(persons_sql,persons_values)
    c.executemany(births_sql, births_values)
    c.executemany(users_sql,users_values)
    c.executemany(marriages_sql,marriages_values)
    c.executemany(vehicles_sql, vehicles_values)
    c.executemany(registration_sql, registration_values)
    c.executemany(registration_sql, registration_values2)
    c.executemany(tickets_sql, tickets_values)
    c.executemany(tickets_sql, tickets_values2)
    c.executemany(tickets_sql, tickets_values3)
    c.executemany(tickets_sql, tickets_values4)
    c.executemany(tickets_sql, tickets_values5)
    c.executemany(tickets_sql, tickets_values6)
    c.executemany(demerits_sql, demerits_values)
    c.executemany(demerits_sql, demerits_values2)
    c.executemany(demerits_sql, demerits_values3)
    c.executemany(demerits_sql, demerits_values4)
    c.executemany(demerits_sql, demerits_values5)
    c.executemany(demerits_sql, demerits_values6)
    c.executemany(demerits_sql, demerits_values7)
    conn.commit()
    return


def main():
    global conn, c
   
    path = "./database_test.db"
    connect(path)
    drop_tables()
    define_tables()
    insert_data()
    conn.commit()
    conn.close()
    return


if __name__ == "__main__":
    main()
