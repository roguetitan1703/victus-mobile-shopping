use e_commerce;

DELIMITER //
CREATE PROCEDURE InsertSellers()
BEGIN
    -- Add 15 Sellers (Companies) to the Seller Table with Indian Phone Numbers
    INSERT INTO Seller (seller_id, seller_name, email, phone_number, password_hash)
    VALUES
        (1, 'TechGiant Corp', 'techgiant@techgiant.com', '+911234567890', 'techgiantpassword'),
        (2, 'ElectroTech Solutions', 'electrotech@electrotech.com', '+911234567891', 'electrotechpassword'),
        (3, 'Innovate Electronics Ltd.', 'innovate@innovate.com', '+911234567892', 'innovatepassword'),
        (4, 'FutureDevices Inc.', 'futuredevices@futuredevices.com', '+911234567893', 'futuredevicespassword'),
        (5, 'SmartTech Innovations', 'smarttech@smarttech.com', '+911234567894', 'smarttechpassword'),
        (6, 'Digital Dynamics Co.', 'digitaldynamics@digitaldynamics.com', '+911234567895', 'digitaldynamicspassword'),
        (7, 'TechSavvy Solutions', 'techsavvy@techsavvy.com', '+911234567896', 'techsavvypassword'),
        (8, 'Infinite Innovations Ltd.', 'infinite@infinite.com', '+911234567897', 'infinitepassword'),
        (9, 'TechMarvel Corp', 'techmarvel@techmarvel.com', '+911234567898', 'techmarvelpassword'),
        (10, 'Epic Electronics Enterprises', 'epicelectronics@epicelectronics.com', '+911234567899', 'epicelectronicspassword'),
        (11, 'FutureTech Innovations', 'futuretech@futuretech.com', '+911234567890', 'futuretechpassword'),
        (12, 'Quantum Electronics Inc.', 'quantumelectronics@quantumelectronics.com', '+911234567891', 'quantumelectronicspassword'),
        (13, 'InnoTech Solutions', 'innotech@innotech.com', '+911234567892', 'innotechpassword'),
        (14, 'Visionary Tech Co.', 'visionarytech@visionarytech.com', '+911234567893', 'visionarytechpassword'),
        (15, 'Global Electronics Group', 'globalelectronics@globalelectronics.com', '+911234567894', 'globalelectronicspassword');
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE InsertProducts()
BEGIN
    -- Add 50 Products to the Product Table Linked to the 15 Sellers (Electronics Category)
    -- Prices are in Indian Rupees (INR)
    INSERT INTO Product (product_id, product_name, price, seller_id)
    VALUES
        (1, 'Smartphone X1', 24999.00, 1),
        (2, 'Smartwatch Pro', 7499.00, 2),
        (3, 'Laptop UltraBook', 39999.00, 3),
        (4, 'Wireless Earbuds', 2499.00, 4),
        (5, 'Portable Bluetooth Speaker', 1499.00, 5),
        (6, 'Smart Home Security Camera', 3999.00, 6),
        (7, 'Gaming Laptop', 54999.00, 7),
        (8, 'Fitness Tracker', 1999.00, 8),
        (9, '3D Printer', 19999.00, 9),
        (10, 'Curved Gaming Monitor', 32999.00, 10),
        (11, 'Robot Vacuum Cleaner', 8999.00, 11),
        (12, 'High-Performance Graphics Card', 31999.00, 12),
        (13, 'Smart Refrigerator', 29999.00, 13),
        (14, 'Home Theater System', 14999.00, 14),
        (15, 'Wireless Charging Pad', 999.00, 15);
        (16, 'Smart LED TV', 44999.00, 1),
        (17, 'Bluetooth Wireless Headphones', 2999.00, 2),
        (18, 'Digital Camera with 4K Video', 15999.00, 3),
        (19, 'Smart Thermostat', 3499.00, 4),
        (20, 'Gaming Console', 27999.00, 5),
        (21, 'Wireless Mouse and Keyboard Combo', 1499.00, 6),
        (22, 'Solar-Powered Phone Charger', 999.00, 7),
        (23, 'Smart Coffee Maker', 4499.00, 8),
        (24, 'Wireless Gaming Mouse', 1999.00, 9),
        (25, 'Bluetooth Car Kit', 1299.00, 10),
        (26, 'VR Headset for Mobile Phones', 3499.00, 11),
        (27, 'Portable External Hard Drive', 5999.00, 12),
        (28, 'Wireless Desktop Printer', 8999.00, 13),
        (29, 'Home Security System', 18999.00, 14),
        (30, 'Smart Doorbell with Camera', 3499.00, 15);
END //

DELIMITER ;

CALL InsertProducts();
