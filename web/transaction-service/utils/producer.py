import pika
import os
import json

CONNECTION_PARAMS = pika.URLParameters(os.environ.get("CLOUDAMQP_URL"))


def send_transaction(session):
    connection = pika.BlockingConnection(CONNECTION_PARAMS)
    channel = connection.channel()  # start a new channel

    queue_name = "success_transactions"
    channel.queue_declare(queue=queue_name)  # declare the queue

    transaction = {
        "session": session,
        "project_id": 2,
    }  # TODO: hardcode for testing, to be changed

    channel.basic_publish(
        exchange="", routing_key=queue_name, body=json.dumps(transaction)
    )
    print(f"Successfully sent the transaction {session.id} details to {queue_name}")

    connection.close()
