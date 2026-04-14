import argparse
import sys
from colorama import init, Fore, Style
from bot.client import test_connection
from bot.validators import validate_inputs
from bot.orders import place_order
from bot.logging_config import setup_logger

init(autoreset=True)
logger = setup_logger("cli")

def print_order_summary(symbol, side, order_type, quantity, price, stop_price=None):
    print(f"\n{Fore.CYAN}--- Order Request Summary ---")
    print(f"  Symbol    : {symbol}")
    print(f"  Side      : {side}")
    print(f"  Type      : {order_type}")
    print(f"  Quantity  : {quantity}")
    if price:
        print(f"  Price     : {price}")
    if stop_price:
        print(f"  Stop Price: {stop_price}")
    print(Style.RESET_ALL)

def print_order_response(response: dict):
    print(f"{Fore.GREEN}--- Order Response ---")
    print(f"  Order ID      : {response.get('orderId')}")
    print(f"  Status        : {response.get('status')}")
    print(f"  Executed Qty  : {response.get('executedQty')}")
    print(f"  Avg Price     : {response.get('avgPrice', 'N/A')}")
    print(f"  Symbol        : {response.get('symbol')}")
    print(Style.RESET_ALL)

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol",   required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side",     required=True, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--type",     required=True, choices=["MARKET", "LIMIT", "STOP"], dest="order_type", help="Order type")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price",      required=False, type=float, default=None, help="Limit price (required for LIMIT/STOP orders)")
    parser.add_argument("--stop-price", required=False, type=float, default=None, dest="stop_price", help="Stop trigger price (required for STOP orders)")

    args = parser.parse_args()

    # validate
    try:
        validate_inputs(args.symbol, args.side, args.order_type, args.quantity, args.price, args.stop_price)
    except ValueError as e:
        print(f"{Fore.RED}Validation failed:\n{e}")
        sys.exit(1)

    # connect
    try:
        if not test_connection():
            print(f"{Fore.RED}Could not connect to Binance Futures Testnet. Check your credentials.")
            sys.exit(1)
    except EnvironmentError as e:
        print(f"{Fore.RED}{e}")
        sys.exit(1)

    # print summary
    print_order_summary(args.symbol, args.side, args.order_type, args.quantity, args.price, args.stop_price)

    # place order
    try:
        response = place_order(args.symbol, args.side, args.order_type, args.quantity, args.price, args.stop_price)
        print_order_response(response)
        print(f"{Fore.GREEN}Order placed successfully.")
        logger.info(f"Order placed successfully: orderId={response.get('orderId')}, status={response.get('status')}")
    except Exception as e:
        print(f"{Fore.RED}Order failed: {e}")
        logger.error(f"Order failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
