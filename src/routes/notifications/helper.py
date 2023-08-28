import json
import asyncio
from firebase_admin import messaging
from src.settings.logging import logger
from src.routes.notifications.handler import get_stale_tokens, delete_tokens
from src.routes.schema import language_to_topic_mapping
from collections import defaultdict


MAX_RETRIES = 3


class NotificationHelper:
    async def load_localization_file(self, lang_code):
        # Load the JSON localization file based on lang_code
        file_path = f'src/localization/{lang_code}.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            localization_data = json.load(file)

        return localization_data

    async def get_localized_message(self, lang_code, notification_key,
                                    variables=None):
        localization_data = await self.load_localization_file(lang_code)

        notification = localization_data[notification_key]
        title = notification['title']
        body = (
                notification['body'].format(**variables)
                if variables
                else notification['body']
            )

        return title, body

    async def subscribe_topic(self, tokens, topic):
        # TODO Tokens should be here batch of 1000
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
        # TODO Tokens should be here batch of 1000
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

    async def push_notification_topic(self, title, body, topic, link):
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
        max_tokens_per_batch = 500  # Maximum tokens per batch
        while retries < MAX_RETRIES:
            try:
                for i in range(0, len(tokens), max_tokens_per_batch):
                    batch_tokens = tokens[i:i + max_tokens_per_batch]
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
                        tokens=batch_tokens
                    )
                    messaging.send_multicast(message)
                break
            except Exception as e:
                # TODO handle exception correctly and remove invalid tokens
                retries += 1
                # Use 'await' for asynchronous sleep
                await asyncio.sleep(2 ** retries)  # Exponential backoff
                logger.error(
                    f'Failed to send notification {title} to tokens {tokens}'
                    f' due to {e}')
        return

    async def unsubscribe_subscribe_topic(self, old_topic, new_topic, tokens):
        await self.unsubscribe_topic(tokens, old_topic)
        await self.subscribe_topic(tokens, new_topic)
        return


notification_helper = NotificationHelper()


async def check_and_delete_stale_token():
    logger.info("check_and_delete_stolean_token method has been invoked")
    # get steal_tokens
    tokens = await get_stale_tokens()

    if len(tokens) > 0:
        # Create a defaultdict to store tokens by language
        categorized_tokens = defaultdict(list)
        # Categorize tokens based on user.language
        for token in tokens:
            language = token['language']
            token = token['token']
            categorized_tokens[language].append(token)

        all_tokens = []
        # unsubscribe the tokens from their topics
        for language, tokens in categorized_tokens.items():
            all_tokens.extend(tokens)
            topic = language_to_topic_mapping.get(language)
            await notification_helper.unsubscribe_topic(tokens, topic)

        # delete stolen token
        await delete_tokens(all_tokens)
