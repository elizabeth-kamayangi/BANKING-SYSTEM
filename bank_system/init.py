import sqlite3
from flask import Flask, request, render_template, flash, url_for, redirect
from dbsetup import *
from wtforms import Form, StringField, IntegerField, validators

app = Flask(__name__)
app.secret_key = 'nm,.gg87t2378e-y2t3e89t723e'


def connect(self):
    return sqlite3.connect('banksys.db')


class BankForm(Form):
    name = StringField('Bank Name', [validators.Length(min=3, max=80)])
    location = StringField('Location', [validators.Length(min=6, max=50)])


class Tellerform(Form):
    name = StringField('Teller Name',  [validators.Length(min=3, max=80)])
    resp_bank = StringField('Specific bank',  [validators.Length(min=3, max=80)])
    location = StringField('Location',  [validators.Length(min=3, max=80)])


class AccountForm(Form):
    acct_type = StringField('Account type', [validators.Length(min=3, max=80)])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_bank', methods=['GET', 'POST'])
def create_bank():
    form = BankForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        location = form.location.data

        # create cursor
        conn = connect(())

        # check
        b = conn.execute("SELECT * FROM banks WHERE name=?", [name]).fetchone()
        if b:
            error = 'Bank Already exists!'
            return render_template('create_bank.html', error=error, form=form)

        conn.execute("INSERT INTO banks(name, location) VALUES(?, ?)", (name, location))

        # commit to db
        conn.commit()
        conn.close()

        flash('Bank {} was successfully created'.format(name), 'Thank You')
        return redirect(url_for('dashboard'))
    return render_template('create_bank.html', form=form)


@app.route('/edit_bank/<string:id>', methods=['GET', 'POST'])
def edit_bank(id):
    # create cursor
    conn = connect(())

    # get bank by id
    bank = conn.execute("SELECT * FROM banks WHERE id = ?", [id]).fetchone()

    form = BankForm()
    # populate fields

    form.name.data = bank[1]
    form.location.data = bank[2]

    if request.method == 'POST' and form.validate():
        name = request.form['name']
        location = request.form['location']

        # create cursor and edit
        conn = connect(())

        conn.execute("UPDATE banks SET name =?, location = ? WHERE id = ?", (name, location, id))

        # commit and close
        conn.commit()
        conn.close()

        flash('{} has been updated'.format(name), 'Thanks')
        return redirect(url_for('dashboard'))
    return render_template('edit_bank.html', form=form)


@app.route('/delete_bank/<string:id>', methods=['POST'])
def delete_bank(id):
    # create cursor and execute delete query
    conn = connect(())

    conn.execute("DELETE FROM banks WHERE id = ?", [id])

    conn.commit()
    conn.close()
    flash('Bank was succesfully deleted', 'success')
    return redirect(url_for('dashboard'))


@app.route('/create_teller', methods=['GET', 'POST'])
def create_teller():
    form = Tellerform(request.form)

    conn = connect(())
    bank = conn.execute("SELECT * FROM banks").fetchall()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        resp_bank = form.resp_bank.data
        location = form.location.data

        # create cursor and execute
        conn = connect(())

        tel_res = conn.execute("SELECT * FROM tellers WHERE name=?", [name]).fetchone()
        if tel_res:
            error = 'The teller already exists with {}'.format(resp_bank)
            return render_template('create_teller.html', error=error, form=form, banks=bank)

        conn.execute("INSERT INTO tellers(name, resp_bank, location) VALUES(?,?,?)", (name, resp_bank, location))

        # commit to db
        conn.commit()
        conn.close()

        flash('The teller has been successfully added with {}'.format(resp_bank), 'success')
        return redirect(url_for('dashboard'))
    return render_template('create_teller.html', form=form, banks=bank)


class CustomerForm(Form):
    name = StringField('Customer Name', [validators.Length(min=3, max=80)])
    email = StringField('Email address', [validators.Length(min=3, max=80)])
    phon_num = StringField('Phone Number', [validators.Length(min=3, max=80)])
    address = StringField('Home address', [validators.Length(min=3, max=80)])
    acct_num = StringField('Account Number', [validators.Length(min=3, max=80)])
    acct_type = StringField('Account type')
    bank_id = StringField('Respective Bank')


@app.route('/dashboard')
def dashboard():
    # create cursor and execute
    conn = connect(())

    # get banks and tellers
    banks = conn.execute("SELECT * FROM banks").fetchall()
    tellers = conn.execute("SELECT * FROM tellers").fetchall()

    if banks or tellers:
        return render_template('dashboard.html', banks=banks, tellers=tellers)
    else:
        msg = 'No banks and tellers found, pliz create!'
        return render_template('dashboard.html', msg=msg)

#     commit and close
    conn.commit()
    conn.close()


@app.route('/edit_teller/<string:id>', methods=['GET', 'POST'])
def edit_teller(id):
    # create cursor
    conn = connect(())

    teller = conn.execute("SELECT * FROM tellers WHERE id = ?", [id]).fetchone()
    bank = conn.execute("SELECT * FROM banks").fetchall()

    form = Tellerform()
    # populate fields

    form.name.data = teller[1]
    form.resp_bank.data = teller[2]
    form.location.data = teller[3]

    if request.method == 'POST' and form.validate():
        name = request.form['name']
        resp_bank = request.form['resp_bank']
        location = request.form['location']

        # create cursor and execute
        conn = connect(())

        conn.execute("UPDATE tellers SET name = ?, resp_bank = ?, location = ? WHERE id = ?", (name, resp_bank, location, id))
        # commit and close
        conn.commit()
        conn.close()

        flash('Teller was successfully changed', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_teller.html', form=form, banks=bank)


@app.route('/tellers/<string:id>')
def tellers(id):
    cod=id
    return render_template('teller.html',cod=cod)

@app.route('/delete_teller/<string:id>', methods=['POST'])
def delete_teller(id):
    # create cursor and execute delete query
    conn = connect(())

    conn.execute("DELETE FROM tellers WHERE id = ?", [id])

    conn.commit()
    conn.close()
    flash('Teller was successfully deleted', 'success')
    return redirect(url_for('dashboard'))


@app.route('/create_customer', methods=['GET', 'POST'])
def create_customer():
    form = CustomerForm(request.form)

    conn = connect(())
    bank = conn.execute("SELECT * FROM banks").fetchall()
    type = conn.execute("SELECT * FROM accounts").fetchall()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        phon_num = form.phon_num.data
        address = form.address.data
        acct_num = form.acct_num.data
        acct_type = form.acct_type.data
        bank_id = form.bank_id.data

        # create cursor and execute
        conn = connect(())

        cust = conn.execute("SELECT * FROM customers WHERE email=?", [email]).fetchone()
        if cust:
            error = 'Customer already exists!'
            return render_template('create_customer.html', error=error, form=form, banks=bank, types=type)

        conn.execute("INSERT INTO customers(name, email, phon_num, address, acct_num, amount, acct_type, bank_id) "
                     "VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                     (name, email, phon_num, address, acct_num, 0, acct_type, bank_id))
        # commit and close
        conn.commit()
        conn.close()

        flash('New Customer created', 'success')
        return redirect(url_for('customers'))
    return render_template('create_customer.html', form=form, banks=bank, types=type)


@app.route('/edit_customer/<string:id>', methods=['GET', 'POST'])
def edit_customer(id):
    # create cursor and do queries
    conn = connect(())

    customs = conn.execute("SELECT * FROM customers WHERE id = ?", [id]).fetchone()
    bank = conn.execute("SELECT * FROM banks").fetchall()
    type = conn.execute("SELECT * FROM accounts").fetchall()
    form = CustomerForm()

    # populate fields
    form.name.data = customs[1]
    form.email.data = customs[2]
    form.phon_num.data = customs[3]
    form.address.data = customs[4]
    form.acct_num.data = customs[5]
    form.acct_type = customs[6]
    form.bank_id.data = customs[7]

    if request.method == 'POST' and form.validate():
        name = request.form['name']
        email = request.form['email']
        phon_num = request.form['phon_num']
        address = request.form['address']
        acct_num = request.form['acct_num']
        acct_type = request.form['acct_type']
        bank_id = request.form['bank_id']

        # do query to update info
        conn = connect(())

        conn.execute("UPDATE customers SET name = ?, email = ?, phon_num = ?, address = ?, acct_num = ?, acct_type = ?, bank_id = ? WHERE id = ?",
                     (name, email, phon_num, address, acct_num, acct_type,  bank_id, id))

        conn.commit()
        conn.close()
        flash('The customer info was successfully updated', 'success')
        return redirect(url_for('customers'))
    return render_template('edit_customer.html', form=form, banks=bank, types=type)


@app.route('/delete_customer/<string:id>', methods=['POST'])
def delete_customer(id):
    # create query to delete item
    conn = connect(())

    conn.execute("DELETE FROM customers WHERE id = ?", [id])

    conn.commit()
    conn.close()
    flash('The customer was successfully deleted', 'success')
    return redirect(url_for('customers'))


@app.route('/customers')
def customers():
    # create cursor and execute
    conn = connect(())

    # get banks and tellers
    customs = conn.execute("SELECT * FROM customers").fetchall()
    accounts = conn.execute("SELECT * FROM accounts").fetchall()

    if customs or accounts:
        return render_template('customers.html', customs=customs, accounts=accounts)
    else:
        msg = 'No customers or accounts found, pliz create'
        return render_template('customers.html', msg=msg)

    # commit and close
    conn.commit()
    conn.close()


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    form = AccountForm(request.form)

    if request.method == 'POST' and form.validate():
        acct_type = form.acct_type.data

#         create cursor check, and insert
        conn = connect(())

        account = conn.execute("SELECT * FROM accounts WHERE acct_type = ?", [acct_type]).fetchone()

        if account:
            error = 'This account type already exists!'
            return render_template('create_account.html', error=error, form=form)
        conn.execute("INSERT INTO accounts(acct_type) VALUES(?)", [acct_type])

#         commit to database
        conn.commit()
        conn.close()

        flash('{} account was successfully created'.format(acct_type), 'success')
        return redirect(url_for('customers'))
    return render_template('create_account.html', form=form)


@app.route('/edit_account/<string:id>', methods=['GET', 'POST'])
def edit_account(id):
    # create cursor and execute query
    conn = connect(())

    account = conn.execute("SELECT * FROM accounts WHERE id = ?", [id]).fetchone()

    form = AccountForm()

#     populate form
    form.acct_type.data = account[1]

    if request.method == 'POST' and form.validate():
        acct_type = request.form['acct_type']

#         create cursor and do update query
        conn = connect(())

        conn.execute("UPDATE accounts SET acct_type = ? WHERE id = ?", (acct_type, id))

        conn.commit()
        conn.close()

        flash('The {} type has been updated'.format(acct_type), 'success')
        return redirect(url_for('customers'))
    return render_template('edit_account.html', form=form)


@app.route('/delete_account/<string:id>', methods=['POST'])
def delete_account(id):
    # create cursor and do delete query
    conn = connect(())

    conn.execute("DELETE FROM accounts WHERE id = ?", [id])

    conn.commit()
    conn.close()
    flash('User account has been successfully deleted!', 'success')
    return redirect(url_for('customers'))


@app.route('/customer_self/<string:id>')
def customer_self(id):
    form = depositForm()
    # create connection and query db
    conn = connect(())
    #
    customer = conn.execute("SELECT * FROM customers WHERE id = ?", [id]).fetchone()
    return render_template('customer_self.html', id=customer[0], acc_no=customer[5], name=customer[1], acct_bal=customer[6], acct_type=customer[7], bank=customer[8], form= form)


@app.route('/get_loan')
def get_loan():
    pass


@app.route('/make_inquiry')
def make_inquiry():
    pass


class depositForm(Form):
    deposit = StringField('Deposit')


@app.route('/user_deposit/<string:id>', methods=['GET', 'POST'])
def user_deposit(id):
    # create query and deposit
    # conn = connect(())
    form = depositForm(request.form)

    if request.method == 'POST' and form.validate():

        new_dep = form.deposit.data
        if len(new_dep)<0 or not new_dep.isdigit():
            flash('Please input a valid amount', 'danger')
            return redirect(url_for('customer_self', id=str(id)))

        conn = connect(())

        old = (conn.execute("SELECT amount FROM customers WHERE id = ?", [id]).fetchone())[0]

        deposit = old + int(new_dep)

        conn.execute("UPDATE customers SET amount = ? WHERE id = ?", (deposit, id))
        conn.commit()
        conn.close()

        flash('New account balance is {}'.format(deposit), 'success')
        return redirect(url_for('customer_self', id=str(id)))
    return render_template('customer_self.html', form=form)


class loanForm(Form):
    amount = StringField('Amount')
    reason = StringField('Reason', [validators.Length(min=3, max=80)])
    period = StringField('Collateral Security and proof')


@app.route('/apply_for_loan/<string:id>', methods=['GET', 'POST'])
def apply_for_loan(id):
    # do check for neccessary credentials

    form = loanForm(request.form)

    # conn.execute("SELECT bank_id, ")

    if request.method == 'POST' and form.validate():
        amount = form.amount.data
        reason = form.reason.data
        period = form.period.data
        acct_num = 'hr'
        bank_id = 'trr'

#         check database
        conn = connect(())

        conn.execute("INSERT INTO loans(amount, reason, period, status, acct_num, bank_id) VALUES(?, ?, ?, ?, ?, ?)", (amount, reason, period, 0, acct_num, bank_id ))

        conn.commit()
        conn.close()
        flash('Your loan request is being processed, please wait.')
        return redirect(url_for('customer_self', id=str(id)))
    return render_template('loanform.html', form=form, id=str(id))


@app.route('/loans')
def loans():
    # pass
    conn = connect(())

    #     check existing loan requests and approve or disprove
    loans = conn.execute("SELECT * FROM loans").fetchall()
    if not loans:
        msg = 'No pending loan requests'
        return redirect(url_for('loans.html', msg=msg))

    conn.commit()
    conn.close()
    return render_template('loans.html', loans=loans)


@app.route('/approve_loan/<string:id>', methods=['POST'])
def approve_loan(id):
    # when a loan is authorized the user's account is credited
    conn = connect(())

    loan = conn.execute("SELECT * FROM loans").fetchall()

    cstatus = conn.execute("SELECT status FROM loans WHERE id = ?", [id]).fetchone()
    if cstatus == 0:
        new_status = 1
    conn.execute("UPDATE loans SET status = ?", [new_status])
    conn.commit()
    conn.close()

    flash('The loan request was successfully approved', 'success')
    return render_template('teller_self.html', loans=loan)


@app.route('/reject_loan/<string:id>', methods=['POST'])
def reject_loan():
    pass


@app.route('/request_card/<string:id>')
def request_card(id):
    # do query
    conn = connect(())

    bank = conn.execute("SELECT bank_id FROM customers WHERE id = ?", [id]).fetchone()

    flash('{} ATM Card has been successfully issued'.format(bank),'Thank you')
    return redirect(url_for('customer_self', id=str(id)))


@app.route('/check_account_type')
def check_account_type():
    pass


@app.route('/load_account')
def load_account():
    pass


@app.route('/collect_money')
def collect_money():
    pass


if __name__ == '__main__':
    app.run(debug=True)

