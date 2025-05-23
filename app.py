import streamlit as st
import pandas as pd
import datetime
from io import BytesIO
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Trading Journal", layout="wide")
st.title("Smart Trading Journal")

# Initialize session state
if 'trades' not in st.session_state:
    st.session_state.trades = []

# Sidebar for settings
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

# Analytics section
st.subheader("Smart Analysis")
if not df.empty:
    st.markdown("### 1. Emotion-Performance Analysis")
    emotion_stats = df.groupby("emotions")["outcome"].value_counts().unstack().fillna(0)
    emotion_stats = emotion_stats.apply(lambda x: x / x.sum(), axis=1) * 100

    fig1, ax1 = plt.subplots()
    emotion_stats.plot(kind='bar', stacked=True, ax=ax1)
    ax1.set_ylabel("Percentage")
    ax1.set_title("Outcome by Emotion")
    st.pyplot(fig1)

    st.markdown("### 2. Strategy Effectiveness")
    strategy_stats = df.groupby("strategy")["outcome"].value_counts().unstack().fillna(0)
    strategy_stats = strategy_stats.apply(lambda x: x / x.sum(), axis=1) * 100

    fig2, ax2 = plt.subplots()
    strategy_stats.plot(kind='bar', stacked=True, ax=ax2)
    ax2.set_ylabel("Percentage")
    ax2.set_title("Outcome by Strategy")
    st.pyplot(fig2)

    st.markdown("### 3. Pre-Trade Advisory Assistant")
    with st.form("Pre-Trade Advisor"):
        st.info("This tool gives you feedback based on your emotional state and strategy choice")
        current_emotion = st.select_slider("Current Emotion", options=["Calm", "Neutral", "Anxious", "Overconfident", "Fearful", "Greedy"])
        selected_strategy = st.selectbox("Planned Strategy", ["Breakout", "Pullback", "News-based", "Other"])
        advisory = st.form_submit_button("Get Advisory")
        if advisory:
            emotion_outcome = emotion_stats.loc[current_emotion].get("Loss", 0)
            strategy_outcome = strategy_stats.loc[selected_strategy].get("Loss", 0)

            if emotion_outcome > 50:
                st.warning(f"You tend to lose {emotion_outcome:.1f}% of trades when feeling {current_emotion}. Consider waiting or adjusting your size.")
            else:
                st.success(f"You usually perform well when {current_emotion}. Proceed with discipline.")

            if strategy_outcome > 50:
                st.warning(f"Your {selected_strategy} strategy has a high loss rate ({strategy_outcome:.1f}%). Review your setup carefully.")
            else:
                st.success(f"{selected_strategy} strategy is generally effective for you.")

    st.subheader("Trade Data Table")
    st.dataframe(df)

    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    st.download_button(
        label="Download CSV",
        data=buffer.getvalue(),
        file_name="smart_trading_journal.csv",
        mime="text/csv"
    )
else:
    st.info("No trades logged yet.")
