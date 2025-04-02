import pytest
from main import Product, Cart, PaymentGateway

# Test jednostkowy: Testowanie funkcji Cart.calculate_total()
def test_cart_calculate_total():
    cart = Cart()
    product1 = Product("Mouse", 50)
    product2 = Product("Keyboard", 80)
    cart.add_product(product1, 1)
    cart.add_product(product2, 1)
    assert cart.calculate_total() == 130

# Test jednostkowy: Testowanie klasy Product
def test_product():
    product = Product("Laptop", 1000)
    assert product.name == "Laptop"
    assert product.price == 1000

    with pytest.raises(ValueError):
        Product("Phone", -500)

# Test jednostkowy: Testowanie dodawania wielu produktów do koszyka
def test_cart_add_multiple_products():
    cart = Cart()
    cart.add_product(Product("Pen", 5), 3)
    cart.add_product(Product("Notebook", 15), 2)
    assert cart.calculate_total() == 45

# Test jednostkowy: Testowanie klasy PaymentGateway
def test_payment_gateway_process_payment():
    assert PaymentGateway.process_payment(100) == True

    with pytest.raises(ValueError):
        PaymentGateway.process_payment(0)

# Test integracyjny: Testowanie przepływu płatności
def test_payment_flow():
    cart = Cart()
    cart.add_product(Product("Phone", 500), 1)
    cart.add_product(Product("Case", 20), 2)
    total = cart.calculate_total()

    assert PaymentGateway.process_payment(total) == True

# Test jednostkowy: Testowanie dodawania produktów do koszyka i błędów w koszyku
def test_cart_items():
    cart = Cart()
    product = Product("Book", 20)
    cart.add_product(product, 2)
    assert len(cart.items) == 1

    with pytest.raises(ValueError):
        cart.add_product(product, 0)