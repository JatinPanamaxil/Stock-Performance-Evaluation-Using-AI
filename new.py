import yfinance as yf


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
        "52 Week Low": info.get("fiftyTwoWeekLow")
    }
 
def main():
    company_name = input("Enter the name of the company: ").strip()
    # You need to convert the company name to its ticker symbol.
    # This is a simplified approach. In practice, you might need a more
    # sophisticated method to find the correct ticker symbol.
    ticker_nse = f"{company_name}.NS"
    ticker_bse = f"{company_name}.BO"
 
    try:
        # Attempt to fetch data for NSE
        stock_info_nse = get_stock_info(ticker_nse)
        if stock_info_nse["Current Price"] is not None:
            print("NSE Data:", stock_info_nse)
        else:
            # Attempt to fetch data for BSE
            stock_info_bse = get_stock_info(ticker_bse)
            if stock_info_bse["Current Price"] is not None:
                print("BSE Data:", stock_info_bse)
            else:
                print("Company not found in NSE or BSE.")
    except Exception as e:
        print("An error occurred:", e)
 
if __name__ == "__main__":
    main()