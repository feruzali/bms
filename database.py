import sqlite3
import datetime
from classes import Customer, Account, Savings, Current, Fixed_Deposit
from connection import con, cur
from random import randint

def sign_up_customer(customer):
    name = customer.get_name()
    password = customer.get_password()

    id = randint(10000, 99999)
    while True:
        sql = "select count(*) from customers where customer_id = :id"
        cur.execute(sql, {"id":id})
        res = cur.fetchall()
        count = res[0][0]
        if count == 0:
            break
        else:
            id = randint(10000, 99999)
            continue

    status = customer.get_status()
    att = customer.get_login_attempts()
    sql = "insert into customers values(:id,:name,:status,:att,:password)"
    cur.execute(sql, {"id":id, "name":name, "status":status, "att":att, "password":password})
    con.commit()
    print("Congratulations! Your Account was Created Successfully")
    print("Your Customer ID : ",id)
    return id

def login_customer(id, password):
    sql = "select count(*) from customers where customer_id = :id and password = :password"
    cur.execute(sql, {"id":id, "password":password})
    res = cur.fetchall()
    count = res[0][0]
    if count == 1:
        return True
    else:
        return False

def open_new_account_customer(account, cus_id):
    withdrawals_left = None
    account_type = account.get_account_type()
    bal = account.get_balance()
    opened_on = datetime.datetime.now().strftime("%d-%b-%Y")
    status = "open"

    acc_no = randint(100000, 999999)
    while True:
        sql = "select count(*) from accounts where account_no = :acc_no"
        cur.execute(sql, {"acc_no":acc_no})
        res = cur.fetchall()
        count = res[0][0]
        if count == 0:
            break
        else:
            acc_no = randint(100000, 999999)
            continue

    if account_type == "savings":
        withdrawals_left = 10
    
    sql = "insert into accounts values(:cus_id,:acc_no,:opened_on,:acc_type,:status,:bal,:wd)"
    cur.execute(sql , {"cus_id":cus_id, "acc_no":acc_no, "opened_on":opened_on, "acc_type":account_type, "status":status, "bal":bal, "wd":withdrawals_left})

    if account_type == "fd":
        term = account.get_deposit_term()
        sql = "insert into fd values (:acc_no,:amount,:term)"
        cur.execute(sql, {"acc_no":acc_no, "term":term, "amount":bal})

    con.commit()
    print("Account Opened Successfully")
    print("Account No is : ",acc_no)

def get_all_info_customer(id):
    sql = "select * from customers where customer_id = :id"
    cur.execute(sql, {"id":id})
    res = cur.fetchall()
    if len(res) == 0:
        return None
    customer = Customer()
    status = res[0][2]
    att = res[0][3]
    customer.set_customer_id(id)
    customer.set_status(status)
    customer.set_login_attempts(att)
    return customer

def get_all_info_account(acc_no, id, msg):
    account = None
    sql = None
    if msg == "transfer":
        sql = "select * from accounts where account_no = :acc_no and account_type != 'fd' and status = 'open'"
        cur.execute(sql, {"acc_no":acc_no})
    elif msg == "loan":
        sql = "select * from accounts where account_no = :acc_no and customer_id = :id and account_type = 'savings' and status = 'open'"
        cur.execute(sql, {"id":id ,"acc_no":acc_no})
    else:
        sql = "select * from accounts where account_no = :acc_no and customer_id = :id and account_type != 'fd' and status = 'open'"
        cur.execute(sql, {"acc_no":acc_no, "id":id})

    res = cur.fetchall()
    if len(res) == 0:
        return None

    account_no = res[0][1]
    account_type = res[0][3]
    balance = res[0][5]
    wd_left = res[0][6]
    if account_type == "savings":
        account = Savings()
    else:
        account = Current()

    account.set_account_type(account_type)
    account.set_balance(balance)
    account.set_account_no(account_no)
    account.set_withdrawals_left(wd_left)
    return account

def money_deposit_customer(account, amount):
    bal = account.get_balance()
    acc_no = account.get_account_no()
    acc_type = "credit"
    sql = "update accounts set balance = :bal where account_no = :acc_no"
    cur.execute(sql , {"bal":bal, "acc_no":acc_no})
    
    t_id = randint(1000000, 9999999)
    while True:
        sql = "select count(*) from transactions where transaction_id = :t_id"
        cur.execute(sql, {"t_id":t_id})
        res = cur.fetchall()
        count = res[0][0]
        if count == 0:
            break
        else:
            t_id = randint(1000000, 9999999)
            continue

    sql = "insert into transactions values (:t_id,:acc_no,:type,:amount,:bal,:date_on)"
    date = datetime.datetime.now().strftime("%d-%b-%Y")
    cur.execute(sql , {"t_id":t_id, "acc_no":acc_no, "type":acc_type , "amount":amount , "bal":bal, "date_on":date})
    con.commit()

def money_withdraw_customer(account, amount, msg):
    acc_type = account.get_account_type()
    wd_left = account.get_withdrawals_left()
    bal = account.get_balance()
    acc_no = account.get_account_no()
    acc_type = "debit"
    sql = "update accounts set balance = :bal where account_no = :acc_no"
    cur.execute(sql , {"bal":bal, "acc_no":acc_no})

    t_id = randint(1000000, 9999999)
    while True:
        sql = "select count(*) from transactions where transaction_id = :t_id"
        cur.execute(sql, {"t_id":t_id})
        res = cur.fetchall()
        count = res[0][0]
        if count == 0:
            break
        else:
            t_id = randint(1000000, 9999999)
            continue

    sql = "insert into transactions values (:t_id,:acc_no,:type,:amount,:bal,:date_on)"
    date = datetime.datetime.now().strftime("%d-%b-%Y")
    cur.execute(sql , {"t_id":t_id ,"acc_no":acc_no, "type":acc_type , "amount":amount , "bal":bal, "date_on":date })
    if acc_type == "savings" and msg != "transfer":
        wd_left -= 1
        sql = "update accounts set withdrawals_left = :wd_left where account_no = :acc_no"
        cur.execute(sql, {"wd_left":wd_left, "acc_no":acc_no})
    con.commit()

def transfer_money_customer(account_sender, account_receiver, amount):
    if account_sender.withdraw(amount) == True:
        account_receiver.deposit(amount)
        money_withdraw_customer(account_sender,amount,"transfer")
        money_deposit_customer(account_receiver,amount)
        print("Transfer Completed !")
        print("New Balance for Account No ",account_sender.get_account_no()," : ",account_sender.get_balance())
        print("New Balance for Account No ",account_receiver.get_account_no()," : ",account_receiver.get_balance())


def login_admin(id, password):
    sql = "select count(*) from admin where admin_id = :id and password = :password"
    cur.execute(sql , {"id":id, "password":password})
    res = cur.fetchall()
    count = res[0][0]
    if count == 1:
        return True
    else:
        return False

def close_account_customer(account):
    acc_no = account.get_account_no()
    balance = account.get_balance()
    sql = "update accounts set status='closed',balance = 0 where account_no = :acc_no"
    cur.execute(sql, {"acc_no":acc_no})
    closed_on = datetime.datetime.now().strftime("%d-%b-%Y")
    sql = "insert into closed_accounts values(:acc_no,:closed_on)"
    cur.execute(sql, {"acc_no":acc_no, "closed_on":closed_on})
    print("Account Closed Successfully !")
    print("$",balance," will be delivered to you shortly")
    con.commit()

def get_loan_customer(acc_no,loan_amt,loan_term):
    loan_id = randint(1000, 9999)
    while True:
        sql = "select count(*) from loans where loan_id = :loan_id"
        cur.execute(sql, {"loan_id":loan_id})
        res = cur.fetchall()
        count = res[0][0]
        if count == 0:
            break
        else:
            loan_id = randint(1000, 9999)
            continue

    sql = "insert into loans values (:acc_no,:loan_id,:amount,:loan_term)"
    cur.execute(sql , {"acc_no":acc_no, "loan_id":loan_id, "loan_term":loan_term, "amount":loan_amt})
    con.commit()
    print("Loan Availed Successfully")

def reset_withdrawals():
    sql = "update accounts set withdrawals_left = 10 where account_type = 'savings'"
    cur.execute(sql)
    con.commit()

def reset_login_attempts(id):
    sql = "update customers set login_attempts = 3 where customer_id = :id"
    cur.execute(sql,{"id":id})
    sql = "update customers set status = 'open' where customer_id = :id"
    cur.execute(sql,{"id":id})
    con.commit()

def update_customer(customer):
    id = customer.get_customer_id()
    status = customer.get_status()
    att = customer.get_login_attempts()
    sql = "update customers set status = :status,login_attempts = :att where customer_id = :id"
    cur.execute(sql, {"status":status, "att":att, "id":id})
    con.commit()