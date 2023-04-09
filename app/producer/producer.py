from flask import Flask, request, jsonify
import pika
import json
import os

app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'test success'})

@app.route('/produce', methods=['POST'])
def produce_message():
    # Validate input data
    try:
        data = request.json
        # Check for required fields
        required_fields = ['device_id', 'client_id', 'created_at', 'data']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"{field} is missing in the input data")
        # Check for data format
        # ...
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # Append 'low_prob' tag if prob < 0.25
    for pred in data['data']['preds']:
        if 'prob' in pred and pred['prob'] < 0.25:
            pred['tags'] = pred.get('tags', []) + ['low_prob']

    # Publish message to RabbitMQ
    credentials = pika.PlainCredentials(username=os.environ.get('RABBITMQ_USER'), password=os.environ.get('RABBITMQ_PASS'))
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.environ.get('RABBITMQ_HOST'), credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue=os.environ.get('RABBITMQ_QUEUE_NAME'))

    message = json.dumps(data)
    channel.basic_publish(exchange='', routing_key=os.environ.get('RABBITMQ_QUEUE_NAME'), body=message)

    connection.close()

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
