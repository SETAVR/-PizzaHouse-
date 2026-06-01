import threading
import time

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import close_old_connections

from .models import Order


STATUS_FLOW = [
    Order.Status.COOKING,
    Order.Status.BAKING,
    Order.Status.DELIVERING,
    Order.Status.COMPLETED,
]


def send_order_status(order):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"order_{order.id}",
        {
            "type": "order.status",
            "status": order.status,
            "is_paid": order.is_paid,
        },
    )


def advance_order_statuses(order_id):
    close_old_connections()
    try:
        for status in STATUS_FLOW:
            time.sleep(4)
            order = Order.objects.get(pk=order_id)
            if order.status == Order.Status.COMPLETED:
                return
            order.status = status
            order.save(update_fields=["status", "updated_at"])
            send_order_status(order)
    finally:
        close_old_connections()


def start_order_status_thread(order_id):
    thread = threading.Thread(target=advance_order_statuses, args=(order_id,), daemon=True)
    thread.start()
