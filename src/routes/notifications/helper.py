
from firebase_admin import messaging
from src.settings.logging import logger


class NotificationHelper:
    def subscribe_topic(tokens, topic):
        response = messaging.subscribe_to_topic(tokens, topic)
        if response.failure_count > 0:
            logger.error(f'Failed to subscribe to topic {topic} due to'
                         f' {list(map(lambda e: e.reason,response.errors))}')

    def unsubscribe_topic(tokens, topic):
        response = messaging.unsubscribe_from_topic(tokens, topic)
        if response.failure_count > 0:
            logger.error(f'Failed to subscribe to topic {topic} due to'
                         f' {list(map(lambda e: e.reason,response.errors))}')

    def push_notification_topic(title, body, topic, link):
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            webpush=messaging.WebpushConfig(
                fcm_options=messaging.WebpushFCMOptions(
                    link=link
                )
            ),
            topic=topic
        )
        messaging.send(message)

    def push_notification_tokens(title, body, tokens, link):
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            webpush=messaging.WebpushConfig(
                fcm_options=messaging.WebpushFCMOptions(
                    link=link
                )
            ),
            tokens=tokens
        )
        messaging.send_multicast(message)


notification_helper = NotificationHelper()
