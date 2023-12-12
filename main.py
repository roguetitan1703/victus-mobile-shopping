from fastapi import FastAPI, Request, Depends, Form, HTTPException, status, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import mysql.connector
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
import tempfile

app = FastAPI()
customerId = 1

# Database Configuration
DATABASE_URL = "mysql+mysqlconnector://root:Test@4321Sql@localhost/mit_mobile_shopping"

# Mount static files and configure templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Create tables in the database
def get_db_connection():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Test@4321Sql",
        database="mit_mobile_shopping"
    )
    return db

async def startup_event():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Test@4321Sql",
        database="mit_mobile_shopping"
    )

    db.cursor().execute("""
        CREATE TABLE IF NOT EXISTS Customer (
            customerId INT PRIMARY KEY AUTO_INCREMENT,
            customerName VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            phoneNumber VARCHAR(15) NOT NULL,
            passwordHash VARCHAR(255) NOT NULL
        )
    """)

    db.close()

async def shutdown_event():
    # Close the database connection when the application shuts down
    app.state.db.close()

app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

def get_db():
    db = get_db_connection()
    try:
        yield db
    finally:
        db.close()

@app.get('/test', response_class=HTMLResponse)
async def test(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})

@app.get('/test2', response_class=HTMLResponse)
async def test2(request: Request):
    return templates.TemplateResponse("test2.html", {"request": request})

@app.get('/index/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/cart', response_class=HTMLResponse)
async def cart(request: Request, db: mysql.connector.MySQLConnection = Depends(get_db)):

    # Fetch cart items for the current customer from the database
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT Product.productId, productName, productBrand, price, productImage, quantity "
                   "FROM Cart "
                   "JOIN Product ON Cart.productId = Product.productId "
                   "WHERE customerId = %s", (customerId,))
    cart_items = cursor.fetchall()

    # Calculate the total using the cart_total function
    cursor.execute("SELECT cart_total(%s) AS total", (customerId,))
    total_result = cursor.fetchone()
    total = total_result['total'] if total_result else 0
    
    # Calculate the total_qty using the cart_total_qty function
    cursor.execute("SELECT cart_total_qty(%s) AS total_qty", (customerId,))
    total_result = cursor.fetchone()
    total_qty = total_result['total_qty'] if total_result else 0

    return templates.TemplateResponse("cart.html", {"request": request, "cart_items": cart_items, "total": total, "total_qty": total_qty})



@app.get("/checkout")
async def checkout(db: mysql.connector.MySQLConnection = Depends(get_db)):
    try:
            
        # Fetch cart items for the current customer from the database
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT Product.productName, Product.price, Cart.quantity, (Product.price * Cart.quantity) AS amount "
                    "FROM Cart "
                    "JOIN Product ON Cart.productId = Product.productId "
                    "WHERE customerId = %s", (customerId,))
        cart_items = cursor.fetchall()

        # Fetch customer information for the current customer
        cursor.execute("SELECT customerName, phoneNumber FROM Customer WHERE customerId = %s", (customerId,))
        customer_info = cursor.fetchone()

        # Calculate the total using the cart_total function
        cursor.execute("SELECT cart_total(%s) AS total", (customerId,))
        total_result = cursor.fetchone()
        total = total_result['total'] if total_result else 0

        # Create a PDF bill
        pdf_buffer = BytesIO()
        p = canvas.Canvas(pdf_buffer)

        # Add header
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 800, "MIT Mobile Shopping - Invoice")
        p.line(100, 795, 500, 795)  # horizontal line under the header

        # Add customer information
        p.setFont("Helvetica", 12)
        p.drawString(100, 770, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Check if customer information is available
        if customer_info:
            customer_name = customer_info['customerName']
            customer_phone = customer_info['phoneNumber']
            p.drawString(100, 750, f"Customer Name: {customer_name}")
            p.drawString(100, 730, f"Customer Phone: {customer_phone}")

        # Add item details
        p.drawString(100, 700, "Item Name")
        p.drawString(250, 700, "Price")
        p.drawString(350, 700, "Quantity")
        p.drawString(450, 700, "Amount")
        p.line(100, 695, 500, 695)  # horizontal line under item details

        y_position = 680
        for item in cart_items:
            y_position -= 20
            p.drawString(100, y_position, item['productName'])
            p.drawString(250, y_position, str(item['price']))
            p.drawString(350, y_position, str(item['quantity']))
            p.drawString(450, y_position, str(item['amount']))

        # Add total
        p.line(100, y_position - 5, 500, y_position - 5)  # horizontal line above total
        p.drawString(350, y_position - 20, "Total:")
        p.drawString(450, y_position - 20, str(total))

        p.save()

        # Reset buffer position
        pdf_buffer.seek(0)

        # Delete cart items for the current customer
        cursor.execute("DELETE FROM Cart WHERE customerId = %s", (customerId,))
        db.commit()
            
        # Save the PDF to a file (optional)
        # with open("bill.pdf", "wb") as f:
        #     f.write(pdf_buffer.read())
        
        # Save the PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(pdf_buffer.getvalue())

        # Return the PDF as a response
        return FileResponse(temp_file.name, filename="bill.pdf", media_type="application/pdf")
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        cursor.close()


@app.get('/login_page', response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login_page.html", {"request": request})

@app.get('/signup_page', response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signup_page.html", {"request": request})


@app.post("/signup", response_class=HTMLResponse)
async def signup(request: Request, db: mysql.connector.MySQLConnection = Depends(get_db),
                 customerName: str = Form(...), email: str = Form(...),
                 phoneNumber: str = Form(...), password: str = Form(...)):
    cursor = db.cursor()
    try:
        # Ensure the email is unique before creating the account
        cursor.execute("SELECT * FROM Customer WHERE email = %s", (email,))
        existing_customer = cursor.fetchone()
        if existing_customer:
            return templates.TemplateResponse("signup_page.html", {"request": request, "message": "Email already exists."})

        # Create a new customer account
        cursor.execute("INSERT INTO Customer (customerName, email, phoneNumber, passwordHash) VALUES (%s, %s, %s, %s)",
                       (customerName, email, phoneNumber, password))
        db.commit()
        return templates.TemplateResponse("index.html", {"request": request, "message": "Account created successfully!"})
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return templates.TemplateResponse("signup_page.html", {"request": request, "message": "Error creating account."})
    finally:
        cursor.close()

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, db: mysql.connector.MySQLConnection = Depends(get_db),
                email: str = Form(...),
                password: str = Form(...)):
    cursor = db.cursor()
    try:
        # Fetch customer information using the provided ID and password
        cursor.execute("SELECT * FROM Customer WHERE email = %s AND passwordHash = %s", (email, password))
        customer = cursor.fetchone()

        if customer:
            # Save customer ID in the global variable
            global customerId
            customerId = customer[0]
            print(f"Customer Id: {customerId}")
            return templates.TemplateResponse("index.html", {"request": request, "message": "Login successful!"})
        else:
            return templates.TemplateResponse("index.html", {"request": request, "message": "Invalid ID or password."})
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return templates.TemplateResponse("index.html", {"request": request, "message": "Error during login."})
    finally:
        cursor.close()
        
        
@app.post("/addtocart", response_class=JSONResponse)
async def add_to_cart(request: Request, db: mysql.connector.MySQLConnection = Depends(get_db)):

    # Parse JSON data from the request body
    data = await request.json()
    
    # Extract productId from the parsed JSON data
    productId = data.get("productId")
    # print(f"Customer Id: {customerId}")

    # Check if the product exists
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Product WHERE productId = %s", (productId,))
    product = cursor.fetchone()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        # Check if the product is already in the cart
        cursor.execute("SELECT * FROM Cart WHERE customerId = %s AND productId = %s", (customerId, productId))
        existing_item = cursor.fetchone()

        if existing_item:
            # If the product is already in the cart, update the quantity
            cursor.execute("UPDATE Cart SET quantity = quantity + 1 WHERE customerId = %s AND productId = %s",
                           (customerId, productId))
        else:
            # If the product is not in the cart, add a new entry
            cursor.execute("INSERT INTO Cart (customerId, productId, quantity) VALUES (%s, %s, %s)",
                           (customerId, productId, 1))

        db.commit()
        return {"status": "success", "message": "Product added to cart"}
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return {"status": "error", "message": "Error adding product to cart"}
    finally:
        cursor.close()