
import bcrypt,sqlite3,os,sys
import traceback
from cryptography.fernet import Fernet
import base64
import getpass
masterpass=""
if not os.path.exists('test.db'):
    print("Database not exists.... Creating now")
    with sqlite3.connect('test.db') as conn:
        conn.execute('''
            CREATE TABLE PASSWORDS
            (ID INT PRIMARY KEY NOT NULL,
            SITE  TEXT NOT NULL,
            USERNAME TEXT NOT NULL,
            PASSWORD TEXT NOT NULL);
        ''')
    print("Database created Successfully")
else:
    print("Database file found",end='')
#all in binary
def encrypt(password,data):
    key = bytes(password,'utf-8')
    key = base64.b64encode(key)
    
    f = Fernet(key)
    
    # the plaintext is converted to ciphertext
    token = f.encrypt(data.encode('utf-8'))
    return token
def decrypt(password,token):
    key = bytes(password,'utf-8')
    key = base64.b64encode(key)
    #print(key)  
    # value of key is assigned to a variable
    f = Fernet(key)
    d = f.decrypt(token)
    return d
while True:
    try:
        with sqlite3.connect('test.db') as conn:
            cursor = conn.execute("SELECT * FROM PASSWORDS")
            if len(list(cursor)) == 0:
                print("No Master password exists")
                password = input("Enter new master password : ")
                pwd_bytes = password.encode("utf-8")
                salt = bcrypt.gensalt()
                pwd_hash = bcrypt.hashpw(pwd_bytes, salt)
                query = f'''INSERT INTO PASSWORDS VALUES(0,"master","master","{pwd_hash.decode('utf-8')}")''';
                conn.execute(query)
                conn.commit()
                print("Master Password Set Successfully , Remember it !")
        
        if masterpass == "":
            masterpass = getpass.getpass('Enter Master Password:')
        
            #Verify masterpass
            with sqlite3.connect('test.db') as conn:
                cursor = conn.execute("SELECT password FROM PASSWORDS where id=0") 
                for row in cursor:
                    pwd_hash = row[0] 
                if bcrypt.checkpw(masterpass.encode("utf-8"),pwd_hash.encode("utf-8")):
                    print("\nPassword Correct")
                else:
                    print("\nPassword Incorrect")
                    exit(0)
        ch = input('''\n1.Display all records\n2.View Record\n3.Search Records\n4.Add New Record\n5.Delete record\n6.Exit\n\nCHOICE : ''')
        if ch == '1':
            print("Displaying Records")
            with sqlite3.connect('test.db') as conn:
                cursor = conn.execute("SELECT * FROM PASSWORDS")
                txt = "{:5}{:<25}{:<20}{:<20}".format("ID", "SITE", "USERNAME", "PASSWORD")
                print(txt)
                for row in cursor:
                    txt = "{:<5}{:<25}{:<20}{:<20}".format(row[0],row[1],row[2],"********")
                    print(txt)
        elif ch == '2':
            id = input("Enter ID : ")
            with sqlite3.connect('test.db') as conn:
                cursor = conn.execute(f"SELECT * FROM PASSWORDS where id={id}")
                if len(list(cursor)) == 0:
                    print("NO Record with such ID")
                else:
                    cursor = conn.execute(f"SELECT * FROM PASSWORDS where id={id}")
                    for row in cursor:
                        print("SITE : ",row[1])
                        print("USERNAME : ",row[2])
                        if(id == '0'):
                            print("PASSWORD :",row[3])
                        else:
                            key = masterpass
                            if len(key) > 32:
                                key = key[0:32]
                            elif len(key) < 32:
                                key = key + (32 - len(key))*"0"
                            password = decrypt(key,row[3])
                            print("Password : ",password.decode('utf-8'))
        elif ch == '3':
            name = input("Enter sitename : ")
            with sqlite3.connect('test.db') as conn:
                cursor = conn.execute(f'''SELECT * FROM PASSWORDS where site like "%{name}%"''')
                if len(list(cursor)) == 0:
                    print("NO Records with such ID")
                else:
                    txt = "{:5}{:<25}{:<20}{:<20}".format("ID", "SITE", "USERNAME", "PASSWORD")
                    print(txt)
                    for row in cursor:
                        txt = "{:<5}{:<25}{:<20}{:<20}".format(row[0],row[1],row[2],"********")
                        print(txt)
        elif ch=='4':
            #to get next id
            next = 0
            with sqlite3.connect('test.db') as conn:
                cursor = conn.execute("SELECT * FROM PASSWORDS")
                next = len(list(cursor))
            name = input("Enter sitename : ")
            username = input("Enter username : ")
            password = getpass.getpass('Enter Password:')
            key = masterpass
            if len(key) > 32:
                key = key[0:32]
            elif len(password) < 32:
                key = key + (32 - len(key))*"0"
            token = encrypt(key,password)
            with sqlite3.connect('test.db') as conn:
                query = f'''INSERT INTO PASSWORDS VALUES({next},"{name}","{username}","{token.decode('utf-8')}")'''
                print(query)
                conn.execute(query)
                print("Record Inserted Successfully")
        elif ch=='5':
            id = input("Enter ID : ")
            with sqlite3.connect('test.db') as conn:
                cursor = conn.execute(f"SELECT * FROM PASSWORDS where id={id}")
                if len(list(cursor)) == 0:
                    print("NO Record with such ID")
                else:
                    if (id == '0'):
                        print("Cannot delete Master Record!")
                    else:
                        cursor = conn.execute(f"DELETE FROM PASSWORDS where id={id}")
                        print("Record Deleted Successfully")
        elif ch=='6':
            exit(0)
        else:
            print("Incorrect Choice!")
                    
    except Exception as e:
        traceback.print_exc()
