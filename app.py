from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)
data_file = 'data.csv'

@app.route('/data', methods=['GET'])
def get_data():
    data = pd.read_csv(data_file)
    return jsonify(data.to_dict(orient='records'))

@app.route('/data/<int:id>', methods=['GET'])
def get_data_by_id(id):
    data = pd.read_csv(data_file)
    data_by_id = data[data['id'] == id]
    if data_by_id.empty:
        return jsonify({'error': 'No data found with that ID'})
    else:
        return jsonify(data_by_id.to_dict(orient='records')[0])

@app.route('/data', methods=['POST'])
def add_data():
    data = pd.read_csv(data_file)
    new_data = {
        'id': request.json['id'],
        'name': request.json['name'],
        'age': request.json['age'],
        'email': request.json['email']
    }
    data = data.append(new_data, ignore_index=True)
    data.to_csv(data_file, index=False)
    return jsonify({'message': 'Data added successfully'})

@app.route('/data/<int:id>', methods=['PUT'])
def update_data_by_id(id):
    data = request.get_json()
    with open(data, 'r') as file:
        reader = data.DictReader(file)
        rows = list(reader)
    for row in rows:
        if int(row['id']) == id:
            row.update(data)
            with open(data, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            return jsonify(row)
    return jsonify({'error': 'Data not found'})

@app.route('/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    data = pd.read_csv(data_file)
    data_by_id = data[data['id'] == id]
    if data_by_id.empty:
        return jsonify({'error': 'No data found with that ID'})
    else:
        data = data[data['id'] != id]
        data.to_csv(data_file, index=False)
        return jsonify({'message': 'Data deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
