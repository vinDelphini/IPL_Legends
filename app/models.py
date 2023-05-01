import random
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from django_extensions.db.fields import AutoSlugField
from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from django.core.validators import MinValueValidator, MaxValueValidator


TEAMS = [
    ('CSK', 'Chennai Super Kings'),
    ('DC', 'Delhi Capitals'),
    ('GT', 'Gujrat Titans'),
    ('KKR' ,'Kolkata Knight Riders'),
    ('LSG', 'Lucknow Super Giants'),
    ('MI', 'Mumbai Indians'),
    ('KIXP', 'Punjab Kings'),
    ('RR', 'Rajasthan Royals'),
    ('RCB', 'Royal Challengers Bangalore'),
    ('SRH', 'Sunrisers Hyderabad'),
]

# CONTENDERS = [
#     ('Hari Babu', 'Iplmogudu'),
#     ('Naveen Sai', 'Naveen Eleven 1136'),
#     ('Sarva Rayudu', 'SARVARA UNITED 112092'),
#     ('Munni', 'SATYA SULTANS 200007'),
#     ('Srinu Kumbha', 'SRIs IX'),
#     ('Uma Mahesh', 'Umamahe Kingsmen 11'),
#     ('Venki Rayudu', 'VIN ROYAL SCORCHERS'),
# ]

SCORE_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
    ]

SCORE_MAPPING = {
    1: 200,
    2: 190,
    3: 180,
    4: 170,
    5: 160,
    6: 150,
    7: 140,
}


class IndexedTimeStampedModel(models.Model):
    created = AutoCreatedField("created", db_index=True)
    modified = AutoLastModifiedField("modified", db_index=True)

    class Meta:
        abstract = True


class Match(models.Model):

    match_no = models.IntegerField(
        unique=True,
        verbose_name="Macth Number",
        validators=[MinValueValidator(1), MaxValueValidator(99)]
    )
    # slug = SafeAutoSlugField(
    #     overwrite=True, max_length=191, populate_from="match_no", unique=True
    # )
    team_1 = models.CharField(
        max_length=256,
        choices=TEAMS,
        verbose_name="Team Name",
    )
    team_2 = models.CharField(
        max_length=256,
        choices=TEAMS,
        verbose_name="Team Name",
    )

    def __str__(self):
        return f'{self.match_no} - {self.team_1} vs {self.team_2}'

class Contender(models.Model):
    name = models.CharField(
        # choices=CONTENDERS,
        unique=True,
        max_length=254,
        verbose_name="Contender Name",
    )

    def __str__(self):
        return self.name


class MatchScore(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True, blank=True)
    contender = models.ForeignKey(Contender, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField(choices=SCORE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f'{self.match} - {self.contender} - {self.score}'

    def get_score_value(self):
        return SCORE_MAPPING.get(self.score)

    try:
        obj, created = MatchScore.objects.update_or_create(
            match=match,
            contender=contender,
            defaults={'score': score},
        )
        if not created:
            # Object was updated
            print(f"Updated {obj}")
        else:
            # Object was created
            print(f"Created {obj}")
    except Exception as e:
        # Handle exception
        print(e)


class LegendCupScore(models.Model):
    contender = models.ForeignKey(Contender, on_delete=models.CASCADE, null=True, blank=True)
    score = models.DecimalField(max_digits=10, decimal_places=1)
