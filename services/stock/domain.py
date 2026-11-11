from errors import Rejected
from sqlite_store import transaction

STOCK = {"TEE": 10, "MUG": 6}


def operation(data, _):
    order, sku, quantity = data["orderId"], data["sku"], data["quantity"]
    if not isinstance(order, str) or not order.strip() or sku not in STOCK or type(quantity) is not int or quantity < 1:
        raise ValueError("Expected order ID, known SKU and positive integer quantity")
    with transaction() as db:
        db.execute("CREATE TABLE IF NOT EXISTS hold (id TEXT PRIMARY KEY, sku TEXT, quantity INTEGER, remaining INTEGER)")
        previous = db.execute("SELECT sku,quantity,remaining FROM hold WHERE id=?", (order,)).fetchone()
        if previous:
            if previous[:2] != (sku, quantity):
                raise Rejected(409, "Order ID already used for a different hold")
            return {"reserved": quantity, "remaining": previous[2], "replayed": True}
        taken = db.execute("SELECT COALESCE(SUM(quantity),0) FROM hold WHERE sku=?", (sku,)).fetchone()[0]
        remaining = STOCK[sku] - taken - quantity
        if remaining < 0:
            raise Rejected(409, "Insufficient stock")
        db.execute("INSERT INTO hold VALUES (?, ?, ?, ?)", (order, sku, quantity, remaining))
    return {"reserved": quantity, "remaining": remaining, "replayed": False}
