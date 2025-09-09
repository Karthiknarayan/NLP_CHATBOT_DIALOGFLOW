import psycopg2
from psycopg2 import sql, Error
from configs.settings import MainSettings
settings = MainSettings()
global cnx

cnx = psycopg2.connect(
host= settings.host,
user= settings.user,
password= settings.password,
dbname= settings.dbname
)

def insert_order_item(food_item, quantity, order_id):
    try:
        with cnx.cursor() as cursor:
            cursor.callproc('insert_order_item', (food_item, quantity, order_id))
            cnx.commit()
        print("Order item inserted successfully!")
        return 1
    except psycopg2.Error as err:
        print(f"Error inserting order item: {err}")
        cnx.rollback()
        return -1
    except Exception as e:
        print(f"An error occurred: {e}")
        cnx.rollback()
        return -1

def insert_order_tracking(order_id, status):
    try:
        with cnx.cursor() as cursor:
            insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
            cursor.execute(insert_query, (order_id, status))
            cnx.commit()
    except psycopg2.Error as err:
        print(f"Error inserting order tracking: {err}")
        cnx.rollback()
    except Exception as e:
        print(f"An error occurred: {e}")
        cnx.rollback()

def get_total_order_price(order_id):
    try:
        with cnx.cursor() as cursor:
            query = "SELECT get_total_order_price(%s)"
            cursor.execute(query, (order_id,))
            result = cursor.fetchone()[0]
        return result
    except psycopg2.Error as err:
        print(f"Error fetching total order price: {err}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_next_order_id():
    try:
        with cnx.cursor() as cursor:
            query = "SELECT MAX(order_id) FROM orders"
            cursor.execute(query)
            result = cursor.fetchone()[0]
        return 1 if result is None else result + 1
    except psycopg2.Error as err:
        print(f"Error fetching next order ID: {err}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_order_status(order_id):
    try:
        with cnx.cursor() as cursor:
            query = "SELECT status FROM order_tracking WHERE order_id = %s"
            cursor.execute(query, (order_id,))
            result = cursor.fetchone()
        return result[0] if result else None
    except psycopg2.Error as err:
        print(f"Error fetching order status: {err}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def update_order_status(order_id):
    try:
        current_status = get_order_status(order_id)
        if not current_status:
            print(f"No status found for order_id {order_id}")
            return -1
        
        new_status = None
        if current_status == "in progress":
            new_status = "in transit"
        elif current_status == "in transit":
            new_status = "delivered"
        
        if new_status:
            with cnx.cursor() as cursor:
                update_query = "UPDATE order_tracking SET status = %s WHERE order_id = %s"
                cursor.execute(update_query, (new_status, order_id))
                cnx.commit()
            print(f"Order status updated to '{new_status}'")
            return 1
        else:
            print(f"No update required for status '{current_status}'")
            return 0
    except psycopg2.Error as err:
        print(f"Error updating order status: {err}")
        cnx.rollback()
        return -1
    except Exception as e:
        print(f"An error occurred: {e}")
        cnx.rollback()
        return -1

if __name__ == "__main__":
    # Test functions
    print(get_next_order_id())
    # insert_order_item('Samosa', 3, 99)
    # insert_order_item('Pav Bhaji', 1, 99)
    # insert_order_tracking(99, "in progress")
    # print(get_total_order_price(56))
    # print(get_order_status(99))
    # update_order_status(99)
