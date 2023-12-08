create database mit_mobile_shopping;

use mit_mobile_shopping;

-- Create Customer Table
CREATE TABLE Customer (
    customerId INT PRIMARY KEY,
    customerName VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phoneNumber VARCHAR(20) NOT NULL,
    passwordHash VARCHAR(255) NOT NULL
);

-- Create Seller Table
CREATE TABLE Seller (
    sellerId INT PRIMARY KEY,
    sellerName VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phoneNumber VARCHAR(20) NOT NULL,
    passwordHash VARCHAR(255) NOT NULL
);

-- Create Product Table
CREATE TABLE Product (
    productId INT PRIMARY KEY,
    productName VARCHAR(255) NOT NULL,
    productBrand VARCHAR(255), -- New column: productBrand
    price DECIMAL(10, 2) NOT NULL,
    productImage VARCHAR(255), -- New column: productImage
    sellerId INT,
    FOREIGN KEY (sellerId) REFERENCES Seller(sellerId)
);

-- Create Cart Table
CREATE TABLE Cart (
    customerId INT,
    productId INT,
    quantity INT,
    PRIMARY KEY (customerId, productId),
    FOREIGN KEY (customerId) REFERENCES Customer(customerId),
    FOREIGN KEY (productId) REFERENCES Product(productId)
);


-- INSERT DATA
-- Insert Data into Seller Table
INSERT INTO `Seller` (`sellerId`, `sellerName`, `email`, `phoneNumber`, `passwordHash`)
VALUES
(1, 'Samsung', 'samsungphones@samsung.com', '+919876543210', 'samsung@123'),
(2, 'Redmi', 'redmiphones@xiaomi.com', '+919876543211', 'redmi@123'),
(3, 'Apple', 'applephones@apple.com', '+919876543212', 'apple@123');

-- Insert Data into Product Table
INSERT INTO product (productId, productName, productBrand, price, productImage, sellerId)
VALUES
    (8, 'Redmi Note 10', 'Redmi', 13999.00, '../static/assets/products/8.png', 1),
    (9, 'Samsung Galaxy S6', 'Samsung', 24990.00, '../static/assets/products/1.png', 1),
    (2, 'Redmi Note 7', 'Redmi', 11999.00, '../static/assets/products/2.png', 1),
    (4, 'Redmi Note 5', 'Redmi', 11990.00, '../static/assets/products/4.png', 1),
    (5, 'Redmi Note 4', 'Redmi', 9990.00, '../static/assets/products/5.png', 1),
    (10, 'Samsung Galaxy S7', 'Samsung', 35500.00, '../static/assets/products/10.png', 1),
    (11, 'Apple iPhone 5', 'Apple', 25000.00, '../static/assets/products/11.png', 1),
    (12, 'Apple iPhone 6', 'Apple', 34900.00, '../static/assets/products/12.png', 1),
    (13, 'Apple iPhone 7', 'Apple', 42900.00, '../static/assets/products/13.png', 1),
    (1, 'Samsung Galaxy 10', 'Samsung', 29999.00, '../static/assets/products/1.png', 1),
    (6, 'Redmi Note 8', 'Redmi', 12999.00, '../static/assets/products/6.png', 1),
    (7, 'Redmi Note 9', 'Redmi', 12999.00, '../static/assets/products/3.png', 1),
    (14, 'Apple iPhone 10', 'Apple', 89000.00, '/static/assets/products/14.png', 1),
    (15, 'Redmi Note 10 pro', 'Redmi', 17999.00, '/static/assets/products/15.png', 1);


DELIMITER //

CREATE TRIGGER customer_id_auto_increment
BEFORE INSERT ON Customer
FOR EACH ROW
BEGIN
  DECLARE next_customer_id INT;

  SELECT IFNULL(MAX(customerId), 0) + 1 INTO next_customer_id;

  SET NEW.customerId = next_customer_id;
END;

//

DELIMITER ;

DELIMITER //

CREATE FUNCTION cart_total(customerId INT)
RETURNS DECIMAL(10, 2)
NO SQL
BEGIN
  DECLARE total DECIMAL(10, 2) DEFAULT 0;

  SELECT SUM(p.price * c.quantity) INTO total
  FROM Cart c
  JOIN Product p ON c.productId = p.productId
  WHERE c.customerId = customerId;

  RETURN total;
END;

//

DELIMITER ;


DELIMITER //

CREATE FUNCTION cart_total_qty(customerId INT)
RETURNS INT
NO SQL
BEGIN
  DECLARE total_qty INT DEFAULT 0;

  SELECT SUM(c.quantity) INTO total_qty
  FROM Cart c
  JOIN Product p ON c.productId = p.productId
  WHERE c.customerId = customerId;

  RETURN total_qty;
END;

//

DELIMITER ;

