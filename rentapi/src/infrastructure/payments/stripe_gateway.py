"""Module containing Stripe gateway implementation."""

import stripe

from src.config import config


class StripeGateway:
    """A class representing Stripe gateway."""

    def __init__(self):
        """The initializer of the `Stripe gateway`."""
        stripe.api_key = config.STRIPE_SECRET_KEY

    async def create_payment_intent(
            self,
            amount: float,
            currency: str = "pln"
    ) -> dict | None:
        """The method creating payment intent in Stripe.

        Args:
            amount (float): The amount to pay.
            currency (str, optional): The currency of the payment. Defaults to "usd".

        Returns:
            dict | None: The payment intent details.
        """
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),
                currency=currency,
                payment_method_types=["card"],
            )
            return intent
        except Exception as e:
            print(f"Error creating payment intent: {e}")
            return None

    async def confirm_payment(self, intent_id: str) -> bool:
        """The method confirming payment in Stripe.

        Args:
            intent_id (str): The id of the payment intent.

        Returns:
            bool: True if payment is confirmed.
        """
        try:
            stripe.PaymentIntent.confirm(
                intent_id,
                payment_method="pm_card_visa",
            )
            return True
        except Exception as e:
            print(f"Error confirming payment: {e}")
            return False
