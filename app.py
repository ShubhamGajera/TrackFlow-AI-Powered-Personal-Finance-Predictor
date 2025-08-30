from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Transaction, Goal
from config import Config
from utils import get_monthly_totals, predict_next_month_expense, category_breakdown, saving_tips
from datetime import datetime, date

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Create tables if not exists
    with app.app_context():
        db.create_all()

    # ---------- Home ----------
    @app.route('/')
    def home():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('home.html')

    # ---------- Register ----------
    @app.route('/register', methods=['GET','POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username','').strip()
            email = request.form.get('email','').strip().lower()
            password = request.form.get('password','')
            role = request.form.get('role','user')  # default role

            if not username or not email or not password:
                flash('All fields are required', 'danger')
                return redirect(url_for('register'))

            # Check if username/email exists
            if User.query.filter((User.username==username)|(User.email==email)).first():
                flash('Username or email already exists', 'warning')
                return redirect(url_for('register'))

            user = User(username=username, email=email, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))

        return render_template('register.html')

    # ---------- Login ----------
    @app.route('/login', methods=['GET','POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email','').strip().lower()
            password = request.form.get('password','')
            user = User.query.filter_by(email=email).first()

            if user and user.check_password(password):
                login_user(user)
                flash('Logged in successfully', 'success')

                # Redirect based on role
                if user.role == 'admin':
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('dashboard'))

            flash('Invalid credentials', 'danger')
            return redirect(url_for('login'))

        return render_template('login.html')

    # ---------- Logout ----------
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('home'))

    # ---------- User Dashboard ----------
    @app.route('/dashboard')
    @login_required
    def dashboard():
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))

        today = date.today()
        month_start = date(today.year, today.month, 1)
        month_transactions = Transaction.query.filter(
            Transaction.user_id==current_user.id,
            Transaction.date >= month_start
        ).all()

        income_this_month = sum(t.amount for t in month_transactions if t.type == 'income')
        expense_this_month = sum(t.amount for t in month_transactions if t.type == 'expense')
        months, totals = get_monthly_totals(current_user.id)
        by_category = category_breakdown(current_user.id)

        return render_template('dashboard.html',
                               income_this_month=income_this_month,
                               expense_this_month=expense_this_month,
                               months=months, totals=totals,
                               by_category=by_category)

    # ---------- Transactions ----------
    @app.route('/transactions/add', methods=['GET','POST'])
    @login_required
    def add_transaction():
        if request.method == 'POST':
            ttype = request.form.get('type','expense')
            amount = request.form.get('amount','0')
            category = request.form.get('category','Other').strip() or 'Other'
            note = request.form.get('note','').strip()
            date_str = request.form.get('date','')
            try:
                amount = float(amount)
            except ValueError:
                flash('Amount must be a number', 'warning')
                return redirect(url_for('add_transaction'))
            if amount <= 0:
                flash('Amount must be positive', 'warning')
                return redirect(url_for('add_transaction'))

            try:
                tdate = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else date.today()
            except ValueError:
                tdate = date.today()

            tx = Transaction(
                user_id=current_user.id,
                type=ttype,
                amount=amount,
                category=category,
                note=note,
                date=tdate
            )
            db.session.add(tx)
            db.session.commit()
            flash('Transaction added', 'success')
            return redirect(url_for('transactions'))

        return render_template('add_transaction.html')

    @app.route('/transactions')
    @login_required
    def transactions():
        category = request.args.get('category','')
        start = request.args.get('start','')
        end = request.args.get('end','')

        q = Transaction.query.filter_by(user_id=current_user.id)
        if category:
            q = q.filter(Transaction.category==category)
        if start:
            try:
                sdate = datetime.strptime(start, '%Y-%m-%d').date()
                q = q.filter(Transaction.date >= sdate)
            except ValueError:
                pass
        if end:
            try:
                edate = datetime.strptime(end, '%Y-%m-%d').date()
                q = q.filter(Transaction.date <= edate)
            except ValueError:
                pass

        items = q.order_by(Transaction.date.desc(), Transaction.id.desc()).all()
        return render_template('transactions.html', items=items)

    # ---------- Predictions ----------
    @app.route('/predictions')
    @login_required
    def predictions():
        months, totals = get_monthly_totals(current_user.id)
        prediction = predict_next_month_expense(months, totals)
        return render_template('predictions.html', months=months, totals=totals, prediction=prediction)

    # ---------- Savings ----------
    @app.route('/savings', methods=['GET','POST'])
    @login_required
    def savings():
        goal = Goal.query.filter_by(user_id=current_user.id).first()
        if request.method == 'POST':
            target = request.form.get('monthly_savings_target','0')
            try:
                target = float(target)
            except ValueError:
                flash('Target must be a number', 'warning')
                return redirect(url_for('savings'))

            if not goal:
                goal = Goal(user_id=current_user.id, monthly_savings_target=target)
                db.session.add(goal)
            else:
                goal.monthly_savings_target = target
            db.session.commit()
            flash('Savings target updated', 'success')
            return redirect(url_for('savings'))

        tips, snapshot = saving_tips(current_user.id)
        return render_template('savings.html', goal=goal, tips=tips, snapshot=snapshot)

    # ---------- Profile ----------
    @app.route('/profile', methods=['GET','POST'])
    @login_required
    def profile():
        if request.method == 'POST':
            username = request.form.get('username','').strip()
            email = request.form.get('email','').strip().lower()
            password = request.form.get('password','')

            if username:
                current_user.username = username
            if email:
                current_user.email = email
            if password:
                current_user.set_password(password)
            db.session.commit()
            flash('Profile updated', 'success')
            return redirect(url_for('profile'))

        return render_template('profile.html')

    # ---------- About ----------
    @app.route('/about')
    def about():
        return render_template('about.html')

    # ---------- Admin Panel ----------
    @app.route('/admin/dashboard')
    @login_required
    def admin_dashboard():
        if current_user.role != 'admin':
            flash("Access denied. Admins only.", "danger")
            return redirect(url_for('dashboard'))

        users = User.query.all()
        transactions = Transaction.query.all()
        goals = Goal.query.all()

        total_users = len(users)
        total_transactions = len(transactions)
        total_income = sum(t.amount for t in transactions if t.type == 'income')
        total_expense = sum(t.amount for t in transactions if t.type == 'expense')
        total_goals = len(goals)

        return render_template('admin_dashboard.html',
                               users=users,
                               transactions=transactions,
                               goals=goals,
                               total_users=total_users,
                               total_transactions=total_transactions,
                               total_income=total_income,
                               total_expense=total_expense,
                               total_goals=total_goals)

    # ---------- Admin: Delete User ----------
    @app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
    @login_required
    def delete_user(user_id):
        if current_user.role != 'admin':
            return redirect(url_for('dashboard'))

        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.username} deleted successfully.', 'success')
        return redirect(url_for('admin_dashboard'))

    # ---------- Admin: Delete Transaction ----------
    @app.route('/admin/delete_transaction/<int:transaction_id>', methods=['POST'])
    @login_required
    def delete_transaction(transaction_id):
        if current_user.role != 'admin':
            return redirect(url_for('dashboard'))

        transaction = Transaction.query.get_or_404(transaction_id)
        db.session.delete(transaction)
        db.session.commit()
        flash('Transaction deleted successfully.', 'success')
        return redirect(url_for('admin_dashboard'))

    # ---------- Admin: Edit User ----------
    @app.route('/admin/edit_user/<int:user_id>', methods=['GET','POST'])
    @login_required
    def edit_user(user_id):
        if current_user.role != 'admin':
            return redirect(url_for('dashboard'))

        user = User.query.get_or_404(user_id)
        if request.method == 'POST':
            user.role = request.form['role']
            db.session.commit()
            flash('User role updated successfully.', 'success')
            return redirect(url_for('admin_dashboard'))

        return render_template('edit_user.html', user=user)

    return app


app = create_app()
# ---------------- Run the app ----------------
if __name__ == "__main__":
    app.run(debug=True)
