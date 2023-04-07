import sqlite3 as sq
from datetime import *
import os,time

Path="./Database/Fees.db"

def Add_customer(Name,Mobile_no,Paid_amnt,Tamount):

    try:
        Feebook=sq.connect(Path)
    except:
        Crash_Report("Can't connect to Database")
        return False
    Pen=Feebook.cursor()
    
    Pen.execute(f'''SELECT MAX(Regno) FROM FEE''')    
    Regno=0
    for x in Pen:
        if x[0]!=None:
            Regno=x[0]+1
        else:
            Regno=0

    try:
        Pen.execute(f'''
    INSERT INTO FEE VALUES({Regno},"{Name}",{Mobile_no},"{datetime.now()}",{Tamount},{Paid_amnt},{int(Tamount)-int(Paid_amnt)})
    ''')

    except:
        lst=[Name,type(Name),Mobile_no,type(Mobile_no),Paid_amnt,type(Paid_amnt),Tamount,type(Tamount)]
        Crash_Report(f'Record Addition Failed Record:<{lst}>')
        return False

    Feebook.commit()
    Feebook.close()
    return True

def Get_Full_Data():
    try:
        Feebook=sq.connect(Path)
    except:
        Crash_Report("Can't connect to Database")
    Pen=Feebook.cursor()
    Pen.execute('''
    SELECT * FROM FEE ORDER BY TIME DESC LIMIT 25
    ''')
    value=Pen.fetchmany(25)
    Feebook.close()

    return value

def Get_Data(Regno):
    try:
        Feebook=sq.connect(Path)
    except:
        Crash_Report("Can't connect to Database")
    Pen=Feebook.cursor()
    Pen.execute(f"""
    SELECT * FROM FEE WHERE RegNo={Regno}
    """)    
    value=Pen.fetchall()
    Feebook.close()
    return value

def Search_Customer(Phno):
    try:
        Feebook=sq.connect(Path)
    except:
        Crash_Report("Can't connect to Database")
    Pen=Feebook.cursor()
    Pen.execute(f'''
    SELECT Regno FROM FEE WHERE Mobileno={Phno}
    ''')
    return Pen.fetchall()

def Max_Regno():
    try:
        Feebook=sq.connect(Path)
    except:
        Crash_Report("Can't connect to Database")
        return False
    Pen=Feebook.cursor()
    Pen.execute(f'''SELECT MAX(Regno) FROM FEE''')    
    lst=Pen.fetchone()
    if lst[0]==None:
        return 0
    else:
        return lst

def update_db(Regno,column,new_value):
    columnlst=["Regno","Name","Mobileno","Time","Totalamnt","Paidamnt"]
    try:
        Feebook=sq.connect(Path)
    except:
        Crash_Report("Can't connect to Database")
    Pen=Feebook.cursor()
    #try:
    if column==1 or column==3:
        Pen.execute(f'''
    UPDATE FEE SET {columnlst[column]}="{new_value}" WHERE Regno={Regno}  
    ''')
    elif column==4 or column==5:
        Pen.execute(f"""
        UPDATE FEE SET {columnlst[column]}={new_value} WHERE Regno={Regno}
        """)
        Pen.execute(f'''
        UPDATE FEE SET Bal=Totalamnt-Paidamnt WHERE Regno={Regno};
        ''')
    else:
        try:
            Pen.execute(f'''
    UPDATE FEE SET {columnlst[column]}={new_value} WHERE Regno={Regno}  
    ''')

        except:
            Crash_Report(f"Record Update Error Regno={Regno} Column={column} New_value={new_value}")
            Feebook.close()
            return False
    Feebook.commit()
    Feebook.close()
    return True

def Delete_customer(Regno):
    try:
        Feebook=sq.connect(Path)
    except:
        Crash_Report("Can't connect to Database")
    Pen=Feebook.cursor()
    try:
        Pen.execute(f'''
    DELETE FROM FEE WHERE Regno={Regno}
    ''')
    except:
        Crash_Report(f"Record Deletion Error {Regno}")
        return False
    Feebook.commit()
    Feebook.close()
    return True
    
def Crash_Report(Error):
    try:
        os.mkdir("CrashReports")
    except:
        pass
    with open("./CrashReports.txt","a") as f:
        f.writelines(f"[{datetime.now()}]{Error}\n")

def Print_page(name_cust,phone_cust,Tamnt_cust,Bal_cust):


    with open("Bill.txt","r") as f:
        lines=f.read()
    newline=lines.format(name=f"{name_cust}",date=f"{date.today()}",phone=f"{phone_cust}",tamnt=f"{Tamnt_cust}",bal=f"{Bal_cust}")


    with open("Bill_temp.txt","w") as f:
        f.write(newline) 

    os.startfile("Bill_temp.txt","print")

    time.sleep(5)
    os.remove("Bill_temp.txt")