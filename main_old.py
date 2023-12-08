""""
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
        cursor.execute("INSERT INTO Customer (customer_name, email, phone_number, password_hash) VALUES (%s, %s, %s, %s)",
                       (customerName, email, phoneNumber, password))
        db.commit()
        return templates.TemplateResponse("index.html", {"request": request, "message": "Account created successfully!"})
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return templates.TemplateResponse("signup_page.html", {"request": request, "message": "Error creating account."})
    finally:
        cursor.close()

"""
