from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database models
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Expense {self.description}>"

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Income {self.description}>"

# Route for the homepage
@app.route('/')
def index():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    incomes = Income.query.order_by(Income.date.desc()).all()
    total_income = sum(income.amount for income in incomes)
    total_expenses = sum(expense.amount for expense in expenses)
    remaining_balance = total_income - total_expenses
    return render_template('index.html', expenses=expenses, incomes=incomes, total_income=total_income, total_expenses=total_expenses, remaining_balance=remaining_balance)

# Route for adding a new expense
@app.route('/add_expense', methods=['POST'])
def add_expense():
    description = request.form['description']
    amount = request.form['amount']

    if not description or not amount:
        return redirect(url_for('index'))

    try:
        amount = float(amount)
    except ValueError:
        return redirect(url_for('index'))

    new_expense = Expense(description=description, amount=amount)

    try:
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "There was an issue adding your expense."

# Route for adding a new income
@app.route('/add_income', methods=['POST'])
def add_income():
    description = request.form['description']
    amount = request.form['amount']

    if not description or not amount:
        return redirect(url_for('index'))

    try:
        amount = float(amount)
    except ValueError:
        return redirect(url_for('index'))

    new_income = Income(description=description, amount=amount)

    try:
        db.session.add(new_income)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "There was an issue adding your income."

# Route for deleting an expense
@app.route('/delete_expense/<int:id>')
def delete_expense(id):
    expense_to_delete = Expense.query.get_or_404(id)

    try:
        db.session.delete(expense_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "There was a problem deleting that expense."

# Route for deleting an income
@app.route('/delete_income/<int:id>')
def delete_income(id):
    income_to_delete = Income.query.get_or_404(id)

    try:
        db.session.delete(income_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "There was a problem deleting that income."

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
