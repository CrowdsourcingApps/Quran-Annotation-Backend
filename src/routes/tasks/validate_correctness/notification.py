from json import load, dump
from collections import defaultdict
from src.routes.notifications.helper import notification_helper
from src.routes.notifications.schema import TopicEnum
from src.routes.tasks.validate_correctness.handler \
    import get_total_solved_tasks, get_users_tokens_with_no_contributions_today
from src.settings import settings
from src.settings.logging import logger


async def achievement_notification():
    logger.info("vc_achievement_notification method has been invoked")
    # load acheivement targets json file
    file_path = 'src/routes/tasks/achievement_targets.json'
    # Read the current data from the JSON file
    with open(file_path, "r") as json_file:
        target_achievements = load(json_file)

    vc_target_achievement = target_achievements['validate_correctness']
    if vc_target_achievement == 500:
        vc_next_target_achievement = 1000
    else:
        vc_next_target_achievement = vc_target_achievement + 1000

    # get number of solved tasks till now
    vc_sloved_tasks = await get_total_solved_tasks()

    # check if the number approched the target
    if (vc_sloved_tasks >= vc_target_achievement and
       vc_sloved_tasks < vc_next_target_achievement):
        # the target acheivement is reach
        link = settings.FRONT_END

        # load message and send it for all arab users
        variables = {
                "count": vc_target_achievement,
                "mission": 'التحقق من النطق الصحيح للكلمات'
            }
        title, body = await notification_helper.get_localized_message(
                                            lang_code='ar',
                                            notification_key='achievement',
                                            variables=variables
                                        )
        # send the notification message
        topic = TopicEnum.AllARUsers
        await notification_helper.push_notification_topic(title, body,
                                                          topic, link)

        # load message and send it for all english users
        variables = {
                "count": vc_target_achievement,
                "mission": 'Validate the correctness of word pronunciation'
            }
        title, body = await notification_helper.get_localized_message(
                                            lang_code='en',
                                            notification_key='achievement',
                                            variables=variables
                                        )
        # send the notification message
        topic = TopicEnum.AllENUsers
        await notification_helper.push_notification_topic(title, body,
                                                          topic, link)

        # load message and send it for all Russian users
        variables = {
                "count": vc_target_achievement,
                "mission": 'Validate the correctness of word pronunciation'
            }
        title, body = await notification_helper.get_localized_message(
                                            lang_code='ru',
                                            notification_key='achievement',
                                            variables=variables
                                        )
        # send the notification message
        topic = TopicEnum.AllRUUsers
        await notification_helper.push_notification_topic(title, body,
                                                          topic, link)
        # update the target acheviement value
        target_achievements['validate_correctness'] = \
            vc_next_target_achievement
        # Write the updated data back to the JSON file
        with open(file_path, "w") as json_file:
            dump(target_achievements, json_file, indent=4)


async def contribute_notification():
    logger.info("vc_contribute_notification method has been invoked")
    # get users who haven't contribute today with their language
    tokens = await get_users_tokens_with_no_contributions_today()
    if len(tokens) > 0:
        # Create a defaultdict to store tokens by language
        categorized_tokens = defaultdict(list)
        # Categorize tokens based on user.language
        for token in tokens:
            language = token['language']
            token = token['token']
            categorized_tokens[language].append(token)

        link = settings.FRONT_END + '/task/vc'

        # load message and send it for arab tokens
        variables = {
                "mission": 'التحقق من النطق الصحيح للكلمات'
            }
        title, body = await notification_helper.get_localized_message(
                                            lang_code='ar',
                                            notification_key='task_reminder',
                                            variables=variables
                                        )
        # send the notification message
        await notification_helper.push_notification_tokens(
                        title, body, categorized_tokens['ar'], link)

        # load message and send it for en tokens
        variables = {
                "mission": 'Validate the correctness of word pronunciation'
            }
        title, body = await notification_helper.get_localized_message(
                                            lang_code='en',
                                            notification_key='task_reminder',
                                            variables=variables
                                        )
        # send the notification message
        await notification_helper.push_notification_tokens(
                        title, body, categorized_tokens['en'], link)

        # load message and send it for ru tokens
        variables = {
                "mission": 'Validate the correctness of word pronunciation'
            }
        title, body = await notification_helper.get_localized_message(
                                            lang_code='ru',
                                            notification_key='task_reminder',
                                            variables=variables
                                        )
        # send the notification message
        await notification_helper.push_notification_tokens(
                        title, body, categorized_tokens['ru'], link)
