# 💰 Personal Finance Manager

A simple, interactive web app to track personal income and expenses, built with **Python** and **Streamlit**.

Features

- Add income and expense transactions with date, category, amount, and notes
- Automatic summary of total income, total expenses, and current balance
- Expense breakdown by category (pie chart)
- Monthly income vs. expenses comparison (bar chart)
- Filterable transaction history table
- Export transactions as a CSV file
- Data persists locally between sessions (`transactions.csv`)

Tech Stack

- **Python**
- **Streamlit** — UI and app framework
- **Pandas** — data handling
- **Matplotlib** — charts and visualizations

How to Run Locally

1. Clone the repository:
   ```
   git clone https://github.com/SandhyaAK24/personal-finance-manager.git
   cd personal-finance-manager
   ```

2. Install the requirements:
   ```
   pip install -r requirements.txt
   ```

3. Run the app:
   ```
   streamlit run streamlit_app.py
   ```

4. Open the local URL shown in your terminal (usually `http://localhost:8501`).

Project Structure

```
├── streamlit_app.py     # Main application
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

Future Improvements

- User authentication for multi-user support
- Budget goals and alerts when spending exceeds a limit
- Switch storage from CSV to a proper database (SQLite/MySQL)
- Recurring transaction support

Author

**Sandhya A K**
[GitHub](https://github.com/SandhyaAK24) · [LinkedIn](https://www.linkedin.com/in/sandhya-a-k-b4b1a8314)
