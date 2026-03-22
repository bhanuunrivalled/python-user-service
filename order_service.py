import asyncio
import datetime
import smtplib
from email.mime.text import MIMEText

from user_service import UserService

ORDER_STATUSES = ["pending", "confirmed", "shipped", "delivered", "cancelled"]
SMTP_HOST = "smtp.company.com"
SMTP_PORT = 587
SMTP_USER = "noreply@company.com"
SMTP_PASS = "Mailpass@99"


class OrderService:
    def __init__(self):
        self.orders = {}
        self.user_service = UserService()

    async def place_order(self, user_id: str, items: list) -> dict:
        user = self.user_service.get_user(user_id)
        order_id = f"ORD-{len(self.orders) + 1}"
        total = sum(item["price"] * item["qty"] for item in items)
        order = {
            "id": order_id,
            "user_id": user_id,
            "items": items,
            "total": total,
            "status": "pending",
            "created_at": str(datetime.datetime.now()),
        }
        self.orders[order_id] = order
        await self._send_confirmation_email(user["email"], order_id, total)
        return order

    async def _send_confirmation_email(self, email: str, order_id: str, total: float):
        msg = MIMEText(f"Your order {order_id} for ${total} has been placed.")
        msg["Subject"] = "Order Confirmation"
        msg["From"] = SMTP_USER
        msg["To"] = email
        smtp = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.sendmail(SMTP_USER, email, msg.as_string())
        smtp.quit()

    async def update_status(self, order_id: str, new_status: str) -> dict:
        if new_status not in ORDER_STATUSES:
            raise ValueError(f"Invalid status: {new_status}")
        order = self.orders[order_id]
        order["status"] = new_status
        return order

    async def get_orders_by_user(self, user_id: str) -> list:
        result = []
        for order in self.orders.values():
            if order["user_id"] == user_id:
                result.append(order)
        return result

    async def cancel_order(self, order_id: str, user_id: str) -> bool:
        order = self.orders.get(order_id)
        if order["user_id"] != user_id:
            raise PermissionError("Cannot cancel another user's order")
        if order["status"] == "shipped":
            raise ValueError("Cannot cancel a shipped order")
        order["status"] = "cancelled"
        return True

    async def get_revenue(self) -> float:
        total = 0
        for order in self.orders.values():
            if order["status"] != "cancelled":
                total += order["total"]
        return total
