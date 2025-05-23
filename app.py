import streamlit as st
import pandas as pd
import datetime
from io import BytesIO

# Set page config
st.set_page_config(page_title="Trading Journal", layout="wide")
st.title("Trading Journal")

# Initialize session state
if 'trades' not in st.session_state:
    st.session_state.trades = []

# Sidebar for user settings
with st.sidebar:
    st.header("User Settings")
    dark_mode = st.checkbox("Dark Mode")
    email_reminder = st.checkbox("Daily Email Reminder")

# Trade logging form
with st.form("Log a Trade", clear_on_submit=True):
    st.subheader("Enter Trade Details")
    col1, col2, col3 = st.columns(3)
    with col1:
        date = st.date_input("Date", value=datetime.date.today())
        time = st.time_input("Time", value=datetime.datetime.now().time())
        asset = st.text_input("Asset (e.g., BTC/USD)")
        direction = st.selectbox("Direction", ["Long", "Short"])
    with col2:
        entry_price = st.number_input("Entry Price", step=0.01)
        exit_price = st.number_input("Exit Price", step=0.01)
        position_size = st.number_input("Position Size", step=1)
        fees = st.number_input("Fees", step=0.01)
    with col3:
        stop_loss = st.number_input("Stop Loss", step=0.01)
        take_profit = st.number_input("Take Profit", step=0.01)
        strategy = st.selectbox("Strategy Used", ["Breakout", "Pullback", "News-based", "Other"])

    rationale = st.text_area("Trade Rationale")
    screenshot = st.file_uploader("Pre-Trade Screenshot (optional)", type=["png", "jpg", "jpeg"])

    post_col1, post_col2 = st.columns(2)
    with post_col1:
        outcome = st.selectbox("Outcome", ["Profit", "Loss", "Break-even"])
        mistakes = st.text_area("Mistakes Made")
    with post_col2:
        emotions = st.select_slider("Emotions Felt", options=["Calm", "Neutral", "Anxious", "Overconfident", "Fearful", "Greedy"])
        lessons = st.text_area("Lessons Learned")

    submitted = st.form_submit_button("Add Trade")
    if submitted:
        st.session_state.trades.append({
            "date": date,
            "time": time,
            "asset": asset,
            "direction": direction,
            "entry_price": entry_price,
            "exit_price": exit_price,
            "position_size": position_size,
            "fees": fees,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "strategy": strategy,
            "rationale": rationale,
            "outcome": outcome,
            "mistakes": mistakes,
            "emotions": emotions,
            "lessons": lessons
        })
        st.success("Trade added!")

# Convert to DataFrame
df = pd.DataFrame(st.session_state.trades)

# Show Dashboard
st.subheader("Trade Analytics")
if not df.empty:
    st.metric("Total Trades", len(df))
    st.metric("Win Rate", f"{(df['outcome'] == 'Profit').mean() * 100:.2f}%")
    st.metric("Average R", f"{((df['exit_price'] - df['entry_price']) / (df['entry_price'] - df['stop_loss'])).mean():.2f}")

    st.line_chart(df['exit_price'])
    st.dataframe(df)

    # Export option
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    st.download_button(
        label="Download CSV",
        data=buffer.getvalue(),
        file_name="trading_journal.csv",
        mime="text/csv"
    )
else:
    st.info("No trades logged yet.")
