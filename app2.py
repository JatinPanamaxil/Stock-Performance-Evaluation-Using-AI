import streamlit as st
import yfinance as yf
from openai import OpenAI
import google.generativeai as genai
import os
import pandas as pd

# Set the page to fullscreen
st.set_page_config(
    page_title="Stock Trend Predictor",
    page_icon="📈",
    layout="wide"
)


client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
gemini_api_key = os.environ["GEMINI_API_KEY"]
genai.configure(api_key = gemini_api_key)

# Create columns with different widths for your layout
col1, col2 = st.columns([4, 5])
company_name = ""


def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "Current Price": info.get("currentPrice"),
        "Today's Opening Price": info.get("open"),
        "Previous Closing Price": info.get("previousClose"),
        "Today's High": info.get("dayHigh"),
        "Today's Low": info.get("dayLow"),
        "52 Week High": info.get("fiftyTwoWeekHigh"),
        "52 Week Low": info.get("fiftyTwoWeekLow"),
        "Dividend Yield": info.get("dividendYield"),
        "Market Cap": info.get("marketCap"),
        "Volume": info.get("volume"),
        "Average Volume": info.get("averageVolume"),
        "P/E Ratio": info.get("trailingPE"),
        "Forward P/E Ratio": info.get("forwardPE"),
        "Earnings Per Share (EPS)": info.get("trailingEps"),
        "Earnings Date": info.get("earningsDate"),
        "Dividend Rate": info.get("dividendRate"),
        "Beta": info.get("beta"),
        "Trailing Annual Dividend Rate": info.get("trailingAnnualDividendRate"),
        "Trailing Annual Dividend Yield": info.get("trailingAnnualDividendYield"),
        "Float Shares": info.get("floatShares")
    }

def display_stock_info(stock_info, exchange):
    col1.subheader(f"Stock Information for {company_name} on {exchange}")
    # Convert the stock_info dictionary to a Pandas DataFrame
    df = pd.DataFrame(list(stock_info.items()), columns=["Metric", "Value"])
    col1.table(df)


def run_gemini(prompt):
    response = gemini_model.generate_content(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    with col2.chat_message("assistant"):
        col2.markdown(response.text)


def main():
    global company_name
    
    col1.title("Stock Information")
    company_name = col1.text_input("Enter the name of the company:")
    ticker_nse = f"{company_name}.NS"
    ticker_bse = f"{company_name}.BO"

    if col1.button("Get Stock Information"):
        try:
            stock_info_nse = get_stock_info(ticker_nse)
            if stock_info_nse["Current Price"] is not None:
                display_stock_info(stock_info_nse, "NSE")
                # Construct the dynamic prompt
                prompt = f"How has the stock been performing recently, considering its current price at {stock_info_nse['Current Price']}, today's opening price at {stock_info_nse['Today\'s Opening Price']}, and the previous closing price at {stock_info_nse['Previous Closing Price']}? Additionally, what are the 52-week high and low values ({stock_info_nse['52 Week High']} and {stock_info_nse['52 Week Low']}), and how do these relate to the current state of the stock? Provide insights into the dividend yield ({stock_info_nse['Dividend Yield']}), market cap ({stock_info_nse['Market Cap']}), and volume traded today ({stock_info_nse['Volume']}). How does the P/E ratio ({stock_info_nse['P/E Ratio']}) and forward P/E ratio ({stock_info_nse['Forward P/E Ratio']}) indicate the stock's valuation? Consider the earnings per share (EPS) at {stock_info_nse['Earnings Per Share (EPS)']} and the upcoming earnings date ({stock_info_nse['Earnings Date']}). Lastly, explore factors such as the dividend rate ({stock_info_nse['Dividend Rate']}), beta ({stock_info_nse['Beta']}), trailing annual dividend rate ({stock_info_nse['Trailing Annual Dividend Rate']}), trailing annual dividend yield ({stock_info_nse['Trailing Annual Dividend Yield']}), and float shares ({stock_info_nse['Float Shares']}). Based on these variables, what predictions can you make about the stock's future performance?"
            else:
                stock_info_bse = get_stock_info(ticker_bse)
                if stock_info_bse["Current Price"] is not None:
                    display_stock_info(stock_info_bse, "BSE")
                    # Construct the dynamic prompt
                    prompt = f"How has the stock been performing recently, considering its current price at {stock_info_bse['Current Price']}, today's opening price at {stock_info_bse['Today\'s Opening Price']}, and the previous closing price at {stock_info_bse['Previous Closing Price']}? Additionally, what are the 52-week high and low values ({stock_info_bse['52 Week High']} and {stock_info_bse['52 Week Low']}), and how do these relate to the current state of the stock? Provide insights into the dividend yield ({stock_info_bse['Dividend Yield']}), market cap ({stock_info_bse['Market Cap']}), and volume traded today ({stock_info_bse['Volume']}). How does the P/E ratio ({stock_info_bse['P/E Ratio']}) and forward P/E ratio ({stock_info_bse['Forward P/E Ratio']}) indicate the stock's valuation? Consider the earnings per share (EPS) at {stock_info_bse['Earnings Per Share (EPS)']} and the upcoming earnings date ({stock_info_bse['Earnings Date']}). Lastly, explore factors such as the dividend rate ({stock_info_bse['Dividend Rate']}), beta ({stock_info_bse['Beta']}), trailing annual dividend rate ({stock_info_bse['Trailing Annual Dividend Rate']}), trailing annual dividend yield ({stock_info_bse['Trailing Annual Dividend Yield']}), and float shares ({stock_info_bse['Float Shares']}). Based on these variables, what predictions can you make about the stock's future performance?"
                else:
                    col1.write(f"Company {company_name} not found in NSE or BSE.")
                    return
        except Exception as e:
            col1.write("An error occurred:", e)
            return

        col2.subheader("Stock Performance Evaluation Using AI")
        
        
        
        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "gpt-3.5-turbo"

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with col2.chat_message(message["role"]):
                col2.markdown(message["content"])

        st.session_state.messages.append({"role": "user", "content": prompt})
        with col2.chat_message("user"):
            col2.markdown(prompt)

        with col2.chat_message("assistant"):
            message_placeholder = col2.empty()
            full_response = ""
            for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

# Create the Gemini Model
        gemini_model = genai.GenerativeModel('gemini-pro')

        st.subheader("Stock Performance Evaluation Using AI")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # User input
        # prompt = st.text_input("Ask something:")

        if prompt:

            # Generate response using Gemini
            response = gemini_model.generate_content(
                [message["content"] for message in st.session_state.messages]
            )

            # Display assistant's response
            with st.chat_message("assistant"):
                st.markdown(response.text)
        
if __name__ == "__main__":
    main()
