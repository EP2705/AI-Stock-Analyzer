from dotenv import load_dotenv
import streamlit as st
import yfinance
from datetime import date
from ai_agent import get_ai_response
import matplotlib.pyplot as plt

today = date.today().strftime("%Y-%m-%d")

def get_stock_data(ticker):
    data = yfinance.download(ticker, start="2022-01-01", end=today)
    return data

def plot_stock_data(data,ticker):
    data['SMA50'] = data['Close'].rolling(window=50).mean()
    data['SMA200'] = data['Close'].rolling(window=200).mean()
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(data.index, data['Close'], label='Close Price', color='blue')
    ax.plot(data.index, data['SMA50'], label='50-Day SMA', color='orange')
    ax.plot(data.index, data['SMA200'], label='200-Day SMA', color='green')

    ax.set_title(f'{ticker} Stock Price with Moving Averages', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price (USD)', fontsize=12)
    ax.legend()
    ax.grid(True)

    return fig

def main():
    
    st.title("AI Financial Research Assistant")

    if 'ticker' not in st.session_state:
        st.session_state.ticker = ""

    st.header("Enter a Stock Ticker")
    ticker_input = st.text_input("Enter a Stock Ticker (ex AAPL, MSFT, GOOGL)", key="ticker_input")
    
    if st.button("Get Stock Analysis"):
        if ticker_input:
            st.session_state.ticker = ticker_input
        else:
            st.warning("Please enter a stock ticker.")
            st.session_state.ticker = ""


    if st.session_state.ticker:
        st.header(f"Analysis for: {st.session_state.ticker}")
        
        with st.spinner(f"Getting data for {st.session_state.ticker}..."):
            stock_data = get_stock_data(st.session_state.ticker)
        
        if stock_data.empty:
            st.error("Error: No data found for this ticker")
            st.session_state.ticker = ""
        else:
            st.subheader("Recent Data")
            st.write(stock_data.tail())
            
            st.subheader("Stock Price Chart")
            figure = plot_stock_data(stock_data, st.session_state.ticker)
            st.pyplot(figure)
            
            st.subheader("Ask AI Assistant")
            user_question = st.text_input("Ask a Question", key="user_question")
            
            if st.button("Ask AI"):
                if user_question:
                    with st.spinner("AI is thinking..."):
                        prompt = f"Regarding {st.session_state.ticker}, {user_question}"
                        ai_response = get_ai_response(prompt)
                        st.markdown(ai_response)
                else:
                    st.warning("Please enter a question.")


if __name__ == "__main__":
    main()