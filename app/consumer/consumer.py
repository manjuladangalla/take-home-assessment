import csv
import json
import pika
import os

# Connect to the RabbitMQ queue
credentials = pika.PlainCredentials(username=os.environ.get('RABBITMQ_USER'), password=os.environ.get('RABBITMQ_PASS'))
connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get('RABBITMQ_HOST'), credentials=credentials))
channel = connection.channel()

# Declare the queue to consume from
channel.queue_declare(queue=os.environ.get('RABBITMQ_QUEUE_NAME'))

# Open the output CSV file for writing
with open(os.environ.get('CSV_FILE_PATH'), mode='w') as csv_file:

    # Set up the CSV writer
    fieldnames = ['device_id', 'client_id', 'created_at', 'license_id', 'image_frame', 'prob', 'tags']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Define the callback function to be invoked for each message
    def callback(ch, method, properties, body):

        # Parse the message JSON
        message = json.loads(body)

        # Extract the message fields
        device_id = message['device_id']
        client_id = message['client_id']
        created_at = message['created_at']
        license_id = message['data']['license_id']

        # Process each prediction item in the message
        for pred in message['data']['preds']:

            # Extract the prediction fields
            image_frame = pred['image_frame']
            prob = pred['prob']
            tags = pred['tags']
            if prob < 0.25 and 'low_prob' not in tags:
                tags.append('low_prob')

            # Write the prediction fields to the CSV file
            writer.writerow({
                'device_id': device_id,
                'client_id': client_id,
                'created_at': created_at,
                'license_id': license_id,
                'image_frame': image_frame,
                'prob': prob,
                'tags': tags
            })

        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Start consuming messages from the queue
    channel.basic_consume(queue=os.environ.get('RABBITMQ_QUEUE_NAME'), on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    # Block the main thread and continue consuming messages until interrupted
    channel.start_consuming()
