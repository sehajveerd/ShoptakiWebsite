import pika
import os
import json
import time
from models import db, Project
from sqlalchemy import text

CONNECTION_PARAMS = pika.URLParameters(
    os.environ.get(
        "CLOUDAMQP_URL",
        "amqps://cvyuhplk:WaNNcDJON54lpzNWIAtUVfdOAdwqXvJD@shrimp.rmq.cloudamqp.com/cvyuhplk",
    )
)


def pull_transaction():
    connection = pika.BlockingConnection(CONNECTION_PARAMS)
    channel = connection.channel()

    queue_name = "success_transactions"
    channel.queue_declare(queue=queue_name)

    def callback(ch, method, properties, body):
        message_data = json.loads(body)

        email = message_data.get("session", {}).get("customer_details", {}).get("email")
        project_id = message_data.get("project_id")
        amount_total = message_data.get("session", {}).get("amount_total")

        query = f"SELECT auth0_id FROM user_details WHERE email_id = '{email}'"
        user = db.session.execute(query).fetchone()

        if user:
            project = Project.query.filter_by(id=project_id).first()
            if project:
                project.raisedAmount += float(amount_total) / 100

                sql = text(
                    f"UPDATE projects SET investors = array_append(investors, '{email}') WHERE id = :project_id"
                )
                db.session.execute(sql, {"project_id": project_id})
                db.session.commit()

                project.numOfInvestors = len(project.investors)
                db.session.commit()

        time.sleep(5)
        print("transaction processing finished")

    channel.basic_consume("success_transactions", callback, auto_ack=True)

    channel.start_consuming()
    connection.close()
