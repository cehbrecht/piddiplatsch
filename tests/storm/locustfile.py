from locust import HttpUser, TaskSet, task
import json
import pika


class RabbitMQTaskSet(TaskSet):
    def on_start(self):
        # Establish connection to RabbitMQ server
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.channel = self.connection.channel()

        # Declare the queue
        self.channel.queue_declare(queue="json_queue")

    def on_stop(self):
        # Close RabbitMQ connection
        self.connection.close()

    @task
    def send_json_message(self):
        # Define JSON message to be sent
        message = {
            "key": "value"
            # Add your JSON data here
        }

        # Publish message to RabbitMQ queue
        self.channel.basic_publish(
            exchange="", routing_key="json_queue", body=json.dumps(message)
        )


class RabbitMQUser(HttpUser):
    tasks = {RabbitMQTaskSet: 1}
    min_wait = 1000
    max_wait = 3000
