import json
import uuid
from flask import Flask, request, jsonify, make_response
from datetime import datetime
import math

app = Flask(__name__)

# In-memory storage for receipts
receipts_db = {}

def calculate_points(receipt):
    """
    Calculate points based on the criteria provided.

    Args:
        receipt (dict): The receipt data including retailer name, total amount,
                        items list, purchase date, and time.

    Returns:
        int: Total points calculated based on the receipt data.
    """

    # variable to collect points
    points = 0

    # 1. Retailer Name Points: 1 point for every alphanumeric character
    points += sum(1 for char in receipt['retailer'] if char.isalnum())

    # 2. Total Amount Points
    total = float(receipt['total'])
    if total == int(total): # add 50 points if the total is a round dollar amount with no cents
        points += 50    
    if total % 0.25 == 0: # add 25 points if the total is a multiple of 0.25.
        points += 25

    # 3. Item Points: 5 points for every two items on the receipt
    points += 5 * (len(receipt["items"]) // 2)

    # 4. Item Description Points: 
    for item in receipt['items']:
        # if trimmed length is multiple of 3
        if len(item['shortDescription'].strip()) % 3 == 0: # If the trimmed length of the item description is a multiple of 3
            points += math.ceil(float(item["price"]) * 0.2) # multiply the price by 0.2 and round up to the nearest integer

    # 6. Purchase Date Points: 6 points if the day is odd
    if datetime.strptime(receipt["purchaseDate"],"%Y-%m-%d").day % 2 != 0:
        points += 6

    # 7. Purchase Time Points: 10 points if the time is between 2:00 PM and 4:00 PM
    if datetime.strptime("14:00","%H:%M").time() < datetime.strptime(receipt['purchaseTime'], "%H:%M").time() and datetime.strptime("16:00","%H:%M").time() > datetime.strptime(receipt['purchaseTime'], "%H:%M").time():
        points += 10


    return points


@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    """
    Endpoint to process a receipt and generate a unique ID.

    Returns:
        json: A response containing a unique receipt ID.
    """
    try:
        # Get the JSON data from the request
        data = request.get_json()

# This checks if data is None or empty, meaning no JSON data was provided in the request OR checks if the JSON data contains all the required keys: 'retailer', 'total', 'items', 'purchaseDate', and 'purchaseTime'.
# If either of these conditions is True (meaning the data is missing or incomplete), the code will run the line inside this if statement.
        if not data or not all(key in data for key in ['retailer', 'total', 'items', 'purchaseDate', 'purchaseTime']):
            return make_response(jsonify({"error": "Invalid or incomplete receipt data"}), 400)

        # Generate a unique ID for the receipt
        receipt_id = str(uuid.uuid4())

        # Save the receipt in dictionary (local memory)
        receipts_db[receipt_id] = data

        #return receipt_id
        return jsonify(id = receipt_id)
    
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@app.route('/receipts/<string:receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    """
    Endpoint to retrieve points for a specific receipt by its ID.

    Args:
        receipt_id (str): Unique identifier for the receipt.

    Returns:
        json: A response containing the points for the receipt.
    """
    try:
        
        if receipt_id not in receipts_db.keys() : # if receipt id does not exist 
            return make_response(jsonify({"error": "Receipt ID not found"}), 404) # display error

        receipt = receipts_db[receipt_id]
        # Calculate the points for this receipt
        return jsonify(points = calculate_points(receipts_db[receipt_id])),200
    
    except Exception as e: 
        return make_response(jsonify({"error": str(e)}), 500)
    

if __name__ == '__main__':
    app.run(debug=True)