import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from decimal import Decimal

def get_order_details(order_id):
    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",       # Your database host
        user="root",            # Your database username
        password="Karthik@2003",  # Your database password
        database="pandeyji_eatery"  # Your database name
    )
    cursor = conn.cursor(dictionary=True)
    
    # Fetch order details from the orders and food_items tables
    query = """
    SELECT o.order_id, f.name AS item_name, o.quantity, o.total_price
    FROM orders o
    JOIN food_items f ON o.item_id = f.item_id
    WHERE o.order_id = %s
    """
    cursor.execute(query, (order_id,))
    items = cursor.fetchall()
    
    conn.close()
    
    if items:
        return {"order_id": order_id, "items": items}
    else:
        return None

def generate_bill_pdf(order_id, file_name="bill.pdf"):
    # Fetch order details from the database
    order_details = get_order_details(order_id)
    
    if not order_details:
        print(f"No order found with ID {order_id}")
        return
    
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter
    
    # Draw the header with company name
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, height - 30, "FOODY HELPER")
    
    # Draw the order ID
    c.setFont("Helvetica", 12)
    c.drawString(30, height - 60, f"Order ID: {order_details['order_id']}")
    
    # Draw table headers
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, height - 100, "ITEMS ORDERED")
    c.drawString(200, height - 100, "QUANTITY")
    c.drawString(300, height - 100, "PRICE")
    
    # Draw items
    c.setFont("Helvetica", 10)
    y = height - 120
    sum = Decimal('0')
    for item in order_details['items']:
        c.drawString(30, y, item['item_name'])
        c.drawString(200, y, str(item['quantity']))
        c.drawString(300, y, f"${item['total_price']:.2f}")
        sum += item['total_price']
        y -= 20
    # c.setFont("Helvetica-Bold", 10)


    # Draw the grand total
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, y - 20, "GRAND TOTAL")

    c.drawString(300, y - 20, f"${sum:.2f}")
    
    # Save the PDF
    c.save()
    print(f"Bill generated successfully: {file_name}")

# Example usage
# generate_bill_pdf(59)
