from flask import Flask, redirect, request
import stripe

from config import Config
from utils.producer import send_transaction


YOUR_DOMAIN = "http://localhost:5000"


def create_app():
    app = Flask(__name__, static_url_path="", static_folder="public")

    app.config.from_object(Config)
    stripe.api_key = app.config["STRIPE_API_KEY"]

    @app.route("/")
    def index():
        return redirect(YOUR_DOMAIN + "/checkout.html")

    @app.route("/create-checkout-session", methods=["POST"])
    def create_checkout_session():
        product = stripe.Product.create(
            name="Property A",
            description="Sample Crowdfounding Real-Estate Project",
            images=[
                "https://photos.zillowstatic.com/fp/132126196c6a59672475d40f033e6b35-uncropped_scaled_within_1536_1152.webp"
            ],
        )

        price = stripe.Price.create(
            product=product.id,
            unit_amount=1,  # in cents
            currency="usd",
        )

        try:
            deposit = float(request.form.get("deposit"))  # in usd
            quantity = int(deposit * 100)
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": price.id,
                        "quantity": quantity,
                    },
                ],
                mode="payment",
                success_url=YOUR_DOMAIN + "/payment?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=YOUR_DOMAIN + "/cancel.html",
            )

        except Exception as e:
            return str(e)

        return redirect(checkout_session.url, code=303)

    @app.route("/payment", methods=["GET"])
    def success():
        successful_session = request.args.get("session_id")
        if successful_session:
            session = stripe.checkout.Session.retrieve(successful_session)
            send_transaction(session)
            return redirect(YOUR_DOMAIN + "/success.html")
        else:
            return redirect(YOUR_DOMAIN + "/error.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
