import re
import datetime
import sqlite3
from typing import List, NamedTuple, Optional

import pytz
from decouple import config

import db
import exceptions
from categories import Categories


class Message(NamedTuple):
    """ Structure of unparsed message """
    amount: int
    category_text: str


class Expense(NamedTuple):
    """ Structure of expanse db record"""
    id: Optional[int]
    amount: int
    category_name: str


def add_expense(raw_message: str) -> Expense:
    parsed_message = _parse_message(raw_message)
    category = Categories().get_category(parsed_message.category_text)
    db.insert("expense", {
        "amount": parsed_message.amount,
        "created": _get_now_formatted(),
        "category_name": category.name,
        "raw_text": raw_message
    })
    return Expense(
        id=None, amount=parsed_message.amount, category_name=category.name
    )


def get_today_statistics() -> str:
    cursor = db.get_cursor()
    cursor.execute("SELECT SUM(amount) "
                   "FROM expense WHERE date(created)=date('now', 'localtime')")
    result = cursor.fetchone()
    if not result[0]:
        return "No expenses today"
    all_today_expenses = result[0]
    cursor.execute("SELECT SUM(amount) "
                   "FROM expense WHERE date(created)=date('now', 'localtime') "
                   "AND category_name IN "
                   "(SELECT name FROM category WHERE is_primary_expense=true)")
    result = cursor.fetchone()
    primary_today_expenses = result[0] if result[0] else 0
    return (f"Today's expenses:\n"
            f"total — {all_today_expenses} $\n"
            f"primary — {primary_today_expenses} $ / {_get_daily_limit()} $")


def get_month_statistics() -> str:
    now_datetime = _get_now_datetime()
    cursor = db.get_cursor()
    cursor.execute(f"SELECT SUM(amount) "
                   f"FROM expense WHERE date(created) >= date('now', 'start of month')")
    result = cursor.fetchone()
    if not result[0]:
        return "No expenses yet this month"
    all_month_expenses = result[0]
    cursor.execute(f"SELECT SUM(amount) "
                   f"FROM expense WHERE date(created) >= date('now', 'start of month') "
                   f"AND category_name IN "
                   f"(SELECT name FROM category WHERE is_primary_expense=true)")
    result = cursor.fetchone()
    primary_month_expenses = result[0] if result[0] else 0
    return (f"Current month expenses:\n"
            f"total — {all_month_expenses} $\n"
            f"primary — {primary_month_expenses} $ / "
            f"{now_datetime.day * _get_daily_limit()} $")


def get_last_transactions(quantity: int = 10) -> List[Expense]:
    cursor = db.get_cursor()
    cursor.execute(
        f"SELECT id, amount, category_name FROM expense "
        f"ORDER BY created DESC LIMIT {quantity}")
    rows = cursor.fetchall()
    last_expenses = [Expense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]
    return last_expenses


def delete_expense(row_id: int) -> None:
    try:
        db.delete("expense", row_id)
    except sqlite3.ProgrammingError:
        raise exceptions.NotCorrectMessage(
            f'Expense with ({row_id}) ID does not exist'
        )


def _parse_message(raw_message: str) -> Message:
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage(
            "Cannot parse the message. Write it in format, for example:\n5 coffee"
        )
    amount = int(regexp_result.group(1).replace(" ", ""))
    category_text = regexp_result.group(2).strip().lower()
    return Message(amount=amount, category_text=category_text)


def _get_now_formatted() -> str:
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    tz = pytz.timezone(config("TZ"))
    now = datetime.datetime.now(tz)
    return now


def _get_daily_limit() -> int:
    return db.fetchone("budget", ["daily_limit"])["daily_limit"]
