-- Create database
CREATE DATABASE pandeyji_eatery

-- Switch to the database (in pgAdmin you can just select it from the dropdown)
\c pandeyji_eatery;

-- ========================
-- Table: food_items
-- ========================
DROP TABLE IF EXISTS food_items CASCADE;
CREATE TABLE food_items (
  item_id INT PRIMARY KEY,
  name VARCHAR(255),
  price NUMERIC(10,2)
);

INSERT INTO food_items (item_id, name, price) VALUES
(1,'Pav Bhaji',6.00),
(2,'Chole Bhature',7.00),
(3,'Pizza',8.00),
(4,'Mango Lassi',5.00),
(5,'Masala Dosa',6.00),
(6,'Vegetable Biryani',9.00),
(7,'Vada Pav',4.00),
(8,'Rava Dosa',7.00),
(9,'Samosa',5.00);

-- ========================
-- Table: order_tracking
-- ========================
DROP TABLE IF EXISTS order_tracking CASCADE;
CREATE TABLE order_tracking (
  order_id INT PRIMARY KEY,
  status VARCHAR(255)
);

INSERT INTO order_tracking (order_id, status) VALUES
(40,'delivered'),
(41,'in transit');

-- ========================
-- Table: orders
-- ========================
DROP TABLE IF EXISTS orders CASCADE;
CREATE TABLE orders (
  order_id INT,
  item_id INT,
  quantity INT,
  total_price NUMERIC(10,2),
  PRIMARY KEY (order_id, item_id),
  CONSTRAINT fk_orders_food FOREIGN KEY (item_id) REFERENCES food_items(item_id)
);

INSERT INTO orders (order_id, item_id, quantity, total_price) VALUES
(40,1,2,12.00),
(40,3,1,8.00),
(41,4,3,15.00),
(41,6,2,18.00),
(41,9,4,20.00);

-- ========================
-- Function: get_price_for_item
-- ========================
DROP FUNCTION IF EXISTS get_price_for_item(VARCHAR);
CREATE OR REPLACE FUNCTION get_price_for_item(p_item_name VARCHAR)
RETURNS NUMERIC(10,2)
LANGUAGE plpgsql
AS $$
DECLARE
    v_price NUMERIC(10,2);
BEGIN
    SELECT price INTO v_price
    FROM food_items
    WHERE name = p_item_name;

    IF FOUND THEN
        RETURN v_price;
    ELSE
        RETURN -1;
    END IF;
END;
$$;

-- ========================
-- Function: get_total_order_price
-- ========================
DROP FUNCTION IF EXISTS get_total_order_price(INT);
CREATE OR REPLACE FUNCTION get_total_order_price(p_order_id INT)
RETURNS NUMERIC(10,2)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total_price NUMERIC(10,2);
BEGIN
    SELECT SUM(total_price) INTO v_total_price
    FROM orders
    WHERE order_id = p_order_id;

    IF FOUND THEN
        RETURN v_total_price;
    ELSE
        RETURN -1;
    END IF;
END;
$$;

-- ========================
-- Procedure: insert_order_item
-- ========================
DROP PROCEDURE IF EXISTS insert_order_item;
CREATE OR REPLACE PROCEDURE insert_order_item(
    p_food_item VARCHAR,
    p_quantity INT,
    p_order_id INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_item_id INT;
    v_price NUMERIC(10,2);
    v_total_price NUMERIC(10,2);
BEGIN
    SELECT item_id INTO v_item_id FROM food_items WHERE name = p_food_item;
    v_price := get_price_for_item(p_food_item);

    IF v_price = -1 THEN
        RAISE NOTICE 'Invalid food item: %', p_food_item;
        RETURN;
    END IF;

    v_total_price := v_price * p_quantity;

    INSERT INTO orders (order_id, item_id, quantity, total_price)
    VALUES (p_order_id, v_item_id, p_quantity, v_total_price);
END;
$$;
