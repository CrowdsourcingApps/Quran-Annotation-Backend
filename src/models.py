from datetime import datetime
from enum import Enum

from tortoise import fields
from tortoise.models import Model


class UserRoleEnum(str, Enum):
    Admin = 'admin'
    RecitingApp = 'reciting_app'
    Annotator = 'annotator'


class LabelEnum(str, Enum):
    Correct = 'correct'
    InCorrect = 'in_correct'
    NotRelatedToQuran = 'not_related_quran'
    NotMatchAya = 'not_match_aya'
    MultipleAya = 'multiple_aya'
    InComplete = 'in_complete'


class PlatformEnum(str, Enum):
    Android = 'android'
    IOS = 'ios'
    Web = 'web'


class LanguageEnum(str, Enum):
    AR = 'ar'
    EN = 'en'
    RU = 'ru'


class User(Model):
    email = fields.CharField(max_length=128, unique=True,
                             null=True, default=None)
    hashed_password = fields.CharField(128, null=True, default=None)
    user_role = fields.CharEnumField(UserRoleEnum, default='annotator')
    create_date = fields.DatetimeField(default=datetime.utcnow)
    validate_correctness_exam_pass = fields.BooleanField(
        default=False)
    validate_correctness_tasks_no = fields.IntField(
        default=0,
        description='Number of tasks that user solve in'
                    'validate correctness task type')
    is_anonymous = fields.BooleanField(default=False)
    language = fields.CharEnumField(LanguageEnum, default='ar')
    validate_correctness_cts = fields.ManyToManyField(
        'models.ValidateCorrectnessCT',
        through='validate_correctness_ct_user')
    validate_correctness_ts = fields.ManyToManyField(
        'models.Task',
        through='validate_correctness_t_user')


class NotificationToken(Model):
    user = fields.ForeignKeyField('models.User',
                                  related_name='notificationtokens')
    token = fields.CharField(max_length=255)
    platform = fields.CharEnumField(PlatformEnum)
    update_date = fields.DatetimeField(default=datetime.utcnow)


class ValidateCorrectnessCT(Model):
    surra_number = fields.IntField()
    aya_number = fields.IntField()
    client_id = fields.CharField(max_length=128,
                                 null=True,
                                 description='The id of the recitier')
    audio_file_name = fields.CharField(max_length=128, unique=True)
    duration_ms = fields.IntField(description='length of the audio file in ms')
    create_date = fields.DatetimeField(default=datetime.utcnow)
    golden = fields.BooleanField(default=True)
    label = fields.CharEnumField(LabelEnum)

    class Meta:
        table = 'validate_correctness_ct'
        description = ('The model is for controle tasks that'
                       ' have validate correctness type')


class ValidateCorrectnessCTUser(Model):
    validatecorrectnessct = fields.ForeignKeyField(
        'models.ValidateCorrectnessCT')
    user = fields.ForeignKeyField('models.User')
    test = fields.BooleanField(default=False,
                               description='Indicate if the answer is given'
                                           ' for an entrance test or for'
                                           '  quality control')
    label = fields.CharEnumField(LabelEnum)
    correct_answer = fields.BooleanField(default=True)
    create_date = fields.DatetimeField(default=datetime.utcnow)

    class Meta:
        table = 'validate_correctness_ct_user'
        unique_together = ['validatecorrectnessct', 'user']


class Task(Model):
    surra_number = fields.IntField()
    aya_number = fields.IntField()
    audio_file_name = fields.CharField(max_length=128, unique=True)
    duration_ms = fields.IntField(description='length of the audio file in ms')
    create_date = fields.DatetimeField(null=True)
    client_id = fields.CharField(max_length=128,
                                 null=True,
                                 description='The id of the recitier')
    final_transcription = fields.TextField(null=True)
    label = fields.CharEnumField(LabelEnum, null=True)
    validated = fields.BooleanField(default=False)


class ValidateCorrectnessTUser(Model):
    task = fields.ForeignKeyField(
        'models.Task')
    user = fields.ForeignKeyField('models.User')
    label = fields.CharEnumField(LabelEnum)
    create_date = fields.DatetimeField(default=datetime.utcnow)

    class Meta:
        table = 'validate_correctness_t_user'
        unique_together = ['task', 'user']
        description = ('The model is for tasks that user solve'
                       ' in validate correctness phase')
