---

# 🛒 VICTUS Mobile Shopping

## 📝 Description

MIT Mobile Shopping is an e-commerce platform for purchasing electronic products. It provides features for browsing products, adding them to a cart, and generating PDF invoices upon checkout. The application is built using FastAPI for the backend and MySQL for the database, with HTML templates rendered using Jinja2. Additionally, it utilizes Bootstrap for front-end styling and Owl Carousel for product carousels.

## 🌟 Features

- **User Authentication:** Users can register, log in, and log out securely.
- **Browse Products:** View a list of available electronic products.
- **Add to Cart:** Add products to a shopping cart for later purchase.
- **Checkout:** Generate a PDF invoice for the items in the cart and clear the cart upon checkout.
- **Static File Serving:** Serve static files such as images and CSS for a seamless user experience.
- **Database Integration:** Interact with a MySQL database to store user data, product information, and cart contents.
- **PDF Generation:** Utilize ReportLab to dynamically generate PDF invoices with detailed product information.
- **Frontend Styling:** Enhance the user interface with Bootstrap for responsive design and Owl Carousel for product carousels.

## 💻 Technologies Used

- **Backend:** FastAPI (Python)
- **Database:** MySQL
- **HTML Templating:** Jinja2Templates
- **PDF Generation:** ReportLab
- **Frontend:** HTML, CSS, Bootstrap, Owl Carousel

## 🛠️ Setup Instructions

1. Clone the repository to your local machine.
2. Install the necessary dependencies using `pip install -r requirements.txt`.
3. Set up a MySQL database and configure the connection in the backend code.
4. Run the backend server using `uvicorn app:app --reload`.
5. Access the application through your web browser.

## 🚀 Usage

1. **Register/Login:** Create a new account or log in with existing credentials.
2. **Browse Products:** View the list of available electronic products.
3. **Add to Cart:** Add products to the cart by clicking the "Add to Cart" button.
4. **View Cart:** Click on the cart icon to view the items added to the cart.
5. **Checkout:** Proceed to checkout to generate a PDF invoice for the items in the cart.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---
