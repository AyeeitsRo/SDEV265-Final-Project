from PyQt6.QtWidgets import QMessageBox, QLineEdit
from model.inventory_data import check_order_validity


def handle_order_submission(view):
    entries = get_entries(view)

    if not entries:
        show_custom_message(
            view,
            "Invalid Input",
            "Please enter at least one valid SKU and quantity.",
            icon=QMessageBox.Icon.Warning
        )
        return

    # Validate SKUs and quantities
    errors, valid_entries = check_order_validity(entries)
    if errors:
        show_custom_message(
            view,
            "Order Validation Failed",
            "\n".join(errors),
            icon=QMessageBox.Icon.Critical
        )
        return

    # Confirm high quantity entries
    high_quantity_entries = [(sku, qty) for sku, qty in valid_entries if qty >= 100]
    if high_quantity_entries:
        high_qty_text = "\n".join([f"{sku}: {qty}" for sku, qty in high_quantity_entries])
        confirm = show_custom_message(
            view,
            "High Quantity Confirmation",
            f"These SKUs have a quantity of 100 or more:\n\n{high_qty_text}\n\nProceed?",
            icon=QMessageBox.Icon.Question,
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

    # Final confirmation
    order_summary = "\n".join([f"{sku}: {qty}" for sku, qty in valid_entries])
    confirm = show_custom_message(
        view,
        "Confirm Order",
        f"Do you want to place this order?\n\n{order_summary}",
        icon=QMessageBox.Icon.Question,
        buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    if confirm != QMessageBox.StandardButton.Yes:
        return

    clear_entries(view)


def get_entries(view):
    entries = []
    for i in range(view.scroll_layout.count()):
        entry_frame = view.scroll_layout.itemAt(i).widget()
        if not entry_frame:
            continue
        line_edits = entry_frame.findChildren(QLineEdit)
        if len(line_edits) >= 2:
            sku = line_edits[0].text().strip()
            qty_text = line_edits[1].text().strip()
            if sku and qty_text.isdigit():
                entries.append((sku, int(qty_text)))
    return entries


def clear_entries(view):
    for i in reversed(range(1, view.scroll_layout.count())):
        widget = view.scroll_layout.itemAt(i).widget()
        if widget:
            widget.setParent(None)

    first_widget = view.scroll_layout.itemAt(0).widget()
    if first_widget:
        line_edits = first_widget.findChildren(QLineEdit)
        for le in line_edits:
            le.clear()


def show_custom_message(parent, title, text, icon=QMessageBox.Icon.Information, buttons=QMessageBox.StandardButton.Ok):
    msg = QMessageBox(parent)
    msg.setIcon(icon)
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setStandardButtons(buttons)
    msg.setStyleSheet("""
        QLabel {
            color: black;
            font-family: 'Roboto';
            font-size: 14px;
        }
        QPushButton {
            color: black;
            font-family: 'Roboto';
            font-size: 13px;
        }
    """)
    return msg.exec()
