from flask import Flask, request, jsonify
from process import process_data
import csv
import login

app = Flask(__name__)

data = process_data()

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data.to_dict(orient='records'))

@app.route('/data/<int:id>', methods=['GET'])
def get_data_by_id(id):
    data_by_id = data[data['id'] == id]
    if data_by_id.empty:
        return jsonify({'error': 'No data found with that ID'})
    else:
        return jsonify(data_by_id.to_dict(orient='records')[0])

@app.route('/data/add/', methods=['POST'])
def add_data():
    new_data = {
        'id': request.json['id'],
        'native_english_speaker': request.json['native_english_speaker'],
        'course_instructor': request.json['course_instructor'],
        'course': request.json['course'],
        'semester': request.json['semester'],
        'class_size': request.json['class_size'],
        'performance_score': request.json['performance_score']
    }
    data = data.append(new_data, ignore_index=True)
    data.to_csv('data_file.csv', index=False)
    return jsonify({'message': 'Data added successfully'})

@app.route('/data/update/<int:id>', methods=['PUT'])
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

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_data(id):
    data_by_id = data[data['id'] == id]
    if data_by_id.empty:
        return jsonify({'error': 'No data found with that ID'})
    else:
        data = data[data['id'] != id]
        data.to_csv('data_file.csv', index=False)
        return jsonify({'message': 'Data deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)