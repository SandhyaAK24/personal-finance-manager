import streamlit as st
import pandas as pd
import os
from datetime import date
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# Personal Finance Manager
# A simple Streamlit app to track income and expenses, categorize spending,
# and visualize monthly financial trends.
# ----------------------------------------------------------------------------

st.set_page_config(page_title="Personal Finance Manager", page_icon="💰", layout="wide")

DATA_FILE = "transactions.csv"
CATEGORIES = {
    "Income": ["Salary", "Freelance", "Investment", "Other Income"],
    "Expense": ["Food", "Rent", "Transport", "Utilities", "Shopping", "Entertainment", "Health", "Other Expense"],
}


def load_data():
    """Load transactions from the CSV file, or create an empty DataFrame if none exists."""
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE, parse_dates=["Date"])
    else:
        df = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Note"])
    return df


def save_data(df):
    """Persist transactions to the CSV file."""
    df.to_csv(DATA_FILE, index=False)


def add_transaction(df, entry_date, entry_type, category, amount, note):
    """Append a new transaction and save it."""
    new_row = pd.DataFrame(
        [{"Date": pd.to_datetime(entry_date), "Type": entry_type, "Category": category, "Amount": amount, "Note": note}]
    )
    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)
    return df


# ----------------------------------------------------------------------------
# App state
# ----------------------------------------------------------------------------
if "transactions" not in st.session_state:
    st.session_state.transactions = load_data()

df = st.session_state.transactions

st.title("💰 Personal Finance Manager")
st.caption("Track your income and expenses, and visualize where your money goes.")

# ----------------------------------------------------------------------------
# Sidebar: Add a transaction
# ----------------------------------------------------------------------------
st.sidebar.header("Add a Transaction")

with st.sidebar.form("add_transaction_form", clear_on_submit=True):
    entry_date = st.date_input("Date", value=date.today())
    entry_type = st.selectbox("Type", ["Income", "Expense"])
    category = st.selectbox("Category", CATEGORIES[entry_type])
    amount = st.number_input("Amount (₹)", min_value=0.0, step=100.0, format="%.2f")
    note = st.text_input("Note (optional)")
    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        if amount <= 0:
            st.sidebar.error("Amount must be greater than 0.")
        else:
            st.session_state.transactions = add_transaction(
                df, entry_date, entry_type, category, amount, note
            )
            st.sidebar.success(f"{entry_type} of ₹{amount:.2f} added!")
            st.rerun()

df = st.session_state.transactions

# ----------------------------------------------------------------------------
# Summary metrics
# ----------------------------------------------------------------------------
total_income = df.loc[df["Type"] == "Income", "Amount"].sum()
total_expense = df.loc[df["Type"] == "Expense", "Amount"].sum()
balance = total_income - total_expense

col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"₹{total_income:,.2f}")
col2.metric("Total Expenses", f"₹{total_expense:,.2f}")
col3.metric("Balance", f"₹{balance:,.2f}", delta=f"{balance:,.2f}")

st.divider()

# ----------------------------------------------------------------------------
# Charts
# ----------------------------------------------------------------------------
if df.empty:
    st.info("No transactions yet. Add your first one from the sidebar to get started.")
else:
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Expenses by Category")
        expense_df = df[df["Type"] == "Expense"]
        if not expense_df.empty:
            category_totals = expense_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
            fig, ax = plt.subplots()
            ax.pie(category_totals, labels=category_totals.index, autopct="%1.1f%%", startangle=90)
            ax.axis("equal")
            st.pyplot(fig)
        else:
            st.write("No expenses recorded yet.")

    with chart_col2:
        st.subheader("Monthly Income vs Expenses")
        monthly_df = df.copy()
        monthly_df["Month"] = monthly_df["Date"].dt.to_period("M").astype(str)
        monthly_summary = monthly_df.groupby(["Month", "Type"])["Amount"].sum().unstack(fill_value=0)
        if not monthly_summary.empty:
            fig2, ax2 = plt.subplots()
            monthly_summary.plot(kind="bar", ax=ax2)
            ax2.set_ylabel("Amount (₹)")
            ax2.set_xlabel("Month")
            plt.xticks(rotation=45)
            st.pyplot(fig2)
        else:
            st.write("Not enough data yet.")

    st.divider()

    # ------------------------------------------------------------------------
    # Transaction history table
    # ------------------------------------------------------------------------
    st.subheader("Transaction History")

    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        type_filter = st.multiselect("Filter by type", options=["Income", "Expense"], default=["Income", "Expense"])
    with filter_col2:
        category_filter = st.multiselect(
            "Filter by category",
            options=sorted(df["Category"].unique()),
            default=sorted(df["Category"].unique()),
        )

    filtered_df = df[df["Type"].isin(type_filter) & df["Category"].isin(category_filter)]
    filtered_df = filtered_df.sort_values("Date", ascending=False)

    st.dataframe(
        filtered_df.style.format({"Amount": "₹{:.2f}"}),
        use_container_width=True,
        hide_index=True,
    )

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download as CSV", data=csv, file_name="transactions.csv", mime="text/csv")
