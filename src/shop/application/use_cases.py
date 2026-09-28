from shop.domain.entities import OrderLineRequest, PaymentMethod


class PlaceOrder:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, *, customer_name, phone, address, city, notes, payment_method, cart):
        if not customer_name.strip() or not phone.strip():
            raise ValueError("Informe seu nome e telefone para recebermos o pedido.")
        try:
            method = PaymentMethod(payment_method)
        except ValueError as error:
            raise ValueError("Escolha uma forma de pagamento válida.") from error

        lines = []
        for product_id, quantity in cart.items():
            try:
                product_id = int(product_id)
                quantity = int(quantity)
            except (TypeError, ValueError) as error:
                raise ValueError("Seu carrinho contém um item inválido.") from error
            if quantity < 1 or quantity > 20:
                raise ValueError("A quantidade deve estar entre 1 e 20 unidades.")
            lines.append(OrderLineRequest(product_id=product_id, quantity=quantity))

        if not lines:
            raise ValueError("Adicione ao menos um item antes de enviar o pedido.")

        return self.repository.place_order(
            customer_name=customer_name.strip(),
            phone=phone.strip(),
            address=address.strip(),
            city=city.strip(),
            notes=notes.strip(),
            payment_method=method,
            lines=lines,
        )