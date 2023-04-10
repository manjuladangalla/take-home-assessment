### Multi-Container Service with RabbitMQ and Docker Compose

This project is a multi-container service that consists of a web service (producer), a RabbitMQ queue, and a consumer. The web service accepts a JSON payload, validates it, and pushes it to the RabbitMQ queue. The consumer reads messages from the queue, transforms them, and appends them to a CSV file.

## Prerequisites

[Docker](https://docs.docker.com/get-docker/)
[Docker Compose](https://docs.docker.com/compose/install/)

## Setup

1. Clone the repository:

```bash
git clone https://github.com/manjuladangalla/take-home-assessment.git
cd take-home-assessment
```

2. Start the multi-container service:

```bash
docker-compose up
```

This will start the producer, consumer, and RabbitMQ queue.

3. Send a POST request to the producer:

```bash
curl --header "Content-Type: application/json" \
     --request POST \
     --data '{"device_id": "device1", "client_id": "client1", "created_at": "2023-02-07 14:56:49.386042", "data": {"license_id": "license1", "preds": [{"image_frame": "image1", "prob": 0.5, "tags": ["tag1", "tag2"]}, {"image_frame": "image2", "prob": 0.1, "tags": ["tag3", "tag4"]}]}}' \
     http://localhost:8000/produce
```

4. Check the output CSV file

```bash
cat consumer/output/data.csv
```

## Testing

To test the producer, you can use the test_producer.py script to send a 1000 randomly generated JSON body requests to the producer endpoint. This will result in having a CSV file that contains (preds_per_message \* num_messages). To run the test, use the following command:

```bash
docker-compose -f docker-compose.test.yml up --build
```

## Notes

1. The producer service is running on port 8000.
2. The consumer service is writing output to the file consumer/output/data.csv.
3. The RabbitMQ queue is running on ports 5672 and 15672. The management UI is available at http://localhost:15672/.
4. The RabbitMQ queue is persisted to disk, so it will not lose messages if it is restarted.
