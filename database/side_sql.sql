
-- Trigger to update product quantity in the cart after a purchase
CREATE TRIGGER update_cart_quantity
AFTER INSERT ON OrderDetails
FOR EACH RO
-- Trigger to update product quantity in the cart after a purchase
CREATE TRIGGER update_cart_quantity
AFTER INSERT ON OrderDetails
FOR EACH ROW
BEGIN
    UPDATE Cart
    SET quantity = quantity - NEW.quantity
    WHERE customer_id = NEW.customer_id AND product_id = NEW.product_id;
END; 

-- Procedure to add a product to the cart
DELIMITER //
CREATE PROCEDURE AddToCart(IN cust_id INT, IN prod_id INT, IN qty INT)
BEGIN
    INSERT INTO Cart(customer_id, product_id, quantity)
    VALUES (cust_id, prod_id, qty);
END;
//
DELIMITER ;

-- Function to calculate the total price of items in the cart for a customer
CREATE FUNCTION CalculateTotal(IN cust_id INT)
RETURNS DECIMAL(10, 2)
BEGIN
    DECLARE total DECIMAL(10, 2);
    SELECT SUM(p.price * c.quantity) INTO total
    FROM Cart c
    JOIN Product p ON c.product_id = p.product_id
    WHERE c.customer_id = cust_id;
    RETURN total;
END;

-- Sample Query to retrieve products in a customer's cart
SELECT p.product_name, c.quantity, p.price
FROM Cart c
JOIN Product p ON c.product_id = p.product_id
WHERE c.customer_id = 1;

SELECT s.seller_name
FROM Cart c
JOIN Product p ON c.product_id = p.product_id
JOIN Seller s ON p.seller_id = s.seller_id
WHERE c.customer_id = 1;

SELECT p.product_name, c.quantity
FROM Cart c
JOIN Product p ON c.product_id = p.product_id
WHERE c.customer_id = 1;

SELECT DISTINCT cu.customer_name
FROM Cart ca
JOIN Customer cu ON ca.customer_id = cu.customer_id
WHERE ca.product_id = 1;

SELECT s.seller_name, SUM(p.price * od.quantity) AS total_sales
FROM OrderDetails od
JOIN Product p ON od.product_id = p.product_id
JOIN Seller s ON p.seller_id = s.seller_id
GROUP BY s.seller_name;
W
BEGIN
    UPDATE Cart
    SET quantity = quantity - NEW.quantity
    WHERE customer_id = NEW.customer_id AND product_id = NEW.product_id;
END; 

-- Procedure to add a product to the cart
DELIMITER //
CREATE PROCEDURE AddToCart(IN cust_id INT, IN prod_id INT, IN qty INT)
BEGIN
    INSERT INTO Cart(customer_id, product_id, quantity)
    VALUES (cust_id, prod_id, qty);
END;
//
DELIMITER ;

-- Function to calculate the total price of items in the cart for a customer
CREATE FUNCTION CalculateTotal(IN cust_id INT)
RETURNS DECIMAL(10, 2)
BEGIN
    DECLARE total DECIMAL(10, 2);
    SELECT SUM(p.price * c.quantity) INTO total
    FROM Cart c
    JOIN Product p ON c.product_id = p.product_id
    WHERE c.customer_id = cust_id;
    RETURN total;
END;

-- Sample Query to retrieve products in a customer's cart
SELECT p.product_name, c.quantity, p.price
FROM Cart c
JOIN Product p ON c.product_id = p.product_id
WHERE c.customer_id = 1;

SELECT s.seller_name
FROM Cart c
JOIN Product p ON c.product_id = p.product_id
JOIN Seller s ON p.seller_id = s.seller_id
WHERE c.customer_id = 1;

SELECT p.product_name, c.quantity
FROM Cart c
JOIN Product p ON c.product_id = p.product_id
WHERE c.customer_id = 1;

SELECT DISTINCT cu.customer_name
FROM Cart ca
JOIN Customer cu ON ca.customer_id = cu.customer_id
WHERE ca.product_id = 1;

SELECT s.seller_name, SUM(p.price * od.quantity) AS total_sales
FROM OrderDetails od
JOIN Product p ON od.product_id = p.product_id
JOIN Seller s ON p.seller_id = s.seller_id
GROUP BY s.seller_name;
