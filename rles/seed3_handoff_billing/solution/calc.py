from decimal import Decimal, ROUND_HALF_UP


def _validate_rates(tax_rate, discount_rate, shipping):
    tax = Decimal(str(tax_rate))
    discount = Decimal(str(discount_rate))
    shipping_amount = Decimal(str(shipping))
    if not tax.is_finite() or tax < 0 or tax > 1:
        raise ValueError("tax_rate must be between zero and one")
    if not discount.is_finite() or discount < 0 or discount > 1:
        raise ValueError("discount_rate must be between zero and one")
    if not shipping_amount.is_finite() or shipping_amount < 0:
        raise ValueError("shipping must be nonnegative")
    return tax, discount, shipping_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _calculate_lines(items, discount):
    lines = []
    subtotal = Decimal("0.00")
    taxable_subtotal = Decimal("0.00")
    for item in items:
        sku = item["sku"]
        quantity = item["quantity"]
        price = Decimal(str(item["unit_price"]))
        if not isinstance(sku, str) or not sku:
            raise ValueError("sku must be a nonempty string")
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("quantity must be a positive integer")
        if not price.is_finite() or price < 0:
            raise ValueError("unit_price must be nonnegative")
        taxable = bool(item.get("taxable", True))
        gross = (price * quantity).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        reduction = (gross * discount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        net = gross - reduction
        subtotal += net
        if taxable:
            taxable_subtotal += net
        lines.append({"sku": sku, "quantity": quantity, "gross": format(gross, ".2f"),
                      "discount": format(reduction, ".2f"), "net": format(net, ".2f"), "taxable": taxable})
    return lines, subtotal, taxable_subtotal


def compute_invoice(items, tax_rate="0", discount_rate="0", shipping="0"):
    """Calculate an invoice without modifying the supplied items."""
    tax, discount, shipping_amount = _validate_rates(tax_rate, discount_rate, shipping)
    lines, subtotal, taxable_subtotal = _calculate_lines(items, discount)
    tax_amount = (taxable_subtotal * tax).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    total = subtotal + tax_amount + shipping_amount
    return {
        "lines": lines,
        "subtotal": format(subtotal, ".2f"),
        "taxable_subtotal": format(taxable_subtotal, ".2f"),
        "tax": format(tax_amount, ".2f"),
        "shipping": format(shipping_amount, ".2f"),
        "total": format(total, ".2f"),
        "currency": "USD",
    }
