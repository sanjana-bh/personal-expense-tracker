# 💰 Personal Expense Tracker

A professional, full-featured web application built with **Streamlit** for tracking personal expenses, analyzing spending patterns, and managing budgets.

## 📊 Overview

Personal Expense Tracker helps you:
- Track daily expenses effortlessly
- Understand spending habits through visual analytics
- Maintain a monthly budget
- Gain insights into financial patterns

## ✨ Features

- **Smart Dashboard** — KPI cards, month-over-month comparisons, budget progress bar, recent transactions
- **Advanced Analytics** — trends over 7/30/90 days, month, year, or all time; category breakdowns; auto-generated spending insights
- **Full CRUD Operations** — add, view, edit, and delete expenses with validation and confirmation dialogs
- **Data Management** — export/import CSV, manage categories, clear all data
- **Interactive Visualizations** — bar, pie/donut, and line charts via Plotly

## 🏗️ Project Structure

```
Personal_Expense_Tracker/
│
├── app.py                    # Main application file
├── expenses.json             # Data storage (auto-generated)
├── requirements.txt          # Python dependencies
└── README.md                 # Documentation
```

## 🧩 Core Components

| Page | Purpose | Key Features |
|------|---------|--------------|
| Dashboard | Overview | KPI cards, charts, budget tracking, recent transactions |
| Add Expense | Data entry | Form with validation, category selection, date picker |
| History | Management | Filters, search, edit/delete, export CSV |
| Analytics | Insights | Trends, category analysis, spending insights |
| Manage | Administration | Category management, data import/export, clear data |

The backend is powered by an **ExpenseManager** class that handles CRUD operations, JSON-based data persistence, and analytics calculations.

## 🛠️ Tech Stack

```
streamlit==1.28.0        # Web framework
pandas==2.0.3            # Data manipulation
plotly==5.15.0           # Interactive visualizations
python-dateutil==2.8.2   # Date handling
```

## 🔐 Data Storage

Expenses are stored locally in `expenses.json`:

```json
{
  "expenses": [
    {
      "id": "a1b2c3d4",
      "amount": 250.00,
      "category": "Food & Dining",
      "description": "Lunch at Cafe",
      "date": "2024-01-15",
      "created_at": "2024-01-15T12:30:00"
    }
  ],
  "budget": 10000
}
```

Every change auto-saves, each expense gets a unique ID, and corrupted data is handled gracefully.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/sanjana-bh/personal_expense_tracker.git
cd Personal_Expense_Tracker

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
streamlit run app.py

# 4. Open your browser to
http://localhost:8501
```

## 🎨 Customization

**Change the color scheme** in `app.py`:

```python
COLORS = {
    'primary': '#2563EB',
    'secondary': '#64748B',
    'success': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444'
}
```

**Add new expense categories**:

```python
self.categories = [
    "Food & Dining",
    "Transportation",
    # Add your categories here
]
```

## 🧪 Testing Checklist

- [ ] Add Expense — form validation and data persistence
- [ ] Edit Expense — update functionality
- [ ] Delete Expense — deletion confirmation dialog
- [ ] Budget Tracking — calculations
- [ ] CSV Export/Import — data integrity
- [ ] Category Management — CRUD operations

## 📈 Roadmap

- [ ] Multi-user authentication
- [ ] Recurring expenses (subscriptions)
- [ ] Receipt image upload
- [ ] Mobile app (React Native / Flutter)
- [ ] Cloud sync across devices
- [ ] AI-powered spending predictions
- [ ] Multi-currency support
- [ ] Dark mode

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).

---

Built with **Python, Streamlit, Pandas, and Plotly** by **Sanjana Bharadwaj**. ✨

A demonstration of Python programming, data analysis, and UI/UX design — created as a portfolio project for showcasing practical development and analytical skills. 🚀
