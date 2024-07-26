from flask import Flask, request, jsonify
import math
import uuid

app = Flask(__name__)
points_map = {}

def calculate_points(content):
    points = 0
    # One point for every alphanumeric character in the retailer name.
    add = 0
    for c in content["retailer"]:
        if c.isalnum():
            add += 1
    print(f"{add} points for every alphanumeric character in the retailer name.")
    points += add

    # 50 points if the total is a round dollar amount with no cents.
    add = 0
    total = float(content["total"])
    if total.is_integer():
        add = 50
    print(f"{add} points if the total is a round dollar amount with no cents.")
    points += add

    # 25 points if the total is a multiple of 0.25.
    add = 0
    if (total / .25).is_integer():
        add = 25
    print(f"{add} points if the total is a multiple of 0.25.")
    points += add

    # 5 points for every two items on the receipt.
    add = len(content["items"]) // 2 * 5
    print(f"{add} points for every two items on the receipt.")
    points += add

    # If the trimmed length of the item description is a multiple of 3,
    # multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    add = 0
    for item in content["items"]:
        if len(item["shortDescription"].strip()) % 3 == 0:
            add += math.ceil(float(item["price"]) * .2)
    print(f"{add} points for the length of item descriptions")
    points += add

    # 6 points if the day in the purchase date is odd.
    add = 0
    day = int(content["purchaseDate"].split("-")[-1])
    if day % 2 == 1:
        add += 6
    print(f"{add} points if the day in the purchase date is odd.")
    points += add

    # # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    add = 0
    hour = int(content["purchaseTime"].split(":")[0])
    if 14 <= hour and hour < 16:
        add = 10
    print(f"{add} points if the time of purchase is after 2:00pm and before 4:00pm.")
    points += add

    print(f"{points} points calculated")
    return points

def generate_id():
    id = str(uuid.uuid4())
    global points_map
    while id in points_map:
        id = str(uuid.uuid4())
    return id

@app.route("/receipts/process", methods=["POST"])
def process_receipts():
    content = request.json
    points = calculate_points(content)
    id = generate_id()
    global points_map
    points_map[id] = points
    return jsonify({"id": id})

@app.route("/receipts/<id>/points", methods=["GET"])
def get_points(id):
    global points_map
    print(points_map)
    return jsonify({"points": points_map[id]})