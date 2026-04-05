from models.record import Record
from extensions import db

def get_active_records(type_filter=None, category_filter=None, date_filter=None):
    query = Record.query.filter_by(deleted=False)
    if type_filter:
        query = query.filter_by(type=type_filter)
    if category_filter:
        query = query.filter_by(category=category_filter)
    if date_filter:
        query = query.filter_by(date=date_filter)
    return query.all()

def get_summary():
    records = Record.query.filter_by(deleted=False).all()

    total_income = sum(r.amount for r in records if r.type == "income")
    total_expense = sum(r.amount for r in records if r.type == "expense")

    category_totals = {}
    for r in records:
        category_totals[r.category] = category_totals.get(r.category, 0) + r.amount

    recent = sorted(records, key=lambda r: r.date, reverse=True)[:5]

    return {
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "net_balance": round(total_income - total_expense, 2),
        "category_totals": {k: round(v, 2) for k, v in category_totals.items()},
        "recent_activity": [r.to_dict() for r in recent],
    }

def get_monthly_trends():
    records = Record.query.filter_by(deleted=False).all()
    monthly = {}
    for r in records:
        month = r.date[:7]
        if month not in monthly:
            monthly[month] = {"income": 0.0, "expense": 0.0}
        monthly[month][r.type] = round(monthly[month][r.type] + r.amount, 2)
    return dict(sorted(monthly.items()))
