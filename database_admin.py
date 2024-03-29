from connection import con,cur

def check_customer_exists(id):
    sql = "select count(*) from customers where customer_id = :id"
    cur.execute(sql, {"id":id})
    res = cur.fetchall()
    count = res[0][0]
    if count == 1:
        return True
    else:
        return False

def check_acc_exists(acc):
    sql = "select count(*) from accounts where account_no = :acc_no"
    cur.execute(sql, {"acc_no":acc})
    res = cur.fetchall()
    count = res[0][0]
    if count == 1:
        return True
    else:
        return False

def get_customers():
    sql = "select customer_id, name, status from customers"
    cur.execute(sql)
    res = cur.fetchall()
    return res

def get_customer_by_name(name):
    sql = "select customer_id, status from customers where name = :name"
    cur.execute(sql, {"name": name})
    res = cur.fetchall()
    return res

def get_locked_accounts():
    sql = "select customer_id from customers where status = 'locked' "
    cur.execute(sql)
    res = cur.fetchall()
    return res

def get_closed_accounts():
    sql = "select * from closed_accounts"
    cur.execute(sql)
    res = cur.fetchall()
    return res

def get_fd_report(cus_id):
    sql = "select account_no,amount,deposit_term from accounts_fd where customer_id = :id"
    cur.execute(sql, {"id":cus_id})
    res = cur.fetchall()
    return res

def get_fd_count(cus_id):
    sql = "select count(*) from accounts_fd where customer_id = :id"
    cur.execute(sql, {"id":cus_id})
    res = cur.fetchall()
    count = res[0][0]
    return count

def get_fd_report_vis_customer(cus_id):
    sql = "select * from accounts_fd where amount > (select sum(amount) from accounts_fd where customer_id = :id)"
    cur.execute(sql, {"id":cus_id})
    res = cur.fetchall()
    return res

def get_fd_report_wrt_amount(amount):
    sql = "select * from accounts_fd where amount > :amt"
    cur.execute(sql, {"amt":amount})
    res = cur.fetchall()
    return res

def get_loan_report(cus_id):
    sql = "select loan_id,loan_amount,repay_term from accounts_loans where customer_id = :id"
    cur.execute(sql, {"id":cus_id})
    res = cur.fetchall()
    return res

def get_loan_count(cus_id):
    sql = "select count(*) from accounts_loans where customer_id = :id"
    cur.execute(sql, {"id":cus_id})
    res = cur.fetchall()
    count = res[0][0]
    return count

def get_loan_report_vis_customer(cus_id):
    sql = "select customer_id,loan_id,loan_amount,repay_term from accounts_loans where loan_amount > (select sum(loan_amount) from accounts_loans where customer_id = :id)"
    cur.execute(sql, {"id":cus_id})
    res = cur.fetchall()
    return res

def get_loan_report_wrt_amount(amount):
    sql = """select a.customer_id,c.name,a.loan_amount from accounts_loans a,customers c
              where a.customer_id = c.customer_id and loan_amount > :amt"""
    cur.execute(sql, {"amt":amount})
    res = cur.fetchall()
    return res

def get_loan_fd_report():
    sql = """select c.customer_id,c.name,sum.loan_amount,sum.amount from
            (select al.customer_id,al.loan_amount,af.amount from (select customer_id,sum(loan_amount) as loan_amount from accounts_loans group by customer_id) al,
            (select customer_id,sum(amount) as amount from accounts_fd group by customer_id) af
            where al.customer_id = af.customer_id) sum,customers c
            where sum.customer_id = c.customer_id and sum.loan_amount > sum.amount """
    cur.execute(sql)
    res = cur.fetchall()
    return res

def get_report_no_loan():
    sql = """select customer_id, name from customers
              where customer_id not in (select distinct(customer_id) from accounts_loans)"""
    cur.execute(sql)
    res = cur.fetchall()
    return res

def get_report_no_fd():
    sql = """select customer_id, name from customers
              where customer_id not in (select distinct(customer_id) from accounts_fd)"""
    cur.execute(sql)
    res = cur.fetchall()
    return res

def get_report_no_fd_loan():
    sql = """select customer_id, name from customers
              where customer_id not in (select distinct(customer_id) from accounts_fd) and
              customer_id not in (select distinct(customer_id) from accounts_loans)"""
    cur.execute(sql)
    res = cur.fetchall()
    return res

def get_transactions():
    sql = "select transaction_date, transaction_id, amount, account_no from transactions"
    cur.execute(sql)
    res = cur.fetchall()
    return res

def get_acc_transaction(acc):
    sql = "select transaction_date, transaction_id, amount from transactions where account_no = :acc_no"
    cur.execute(sql, {"acc_no":acc})
    res = cur.fetchall()
    return res