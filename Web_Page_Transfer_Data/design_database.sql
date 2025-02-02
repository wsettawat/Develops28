create database abc_telephone_network;

use abc_telephone_network;

-- customers table
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    
    -- Address
    address VARCHAR(255),
    subdistrict VARCHAR(100),
    district VARCHAR(100),
    province VARCHAR(100),
    country varchar(100),
    zipcode VARCHAR(10),
    
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

desc customers;

select * from customers;

-- packages table
create table packages (
	package_id int auto_increment primary key,
	package_name VARCHAR(100) NOT NULL,
    monthly_fee DECIMAL(10,2) NOT NULL,
    call_minutes INT NOT NULL,
    data_quota_gb DECIMAL(5,2) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
    
desc packages;

-- subscriptions table
CREATE TABLE subscriptions (
    subscription_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    package_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    
    -- Foreign Keys
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (package_id) REFERENCES packages(package_id) ON DELETE CASCADE
);

desc subscriptions;

-- Customer’s Subscription Details
SELECT c.first_name, c.last_name, p.package_name, p.monthly_fee, s.start_date, s.end_date
FROM subscriptions s
JOIN customers c ON s.customer_id = c.customer_id
JOIN packages p ON s.package_id = p.package_id
WHERE c.customer_id = 1;

-- 2.1 รายงานลูกค้าใหม่แต่ละวัน
SELECT DATE(created_at)  as registration_date, COUNT(customer_id) AS new_customers
FROM customers
GROUP BY DATE(created_at)
ORDER BY registration_date DESC;

-- 2.2 รายงานประวัติการสมัครใช้บริการของลูกค้าแต่ละคน ในแต่ละวัน
select 
	c.customer_id,
    c.first_name,
    c.last_name,
    c.phone_number,
    c.email,
    s.start_date as subscription_date,
    p.package_name,
    p.monthly_fee
from subscriptions s
join customers c on s.customer_id = c.customer_id
join packages p on  s.package_id  = p.package_id
order by s.start_date desc, c.customer_id desc; -- asc = low to high


INSERT INTO packages (package_name, monthly_fee, call_minutes, data_quota_gb, description)
VALUES 
    ('5G Next Speed', 599, 300, 20, 'Fastest 5G plan with 20GB high-speed data and call 300 mins.'),
    ('Ultra Max', 999, 500, 50, 'Unlimited calls with 50GB high-speed data and call 150 mins.'),
    ('Basic Plan', 399, 200, 10, 'Affordable plan with 10GB high-speed data and call 1000 mins.');

-- Verify that the packages are inserted
SELECT * FROM packages;


SELECT * FROM customers;

SELECT * FROM subscriptions;
