import mysql.connector
from flask import Flask, jsonify

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  # Use your MySQL username
        password='root',  # Use your MySQL password
        database='momo_transactions'
    )
    return connection

@app.route('/transactions', methods=['GET'])
def get_transactions():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(transactions)

if __name__ == '__main__':
    app.run(debug=True)
