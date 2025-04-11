import frappe
from frappe.utils import now
from frappe import _

# apps/salesforce_custom/salesforce_custom/create_so.py

import frappe
import json

@frappe.whitelist(allow_guest=True)
def create_sales_order(**kwargs):
    sales_order_name = kwargs.get("sales_order")  # Optional: For updating
    customer = kwargs.get("customer")
    transaction_date = kwargs.get("transaction_date")
    items = kwargs.get("items", [])
    price_list = kwargs.get("price_list") or "Standard Selling"
    default_warehouse = kwargs.get("default_warehouse") or "Stores - EGSPL"

    if sales_order_name:
        # Try to fetch existing sales order
        try:
            so = frappe.get_doc("Sales Order", sales_order_name)
            so.items = []  # Clear existing items before appending new ones
        except frappe.DoesNotExistError:
            # If not found, create new
            so = frappe.new_doc("Sales Order")
            so.name = sales_order_name  # Optional: Set provided name
    else:
        so = frappe.new_doc("Sales Order")

    so.customer = customer
    so.transaction_date = transaction_date
    so.selling_price_list = price_list

    for item in items:
        qty = float(item.get("qty", 0))
        rate = float(item.get("rate", 0))
        if qty == 0 or rate == 0:
            frappe.throw(f"Item {item.get('item_code')} must have both qty and rate greater than 0")

        so.append("items", {
            "item_code": item["item_code"],
            "qty": qty,
            "rate": rate,
            "delivery_date": item.get("delivery_date") or transaction_date,
            "warehouse": item.get("warehouse") or default_warehouse
        })

    if so.get("name"):
        so.save()
    else:
        so.insert()

    return {
        "message": "Sales Order updated" if sales_order_name else "Sales Order created",
        "sales_order": so.name
    }



# @frappe.whitelist(allow_guest=True)
# def create_sales_order(**kwargs):
#     customer = kwargs.get("customer")
#     transaction_date = kwargs.get("transaction_date")
#     items = kwargs.get("items", [])
#     default_warehouse = kwargs.get("default_warehouse") or "Finished Goods - EGSPL"  # Replace with actual warehouse name

#     so = frappe.new_doc("Sales Order")
#     so.customer = customer
#     so.transaction_date = transaction_date

#     for item in items:
#         so.append("items", {
#             "item_code": item["item_code"],
#             "qty": item["qty"],
#             "rate": item["rate"],
#             "delivery_date": item.get("delivery_date") or transaction_date,
#             "warehouse": item.get("warehouse") or default_warehouse
#         })

#     so.insert()
#     # so.submit()

#     return {"message": "Sales Order created", "sales_order": so.name}


# import frappe

# @frappe.whitelist()
# def create_sales_order():
#     # your actual logic here
#     return {"message": "Sales Order Created"}
