# Python Capstone Project – Personal Expense Tracker

A portfolio-ready Flask + SQLite web application for recording and reviewing personal expenses.

## Features

- Add expense records
- Delete expense records
- SQLite database storage
- Category-wise spending summary
- Total spending calculation
- Input validation and exception safety
- Application logging
- Responsive web interface
- Clean project structure
- Deployment-ready configuration

## Architecture

```text
Browser
   ↓
Flask Routes
   ↓
Validation / Business Logic
   ↓
SQLite Database
   ↓
HTML Templates + CSS
```

## Database Schema

### expenses

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| title | TEXT | Expense name |
| category | TEXT | Spending category |
| amount | REAL | Positive expense amount |
| expense_date | TEXT | Date of expense |

## Project Structure

```text
Python_Capstone_Expense_Tracker/
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── requirements.txt
├── Procfile
├── runtime.txt
├── .gitignore
└── README.md
```

## Run Locally

```bash
python -m pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Demo Flow

1. Add an expense.
2. Verify it appears in the table.
3. Check the total amount and category summary.
4. Delete the expense.
5. Verify the record is removed.
6. Open `app.log` to see application events.

## Deployment

The project includes a `Procfile` and `requirements.txt` for deployment on platforms such as Render or another Python-compatible hosting service. Configure the start command as:

```text
gunicorn app:app
```

## Future Enhancements

- Edit expense records
- User authentication
- Monthly charts
- Export to CSV
- Budget alerts
