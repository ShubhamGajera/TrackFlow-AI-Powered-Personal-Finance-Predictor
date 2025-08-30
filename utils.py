from models import db, Transaction, Goal
from sqlalchemy import extract
from datetime import date
import pandas as pd
import numpy as np

def get_monthly_totals(user_id: int):
    # Aggregate expenses per month (expenses only)
    rows = db.session.query(
        extract('year', Transaction.date).label('year'),
        extract('month', Transaction.date).label('month'),
        db.func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.user_id==user_id,
        Transaction.type=='expense'
    ).group_by('year','month').order_by('year','month').all()

    months = []
    totals = []
    for r in rows:
        y, m, t = int(r.year), int(r.month), float(r.total)
        months.append(f"{y}-{m:02d}")
        totals.append(round(t, 2))

    return months, totals

def predict_next_month_expense(months, totals):
    if len(totals) == 0:
        return {'method':'none','prediction':0.0,'note':'No expense data yet.'}
    if len(totals) < 3:
        # Fallback: average
        avg = float(np.mean(totals))
        return {'method':'average','prediction':round(avg,2),'note':'Using simple average due to limited data.'}

    # Use a simple linear regression over time index
    try:
        from sklearn.linear_model import LinearRegression
        X = np.arange(len(totals)).reshape(-1,1)
        y = np.array(totals)
        model = LinearRegression()
        model.fit(X, y)
        next_idx = np.array([[len(totals)]])
        pred = float(model.predict(next_idx)[0])
        pred = max(0.0, round(pred, 2))
        return {'method':'linear_regression','prediction':pred,'note':'Predicted using linear trend.'}
    except Exception as e:
        # fallback
        avg = float(np.mean(totals))
        return {'method':'average','prediction':round(avg,2),'note':'ML fallback to average.'}

def category_breakdown(user_id: int):
    # Sum expenses by category for the current month
    today = date.today()
    rows = db.session.query(
        Transaction.category,
        db.func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.user_id==user_id,
        Transaction.type=='expense',
        extract('year', Transaction.date)==today.year,
        extract('month', Transaction.date)==today.month
    ).group_by(Transaction.category).all()

    return {r.category: float(r.total) for r in rows}

def saving_tips(user_id: int):
    # Analyze this month's expenses vs. incomes and produce simple tips
    today = date.today()
    expenses = db.session.query(db.func.sum(Transaction.amount)).filter(
        Transaction.user_id==user_id,
        Transaction.type=='expense',
        extract('year', Transaction.date)==today.year,
        extract('month', Transaction.date)==today.month
    ).scalar() or 0.0

    incomes = db.session.query(db.func.sum(Transaction.amount)).filter(
        Transaction.user_id==user_id,
        Transaction.type=='income',
        extract('year', Transaction.date)==today.year,
        extract('month', Transaction.date)==today.month
    ).scalar() or 0.0

    breakdown = db.session.query(
        Transaction.category,
        db.func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.user_id==user_id,
        Transaction.type=='expense',
        extract('year', Transaction.date)==today.year,
        extract('month', Transaction.date)==today.month
    ).group_by(Transaction.category).order_by(db.desc('total')).all()

    goal = Goal.query.filter_by(user_id=user_id).first()
    target = goal.monthly_savings_target if goal else 0.0

    tips = []
    if incomes <= 0:
        tips.append('Add income records to get personalized savings ratio.')
    else:
        savings = incomes - expenses
        rate = (savings / incomes) * 100 if incomes else 0
        tips.append(f"Current savings rate: {rate:.1f}%. Target: {target:.0f} per month.")

    # Suggest cutting top category by 10-20%
    if breakdown:
        top_cat, top_total = breakdown[0].category, float(breakdown[0].total)
        reduce_10 = round(top_total * 0.10, 2)
        tips.append(f"Try reducing your '{top_cat}' spending by ~10% (≈ {reduce_10}).")
    if target > 0:
        shortfall = max(0.0, target - max(0.0, incomes - expenses))
        if shortfall > 0:
            tips.append(f"Shortfall to hit target: {shortfall:.2f}. Consider trimming discretionary categories.")

    snapshot = {
        'this_month_income': round(incomes,2),
        'this_month_expense': round(expenses,2),
        'top_categories': [(b.category, float(b.total)) for b in breakdown[:5]]
    }
    return tips, snapshot
