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
        return {'method':'none','prediction':0.0,'note':'No expense data yet.','confidence':0}
    if len(totals) < 3:
        # Fallback: average with recent trend
        avg = float(np.mean(totals))
        trend = totals[-1] - totals[0] if len(totals) > 1 else 0
        prediction = avg + (trend / 2)
        prediction = max(0.0, round(prediction, 2))
        confidence = 50 + (len(totals) * 10)  # Confidence increases with more data
        return {
            'method': 'weighted_average',
            'prediction': prediction,
            'note': 'Using weighted average with trend analysis.',
            'confidence': min(confidence, 70)  # Cap confidence at 70% for limited data
        }

    try:
        from sklearn.linear_model import LinearRegression
        from sklearn.metrics import r2_score
        import statsmodels.api as sm

        # Prepare data
        X = np.arange(len(totals)).reshape(-1,1)
        y = np.array(totals)

        # Linear regression with confidence interval
        model = LinearRegression()
        model.fit(X, y)
        next_idx = np.array([[len(totals)]])
        pred_lr = float(model.predict(next_idx)[0])

        # Calculate R-squared for model quality
        r2 = r2_score(y, model.predict(X))

        # Time series decomposition for seasonal patterns
        if len(totals) >= 12:
            decomposition = sm.tsa.seasonal_decompose(y, period=12, extrapolate_trend='freq')
            seasonal = decomposition.seasonal[-1]  # Use last seasonal component
            trend = decomposition.trend[-1]  # Use last trend component
            pred_adjusted = pred_lr + seasonal
        else:
            pred_adjusted = pred_lr

        # Exponential smoothing for recent trends
        alpha = 0.3  # Smoothing factor
        exp_smoothed = totals[-1]
        for i in range(len(totals)-2, -1, -1):
            exp_smoothed = alpha * totals[i] + (1-alpha) * exp_smoothed

        # Combine predictions with weights
        final_pred = 0.6 * pred_adjusted + 0.4 * exp_smoothed
        final_pred = max(0.0, round(final_pred, 2))

        # Calculate confidence score (0-100)
        confidence = min(95, int(r2 * 70 + len(totals)))
        if len(totals) >= 12:
            confidence += 5  # Bonus for seasonal data

        # Determine prediction quality
        if confidence >= 90:
            quality = "High confidence prediction"
        elif confidence >= 75:
            quality = "Good confidence prediction"
        else:
            quality = "Moderate confidence prediction"

        return {
            'method': 'advanced_ml',
            'prediction': final_pred,
            'note': f'{quality} using ML and time series analysis.',
            'confidence': confidence
        }

    except Exception as e:
        # Enhanced fallback using weighted average
        weights = np.exp(np.linspace(-1, 0, len(totals)))  # Exponential weights
        weights = weights / weights.sum()
        weighted_avg = float(np.sum(weights * totals))
        prediction = max(0.0, round(weighted_avg, 2))
        
        return {
            'method': 'weighted_average',
            'prediction': prediction,
            'note': 'Using exponentially weighted average.',
            'confidence': 65
        }

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
    # Safely access target_amount with fallback to monthly_savings_target
    if goal and hasattr(goal, 'target_amount') and goal.target_amount is not None:
        target = goal.target_amount
    else:
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
