from flask import Flask, request, render_template, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# ✅ MySQL Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "2803",  # Change to your actual MySQL password
    "database": "abc_telephone_network"
}

# ✅ Route: Display Subscription Form (Frontend UI)
@app.route('/')
def home():
    return render_template('form.html')

# ✅ Route: Handle Form Submission (Register Customer & Subscription via Web Form)
@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Get form data from UI
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        phone_number = request.form['phone_number']
        email = request.form['email']
        address = request.form['address']
        subdistrict = request.form['subdistrict']
        district = request.form['district']
        province = request.form['province']
        country = request.form['country']
        zipcode = request.form['zipcode']
        package_id = request.form['package_id']

        # ✅ Connect to MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # ✅ Insert customer data into `customers` table
        customer_sql = """
            INSERT INTO customers 
            (first_name, last_name, date_of_birth, phone_number, email, 
             address, subdistrict, district, province, country, zipcode) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        customer_values = (first_name, last_name, date_of_birth, phone_number, email, 
                           address, subdistrict, district, province, country, zipcode)

        cursor.execute(customer_sql, customer_values)
        customer_id = cursor.lastrowid  # Get the newly inserted customer ID

        # ✅ Insert subscription data into `subscriptions` table
        subscription_sql = """
            INSERT INTO subscriptions (customer_id, package_id, start_date, end_date) 
            VALUES (%s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 30 DAY))
        """
        subscription_values = (customer_id, package_id)
        cursor.execute(subscription_sql, subscription_values)

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('home'))

    except Exception as e:
        return jsonify({"error": str(e)})

# ✅ Route: Add New Customer & Subscription via API (POST)
@app.route('/add_customer', methods=['POST'])
def add_customer():
    try:
        data = request.get_json()

        # Extract customer details from JSON
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        date_of_birth = data.get('date_of_birth')
        phone_number = data.get('phone_number')
        email = data.get('email')
        address = data.get('address')
        subdistrict = data.get('subdistrict')
        district = data.get('district')
        province = data.get('province')
        country = data.get('country')
        zipcode = data.get('zipcode')
        package_id = data.get('package_id')

        # ✅ Validate Required Fields
        if not (first_name and last_name and phone_number and package_id):
            return jsonify({"error": "Missing required fields"}), 400

        # ✅ Connect to MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # ✅ Insert customer into `customers` table
        customer_sql = """
            INSERT INTO customers 
            (first_name, last_name, date_of_birth, phone_number, email, 
             address, subdistrict, district, province, country, zipcode) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        customer_values = (first_name, last_name, date_of_birth, phone_number, email, 
                           address, subdistrict, district, province, country, zipcode)

        cursor.execute(customer_sql, customer_values)
        customer_id = cursor.lastrowid  # Get the newly inserted customer ID

        # ✅ Insert subscription into `subscriptions` table
        subscription_sql = """
            INSERT INTO subscriptions (customer_id, package_id, start_date, end_date) 
            VALUES (%s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 30 DAY))
        """
        subscription_values = (customer_id, package_id)
        cursor.execute(subscription_sql, subscription_values)

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Customer and subscription added successfully", "customer_id": customer_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Route: Search Customers with Filters
@app.route('/customers', methods=['GET'])
def search_customers():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # ✅ Base Query
        query = """
            SELECT 
                c.customer_id, c.first_name, c.last_name, c.phone_number, c.email,
                c.address, c.subdistrict, c.district, c.province, c.country, c.zipcode,
                s.start_date, s.end_date,
                p.package_name, p.monthly_fee, p.call_minutes, p.data_quota_gb, p.description
            FROM customers c
            JOIN subscriptions s ON c.customer_id = s.customer_id
            JOIN packages p ON s.package_id = p.package_id
            WHERE 1=1
        """

        # ✅ Filtering Parameters
        params = []
        phone_number = request.args.get('phone_number')
        package_name = request.args.get('package_name')
        province = request.args.get('province')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if phone_number:
            query += " AND c.phone_number = %s"
            params.append(phone_number)

        if package_name:
            query += " AND p.package_name LIKE %s"
            params.append(f"%{package_name}%")

        if province:
            query += " AND c.province LIKE %s"
            params.append(f"%{province}%")

        if start_date:
            query += " AND s.start_date >= %s"
            params.append(start_date)

        if end_date:
            query += " AND s.end_date <= %s"
            params.append(end_date)

        # ✅ Execute Query with Filters
        cursor.execute(query, tuple(params))
        customer_data = cursor.fetchall()

        cursor.close()
        conn.close()

        if customer_data:
            return jsonify(customer_data)
        else:
            return jsonify({"error": "No matching customers found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)})

# ✅ Run Flask App
if __name__ == '__main__':
    app.run(debug=True)


