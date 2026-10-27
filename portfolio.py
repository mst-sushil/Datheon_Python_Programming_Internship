import csv
from os import name

def calculate_portfolio():
    print("=" * 60)
    print("      STOCK PORTFOLIO PERFORMANCE TRACKER      ")
    print("=" * 60)
    
    portfolio = []
    
    print("\nEnter your stock holdings. (Type 'DONE' when finished)\n")
    
    use_sample = input("Do you want to use sample portfolio data? (y/n): ").strip().lower()
    
    if use_sample == 'y':
        portfolio = [
            {"ticker": "AAPL", "buy_price": 150.0, "current_price": 185.5, "quantity": 10},
            {"ticker": "MSFT", "buy_price": 300.0, "current_price": 330.0, "quantity": 12},
            {"ticker": "GOOGL", "buy_price": 120.0, "current_price": 140.2, "quantity": 15},
            {"ticker": "AMZN", "buy_price": 130.0, "current_price": 145.0, "quantity": 20}
        ]
        print("\n✅ Sample portfolio loaded successfully!")
    else:
        while True:
            ticker = input("Enter Stock Ticker Symbol (e.g., AAPL, TSLA) or 'DONE': ").strip().upper()
            if ticker == 'DONE':
                break
            if not ticker:
                print("⚠️ Ticker cannot be empty.")
                continue
                
            try:
                buy_price = float(input(f"Enter Buy Price for {ticker}: "))
                current_price = float(input(f"Enter Current Market Price for {ticker}: "))
                quantity = int(input(f"Enter Share Quantity for {ticker}: "))
                
                if buy_price < 0 or current_price < 0 or quantity < 0:
                    print("⚠️ Values cannot be negative. Please re-enter.")
                    continue
                    
                portfolio.append({
                    "ticker": ticker,
                    "buy_price": buy_price,
                    "current_price": current_price,
                    "quantity": quantity
                })
                print(f"➕ Added {ticker} to portfolio.\n")
            except ValueError:
                print("⚠️ Invalid numeric input. Please enter valid numbers for price and quantity.")

    if not portfolio:
        print("❌ No portfolio data entered. Exiting program.")
        return

    # Calculations
    total_invested = 0
    total_current_value = 0
    
    for item in portfolio:
        item["invested_val"] = item["buy_price"] * item["quantity"]
        item["current_val"] = item["current_price"] * item["quantity"]
        item["gain_loss"] = item["current_val"] - item["invested_val"]
        item["gain_loss_pct"] = (item["gain_loss"] / item["invested_val"]) * 100 if item["invested_val"] > 0 else 0
        
        total_invested += item["invested_val"]
        total_current_value += item["current_val"]

    total_gain_loss = total_current_value - total_invested
    total_gain_loss_pct = (total_gain_loss / total_invested) * 100 if total_invested > 0 else 0

    # Display Results in Console
    print("\n" + "=" * 85)
    print(f"{'TICKER':<10} | {'QTY':<6} | {'BUY PRICE':<12} | {'CURR PRICE':<12} | {'INVESTED':<12} | {'VALUATION':<12} | {'GAIN/LOSS (%)':<15}")
    print("-" * 85)
    
    for item in portfolio:
        status_sign = "+" if item["gain_loss"] >= 0 else ""
        print(f"{item['ticker']:<10} | {item['quantity']:<6} | {item['buy_price']:<12.2f} | {item['current_price']:<12.2f} | {item['invested_val']:<12.2f} | {item['current_val']:<12.2f} | {status_sign}{item['gain_loss']:.2f} ({status_sign}{item['gain_loss_pct']:.2f}%)")
    
    print("-" * 85)
    print(f"Total Invested Capital  : {total_invested:.2f}")
    print(f"Total Current Valuation : {total_current_value:.2f}")
    overall_sign = "+" if total_gain_loss >= 0 else ""
    print(f"Overall Portfolio Return: {overall_sign}{total_gain_loss:.2f} ({overall_sign}{total_gain_loss_pct:.2f}%)")
    print("=" * 85)

    # Write results to 'pcsv_filename = "portfolio_summary.csv"
    try:
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
            fieldnames = ["Ticker", "Quantity", "Buy_Price", "Current_Price", "Invested_Value", "Current_Value", "Gain_Loss_Amount", "Gain_Loss_Percentage"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            writer.writeheader()
            for item in portfolio:
                writer.writerow({
                    "Ticker": item["ticker"],
                    "Quantity": item["quantity"],
                    "Buy_Price": f"{item['buy_price']:.2f}",
                    "Current_Price": f"{item['current_price']:.2f}",
                    "Invested_Value": f"{item['invested_val']:.2f}",
                    "Current_Value": f"{item['current_val']:.2f}",
                    "Gain_Loss_Amount": f"{item['gain_loss']:.2f}",
                    "Gain_Loss_Percentage": f"{item['gain_loss_pct']:.2f}%"
                })
        print(f"\n📁 Portfolio summary successfully exported to '{csv_filename}'!")
    except Exception as e:
        print(f"❌ Error writing to CSV file: {e}")

if __name__ == "__main__":
    calculate_portfolio()