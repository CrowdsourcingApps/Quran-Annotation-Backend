import asyncio
from firebase_admin import messaging
from src.settings.logging import logger

MAX_RETRIES = 3


class NotificationHelper:
    async def subscribe_topic(self, tokens, topic):
        retries = 0
        while retries < MAX_RETRIES:
            response = messaging.subscribe_to_topic(tokens, topic)
            if response.failure_count > 0:
                retries += 1
                # Use 'await' for asynchronous sleep
                await asyncio.sleep(2 ** retries)  # Exponential backoff
                logger.error(
                    f'Failed to subscribe to topic {topic} due to'
                    f' {list(map(lambda e: e.reason,response.errors))}')
            else:
                break
        return

    async def unsubscribe_topic(self, tokens, topic):
        retries = 0
        while retries < MAX_RETRIES:
            response = messaging.unsubscribe_from_topic(tokens, topic)
            if response.failure_count > 0:
                retries += 1
                # Use 'await' for asynchronous sleep
                await asyncio.sleep(2 ** retries)  # Exponential backoff
                logger.error(
                    f'Failed to subscribe to topic {topic} due to'
                    f' {list(map(lambda e: e.reason,response.errors))}')
            else:
                break
        return

    async def push_notification_topic(title, body, topic, link):
        retries = 0
        while retries < MAX_RETRIES:
            try:
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
                break
            except Exception as e:
                retries += 1
                # Use 'await' for asynchronous sleep
                await asyncio.sleep(2 ** retries)  # Exponential backoff
                logger.error(
                    f'Failed to send notification {title} to topic {topic}'
                    f' due to {e}')
        return

    async def push_notification_tokens(self, title, body, tokens, link):
        retries = 0
        while retries < MAX_RETRIES:
            try:
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
                break
            except Exception as e:
                retries += 1
                # Use 'await' for asynchronous sleep
                await asyncio.sleep(2 ** retries)  # Exponential backoff
                logger.error(
                    f'Failed to send notification {title} to tokens {tokens}'
                    f' due to {e}')
        return


notification_helper = NotificationHelper()
