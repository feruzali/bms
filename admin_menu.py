from connection import con,cur
import database
import database_admin as db_admin

def print_closed_acc_history():
    res = db_admin.get_closed_accounts()
    if len(res) == 0:
        print("N.A.")
    else:      
        print("Account No \t\t\t Closed On")
        for i in range(0, len(res)):
            print(res[i][0]," \t\t\t ",res[i][1])

def list_customers():
    res = db_admin.get_customers()
    if len(res) == 0:
        print("N.A.")
    else:      
        print("Customer ID \t\t\t Name \t\t\t Status")
        for i in range(0,len(res)):
            print(res[i][0]," \t\t\t ",res[i][1]," \t\t\t ",res[i][2])

def get_customer():
    cus_name = input("\nEnter customer`s name: ")
    
    res = db_admin.get_customer_by_name(cus_name)
    if len(res) == 0:
        print('Customer doesn`t exist')
    else:
        print("Customer ID \t\t Status")
        for i in range(0,len(res)):
            print(res[i][0]," \t\t\t ",res[i][1])


def unlock_acc():
    try:
        cus_id = int(input("\nEnter customer ID: "))
    except:
        print("Invalid ID")
        return
    if db_admin.check_customer_exists(cus_id) is True:
        database.reset_login_attempts(cus_id)
        print("Customer with ID",cus_id,"was unlocked successfully")
    else:
        print("Customer doesn't exist")


def unlock_all():
    res = db_admin.get_locked_accounts()

    if len(res) == 0:
            print("There are no locked accounts")   
    else:
        for i in range(0, len(res)):
            database.reset_login_attempts(res[i][0])
    print("All locked accounts were unlocked successfully")

def print_fd_report():
    try:
        cus_id = int(input("\nEnter customer ID: "))
    except:
        print("Invalid ID")
        return
    if db_admin.check_customer_exists(cus_id) is True:
        res = db_admin.get_fd_report(cus_id)
        if len(res) == 0:
            print("N.A.")
        else:
            print("Account No \t\t\t\t Amount \t\t\t\t Deposit Term")
            for i in range(0,len(res)):
                print(res[i][0],"   \t\t\t\t   ",res[i][1],"   \t\t\t\t   ",res[i][2],"months")
    else:
        print("Customer doesn't exist")


def print_fd_report_vis_customer():
    try:
        cus_id = int(input("\nEnter customer ID: "))
    except:
        print("Invalid ID")
        return
    if db_admin.check_customer_exists(cus_id) is True:
        if db_admin.get_fd_count(cus_id) > 0:
            res = db_admin.get_fd_report_vis_customer(cus_id)
            if len(res) == 0:
                print("N.A.")
            else:
                print("Customer ID \t\t\t\t Account No \t\t\t\t Amount \t\t\t\t Deposit Term")
                for i in range(0,len(res)):
                    print(res[i][0],"   \t\t\t\t  ",res[i][1],"   \t\t\t\t   ",res[i][2],"  \t\t\t\t  ",res[i][3],"months")
        else:
            print("Customer doesn't have any FD Account")
    else:
        print("Customer doesn't exist")

def print_fd_report_wrt_amount():
    try:
        amount = int(input("\nEnter an amount (in multiples of 1000): "))
    except:
        print("Invalid Amount")
        return
    if amount > 0 and amount%1000 == 0 :
        res = db_admin.get_fd_report_wrt_amount(amount)
        if len(res) == 0:
                print("N.A.")
        else:
            print("Customer ID \t\t\t\t Account No \t\t\t\t Amount \t\t\t\t Deposit Term")
            for i in range(0,len(res)):
                print(res[i][0],"   \t\t\t\t   ",res[i][1],"   \t\t\t\t   ",res[i][2],"  \t\t\t\t  ",res[i][3],"months")

    else:
        print("Sorry! Invalid Amount")

def print_loan_report():
    try:
        cus_id = int(input("\nEnter customer ID: "))
    except:
        print("Invalid ID")
        return
    if db_admin.check_customer_exists(cus_id) is True:
        res = db_admin.get_loan_report(cus_id)
        if len(res) == 0:
            print("Not Availed")
        else:
            print("Account No \t\t\t\t Amount \t\t\t\t Repayment Term")
            for i in range(0,len(res)):
                print(res[i][0],"   \t\t\t\t   ",res[i][1],"   \t\t\t\t   ",res[i][2],"months")
    else:
        print("Customer Doesn't exist")

def print_loan_report_vis_customer():
    try:
        cus_id = int(input("\nEnter customer ID : "))
    except:
        print("Invalid ID")
        return
    if db_admin.check_customer_exists(cus_id) is True:
        if db_admin.get_loan_count(cus_id) > 0:
            res = db_admin.get_loan_report_vis_customer(cus_id)
            if len(res) == 0:
                print("N.A.")
            else:
                print("Customer ID \t\t\t\t Account No \t\t\t\t Amount \t\t\t\t Repayment Term")
                for i in range(0,len(res)):
                    print(res[i][0],"   \t\t\t\t   ",res[i][1],"   \t\t\t\t   ",res[i][2],"  \t\t\t\t  ",res[i][3],"months")
        else:
            print("Customer hasn't availed any loan")
    else:
        print("Customer Doesn't exist")

def print_loan_report_wrt_amount():
    try:
        amount = int(input("\nEnter an amount (in multiples of 1000): "))
    except:
        print("Invalid Amount")
        return
    if amount > 0 and amount%1000 == 0 :
        res = db_admin.get_loan_report_wrt_amount(amount)
        if len(res) == 0:
                print("N.A.")
        else:
            print("Customer ID \t\t\t\t Name \t\t\t\t Loan Amount")
            for i in range(0,len(res)):
                print(res[i][0],"   \t\t\t\t  ",res[i][1],"  \t\t\t\t  ",res[i][2])

    else:
        print("Sorry! Invalid Amount")

def print_loan_fd_report():
    res = db_admin.get_loan_fd_report()
    if len(res) == 0:
        print("N.A.")
    else:
        print("Customer ID \t\t\t\t Name \t\t\t\t Sum of Loan Amounts \t\t\t\t Sum of FD Amounts")
        for i in range(0,len(res)):
            print(res[i][0],"   \t\t\t\t   ",res[i][1],"  \t\t\t\t  ",res[i][2], " \t\t\t\t ",res[i][3])


def print_report_no_loan():
    res = db_admin.get_report_no_loan()
    if len(res) == 0:
        print("N.A.")
    else:
        print("Customer ID \t\t\t\t Name ")
        for i in range(0,len(res)):
            print(res[i][0],"   \t\t\t\t",res[i][1])

def print_report_no_fd():
    res = db_admin.get_report_no_fd()
    if len(res) == 0:
        print("N.A.")
    else:
        print("Customer ID \t\t\t\t Name ")
        for i in range(0,len(res)):
            print(res[i][0],"   \t\t\t\t",res[i][1])

def print_report_no_fd_loan():
    res = db_admin.get_report_no_fd_loan()
    if len(res) == 0:
        print("N.A.")
    else:
        print("Customer ID \t\t\t\t Name ")
        for i in range(0,len(res)):
            print(res[i][0],"   \t\t\t\t",res[i][1])

def print_transactions():
    res = db_admin.get_transactions()

    if len(res) == 0:
        print("N.A.")
    else:
        print("Date \t\t\t Transaction No \t\t\t Amount \t\t\t Account No ")
        for i in range(0,len(res)):
            print(res[i][0],"   \t\t\t",res[i][1],"   \t\t\t",res[i][2],"   \t\t\t",res[i][3])

def print_acc_transaction():
    try:
        acc = int(input("\nEnter Account No: "))
    except:
        print("Invalid ID")
        return
    if db_admin.check_acc_exists(acc) is True:
        res = db_admin.get_acc_transaction(acc)

        if len(res) == 0:
            print("N.A.")
        else:
            print("Date \t\t\t Transaction No \t\t\t Amount")
            for i in range(0,len(res)):
                print(res[i][0],"   \t\t\t",res[i][1],"   \t\t\t",res[i][2])
    else:
        print("Account doesn't exist")
