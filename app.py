from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb+srv://janakiramanparamanantham:WIcJ5siKpUpneI8m@cluster0.aqv5s7l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client.bmi_database

bmi_collection = db.bmi_records

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bmi', methods=['POST'])
def calculate_bmi():
    try:
        data = request.get_json()
        print("Received data:", data)
        
        weight = float(data['weight'])
        height_cm = float(data['height'])  
        
        
        if not (weight > 0 and height_cm > 0):
            return jsonify({"error": "Weight and height must be greater than zero and in numeric format."}), 400
        
       
        height_m = height_cm / 100
        
        
        bmi = weight / (height_m ** 2)
        
        
        bmi_record = {
            "weight": weight,
            "height": height_cm,  
            "bmi": bmi
        }
        bmi_collection.insert_one(bmi_record)
        
        return jsonify({"bmi": bmi})
    except (KeyError, ValueError, TypeError) as e:
        print("Error:", str(e))
        return jsonify({"error": "Invalid input. Please provide weight and height in numeric format."}), 400


if __name__ == '__main__':
    app.run(debug=True)
