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


class Task(Model):
    surra_number = fields.IntField()
    aya_number = fields.IntField()
    audio_file_name = fields.CharField(max_length=128, unique=True)
    duration_ms = fields.IntField(description='length of the audio file in ms')
    create_date = fields.DateField(default=None)
    client_id = fields.CharField(max_length=128,
                                 unique=True,
                                 description='The id of the recitier')
    final_transcription = fields.TextField()
    label = fields.CharEnumField(LabelEnum)
    validated = fields.BooleanField(default=False)


class User(Model):
    email = fields.CharField(max_length=128, unique=True)
    hashed_password = fields.CharField(128)
    user_role = fields.CharEnumField(UserRoleEnum, default='annotator')
    create_date = fields.DateField(default=datetime.utcnow)
    validate_correctness_exam_correct_no = fields.IntField(
        default=0,
        description='Number of correct answers in the entrance exam'
                    ' of validate correctness task type')
    validate_correctness_cts = fields.ManyToManyField(
        'models.ValidateCorrectnessControlTask',
        through='validate_correctness_ct_user')


class ValidateCorrectnessControlTask(Model):
    surra_number = fields.IntField()
    aya_number = fields.IntField()
    audio_file_name = fields.CharField(max_length=128, unique=True)
    duration_ms = fields.IntField(description='length of the audio file in ms')
    create_date = fields.DateField(default=datetime.utcnow)
    golden = fields.BooleanField(default=False)
    label = fields.CharEnumField(LabelEnum)


class ValidateCorrectnessCTUser(Model):
    validate_correctness_ct = fields.ForeignKeyField(
        'models.ValidateCorrectnessControlTask')
    user = fields.ForeignKeyField('models.User')
    test = fields.BooleanField(default=False,
                               description='Indicate if the answer is given'
                                           ' for an entrance test or for'
                                           '  quality control')
    label = fields.CharEnumField(LabelEnum)
    create_date = fields.DateField(default=datetime.utcnow)

    class Meta:
        table = 'validate_correctness_ct_user'
        unique_together = ['validate_correctness_ct', 'user']
