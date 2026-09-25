from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "py-shop-dev-secret"

PRODUCTS = [
    {
        "id": 1,
        "name": "Aura Wireless Headphones",
        "price": 89.00,
        "category": "Audio",
        "image": "headphones.png",
        "description": "Over-ear Bluetooth headphones with deep bass, 30-hour battery, and a folding travel case.",
    },
    {
        "id": 2,
        "name": "Pulse Smartwatch",
        "price": 129.00,
        "category": "Wearables",
        "image": "watch.png",
        "description": "Fitness tracking, heart-rate monitor, sleep insights, and a bright always-on display.",
    },
    {
        "id": 3,
        "name": "Nomad Laptop Backpack",
        "price": 64.00,
        "category": "Bags",
        "image": "backpack.png",
        "description": "Water-resistant 16-inch backpack with padded laptop sleeve and USB charging port.",
    },
    {
        "id": 4,
        "name": "BrewHome Coffee Maker",
        "price": 79.00,
        "category": "Home",
        "image": "coffee.png",
        "description": "Programmable 12-cup drip coffee maker with a thermal carafe and auto shut-off.",
    },
    {
        "id": 5,
        "name": "Lumen Desk Lamp",
        "price": 42.00,
        "category": "Home",
        "image": "lamp.png",
        "description": "LED desk lamp with three color temperatures, USB charging, and a flexible neck.",
    },
    {
        "id": 6,
        "name": "Stride Running Shoes",
        "price": 96.00,
        "category": "Fashion",
        "image": "shoes.png",
        "description": "Lightweight everyday runners with cushioned soles and breathable mesh uppers.",
    },
    {
        "id": 7,
        "name": "Studio Ceramic Mug",
        "price": 18.00,
        "category": "Home",
        "image": "mug.png",
        "description": "Handmade 12 oz ceramic mug. Microwave and dishwasher safe.",
    },
    {
        "id": 8,
        "name": "Wave Mini Speaker",
        "price": 54.00,
        "category": "Audio",
        "image": "speaker.png",
        "description": "Portable Bluetooth speaker with 12-hour playtime and splash-resistant body.",
    },
]


def get_product(product_id):
    return next((p for p in PRODUCTS if p["id"] == product_id), None)


def cart_items():
    cart = session.get("cart", {})
    items = []
    total = 0.0
    for pid, qty in cart.items():
        product = get_product(int(pid))
        if not product:
            continue
        line = qty * product["price"]
        total += line
        items.append({"product": product, "qty": qty, "line_total": line})
    return items, total


def cart_count():
    return sum(session.get("cart", {}).values())


@app.context_processor
def inject_cart_count():
    return {"cart_count": cart_count()}


@app.route("/")
def index():
    query = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "").strip()
    products = PRODUCTS
    if query:
        products = [p for p in products if query in p["name"].lower() or query in p["description"].lower()]
    if category:
        products = [p for p in products if p["category"] == category]
    categories = sorted({p["category"] for p in PRODUCTS})
    return render_template(
        "index.html",
        products=products,
        categories=categories,
        query=query,
        active_category=category,
    )


@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = get_product(product_id)
    if not product:
        flash("Product not found.")
        return redirect(url_for("index"))
    related = [p for p in PRODUCTS if p["category"] == product["category"] and p["id"] != product["id"]][:3]
    return render_template("product.html", product=product, related=related)


@app.route("/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = get_product(product_id)
    if not product:
        flash("Product not found.")
        return redirect(url_for("index"))
    qty = max(1, min(10, int(request.form.get("qty", 1))))
    cart = session.get("cart", {})
    key = str(product_id)
    cart[key] = cart.get(key, 0) + qty
    session["cart"] = cart
    flash(f"Added {product['name']} to your cart.")
    return redirect(request.referrer or url_for("index"))


@app.route("/cart")
def cart():
    items, total = cart_items()
    return render_template("cart.html", items=items, total=total)


@app.route("/update/<int:product_id>", methods=["POST"])
def update_cart(product_id):
    cart = session.get("cart", {})
    key = str(product_id)
    qty = int(request.form.get("qty", 1))
    if qty <= 0:
        cart.pop(key, None)
    else:
        cart[key] = min(10, qty)
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    cart.pop(str(product_id), None)
    session["cart"] = cart
    flash("Item removed.")
    return redirect(url_for("cart"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total = cart_items()
    if not items:
        flash("Your cart is empty.")
        return redirect(url_for("index"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()
        if not (name and email and address):
            flash("Please fill in all fields.")
            return render_template("checkout.html", items=items, total=total)
        session["cart"] = {}
        return render_template("success.html", name=name, total=total)
    return render_template("checkout.html", items=items, total=total)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
