from PyQt6.QtWidgets import QMessageBox, QLineEdit
from model.inventory_data import check_order_validity


def handle_order_submission(view):
    # Extract the entries (SKU and quantity) from the view
    entries = get_entries(view)

    # If no entries are found, show a warning message and exit
    if not entries:
        show_custom_message(
            view,
            "Invalid Input",
            "Please enter at least one valid SKU and quantity.",
            icon=QMessageBox.Icon.Warning
        )
        return

    # Validate SKUs and quantities using the model logic
    errors, valid_entries = check_order_validity(entries)
    if errors:
        # If validation failed, show an error message with the issues
        show_custom_message(
            view,
            "Order Validation Failed",
            "\n".join(errors),
            icon=QMessageBox.Icon.Critical
        )
        return

    # Check for high quantity entries (>= 100) and ask for user confirmation
    high_quantity_entries = [(sku, qty) for sku, qty in valid_entries if qty >= 100]
    if high_quantity_entries:
        # Prepare the message text for high quantity items
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

    # Confirm final order details with the user before proceeding
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

    # Clear form inputs after successful submission
    clear_entries(view)


def get_entries(view):
    """
    Extracts SKU and quantity entries from the view, returning a list of valid entries.
    """
    entries = []
    # Loop through each entry frame in the scroll layout
    for i in range(view.scroll_layout.count()):
        entry_frame = view.scroll_layout.itemAt(i).widget()
        if not entry_frame:
            continue

        # Find all QLineEdit fields (expecting SKU and quantity)
        line_edits = entry_frame.findChildren(QLineEdit)
        if len(line_edits) >= 2:
            sku = line_edits[0].text().strip()
            qty_text = line_edits[1].text().strip()

            # Only add the entry if SKU is filled and quantity is a valid number
            if sku and qty_text.isdigit():
                entries.append((sku, int(qty_text)))

    return entries


def clear_entries(view):
    """
    Clears all entries in the form, except for the first one.
    Resets the input fields in the first entry frame.
    """
    # Remove all entries except the first one
    for i in reversed(range(1, view.scroll_layout.count())):
        widget = view.scroll_layout.itemAt(i).widget()
        if widget:
            widget.setParent(None)

    # Clear the input fields in the first entry (if any)
    first_widget = view.scroll_layout.itemAt(0).widget()
    if first_widget:
        line_edits = first_widget.findChildren(QLineEdit)
        for le in line_edits:
            le.clear()


def show_custom_message(parent, title, text, icon=QMessageBox.Icon.Information, buttons=QMessageBox.StandardButton.Ok):
    """
    Utility function to display a styled message box with the specified parameters.
    """
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
