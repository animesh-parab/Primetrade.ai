from flask import Flask, render_template, request, jsonify
from bot.client import test_connection
from bot.validators import validate_inputs
from bot.orders import place_order
from bot.logging_config import setup_logger

app = Flask(__name__)
logger = setup_logger("ui")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/order", methods=["POST"])
def order():
    data = request.json
    symbol     = data.get("symbol", "").strip()
    side       = data.get("side", "").strip()
    order_type = data.get("order_type", "").strip()
    quantity   = data.get("quantity")
    price      = data.get("price") or None
    stop_price = data.get("stop_price") or None

    try:
        quantity = float(quantity)
        price = float(price) if price else None
        stop_price = float(stop_price) if stop_price else None
    except (TypeError, ValueError):
        return jsonify({"success": False, "error": "Invalid quantity or price values."})

    try:
        validate_inputs(symbol, side, order_type, quantity, price, stop_price)
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)})

    if not test_connection():
        return jsonify({"success": False, "error": "Could not connect to Binance Futures Demo."})

    try:
        response = place_order(symbol, side, order_type, quantity, price, stop_price)
        logger.info(f"UI order placed: orderId={response.get('orderId')}, status={response.get('status')}")
        return jsonify({"success": True, "data": response})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
