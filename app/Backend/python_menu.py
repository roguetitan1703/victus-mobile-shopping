import mysql.connector
import uuid, random
from mysql.connector import Error
from datetime import datetime

from getpass import getpass

signed_in = False

class Connector():
    def __init__(self):
        pass

    @classmethod
    def connect_to_database():
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='e_commerce',
                user='root',
                password='Test@4321Sql'
            )
            if connection.is_connected():
                print("Connected to the database")
                return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    @classmethod
    def close_connection(connection):
        if connection.is_connected():
            connection.close()
            print("Connection closed")

class OnlineShopping():
    
    def __init__(self) -> None:
        pass
    
    def create_account(connection):
        print("Creating a new account...")
        customer_name = input("Enter your name: ")
        email = input("Enter your email: ")
        phone_number = input("Enter your phone number: ")
        password = getpass("Enter your password: ")

        # Generate a unique customer_id using UUID
        # customer_id = str(uuid.uuid4())[:4]
        customer_id = random.randint(0,999)

        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Customer (customer_id, customer_name, email, phone_number, password_hash) VALUES (%s, %s, %s, %s, %s)",
                        (customer_id, customer_name, email, phone_number, password))
            connection.commit()
            print("Account created successfully!")
        except Error as e:
            print(f"Error: {e}")

    def sign_in(connection):
        global signed_in
        print("Signing in...")
        email = input("Enter your email: ")
        password = getpass("Enter your password: ")

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Customer WHERE email = %s AND password_hash = %s", (email, password))
            customer = cursor.fetchone()

            if customer:
                print("Sign in successful!")
                signed_in = True
                return customer[0]  # Returning the customer_id
            else:
                print("Invalid email or password. Please try again.")
                return None
        except Error as e:
            print(f"Error: {e}")
            return None

    def logout():
        global signed_in
        signed_in = False
        print("Logged out successfully!")

    def browse_products(connection):
        print("Browsing products...")
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Product")
            products = cursor.fetchall()

            if products:
                for product in products:
                    print(f"{product[0]}. {product[1]} - Rs.{product[2]}")
            else:
                print("No products available.")
        except Error as e:
            print(f"Error: {e}")

    def add_to_cart(connection, customer_id):
        self.browse_products(connection)
        print("Adding item to cart...")
        product_id = input("Enter the product ID you want to add to your cart: ")
        quantity = input("Enter the quantity: ")

        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Cart (customer_id, product_id, quantity) VALUES (%s, %s, %s)",
                        (customer_id, product_id, quantity))
            connection.commit()
            print("Item added to cart successfully!")
        except Error as e:
            print(f"Error: {e}")


    def view_cart(connection, customer_id):
        print("Viewing cart...")
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT p.product_name, c.quantity, p.price FROM Cart c JOIN Product p ON c.product_id = p.product_id WHERE c.customer_id = %s",
                        (customer_id,))
            cart_items = cursor.fetchall()

            if cart_items:
                total_price = 0
                for item in cart_items:
                    total_price += item[1] * item[2]
                    print(f"{item[0]} - Quantity: {item[1]}, Price: Rs.{item[2]}")

                print(f"Total Price: Rs.{total_price}")
            else:
                print("Your cart is empty.")
        except Error as e:
            print(f"Error: {e}")

    def edit_cart(connection, customer_id):
        self.view_cart(connection, customer_id)
        print("Editing cart...")
        product_id = input("Enter the product ID you want to edit in your cart: ")
        new_quantity = input("Enter the new quantity: ")

        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE Cart SET quantity = %s WHERE customer_id = %s AND product_id = %s",
                        (new_quantity, customer_id, product_id))
            connection.commit()
            print("Cart edited successfully!")
        except Error as e:
            print(f"Error: {e}")


    def check_out(connection, customer_id, customer_name):
        print("Checking out...")
        try:
            cursor = connection.cursor()

            # Calculate total price
            cursor.execute("SELECT SUM(p.price * c.quantity) FROM Cart c JOIN Product p ON c.product_id = p.product_id WHERE c.customer_id = %s",
                        (customer_id,))
            total_price = cursor.fetchone()[0]

            # Clear the cart
            cursor.execute("DELETE FROM Cart WHERE customer_id = %s", (customer_id,))
            connection.commit()

            # Get current time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Print the bill
            print("\n********** Bill **********")
            print(f"Time: {current_time}")
            print(f"Customer Name: {customer_name}")

            # Retrieve products in the cart
            cursor.execute("SELECT p.product_name, c.quantity, p.price FROM Cart c JOIN Product p ON c.product_id = p.product_id WHERE c.customer_id = %s",
                        (customer_id,))
            products_in_cart = cursor.fetchall()

            for product in products_in_cart:
                product_name, quantity, price = product
                print(f"{product_name} x{quantity}: Rs.{price * quantity}")

            print(f"Total Price: Rs.{total_price}")
            print("Thank you for shopping with us!")
            print("********** End of Bill **********")

        except Error as e:
            print(f"Error: {e}")

def main():
    connection = Connector.connect_to_database()
    if connection is None:
        return

    customer_id = None

    while True:
        if signed_in:
            print("\nMenu:")
            print("1. Logout")
            print("2. Browse products")
            print("3. Add item to cart")
            print("4. Edit cart")
            print("5. View cart")
            print("6. Check out")
            print("7. Exit")
        else:
            print("\nMenu:")
            print("1. Create a new account")
            print("2. Sign in")
            print("3. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            if signed_in:
                logout()
            else:
                create_account(connection)
        elif choice == '2':
            if not signed_in:
                customer_id = sign_in(connection)
            else:
                browse_products(connection)
        elif choice == '3':
            if signed_in:
                add_to_cart(connection, customer_id)
            else:
                break
        elif choice == '4':
            if signed_in:
                edit_cart(connection, customer_id)
            else:
                break
        elif choice == '5':
            if signed_in:
                view_cart(connection, customer_id)
            else:
                break
        elif choice == '6':
            if signed_in:
                check_out(connection, customer_id, customer_name)
            else:
                break
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

    Connector.close_connection(connection)

if __name__ == "__main__":
    main()
