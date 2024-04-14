import random
from django.db.models import Sum, Count, QuerySet
from operator import attrgetter
from django.db import models
from django.utils import timezone
from django_extensions.db.fields import AutoSlugField
from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from django.core.validators import MinValueValidator, MaxValueValidator


TEAMS = [
    ('CSK', 'Chennai Super Kings'),
    ('DC', 'Delhi Capitals'),
    ('GT', 'Gujrat Titans'),
    ('KKR' ,'Kolkata Knight Riders'),
    ('LKN', 'Lucknow Super Giants'),
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
        (0, 0),
    ]

SCORE_MAPPING = {
    1: 100,
    2: 90,
    3: 80,
    4: 70,
    5: 60,
    6: 50,
    7: 40,
    0: 40,
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
        # Check if there are any other MatchScore objects with the same match and score
        other_match_scores = MatchScore.objects.filter(match=self.match, score=self.score).exclude(id=self.id)
        if other_match_scores.exists() and self.match_id == 4:
            return SCORE_MAPPING[self.score] + 10
        elif other_match_scores.exists() and self.match_id == 26:
            return SCORE_MAPPING[self.score] -5
        else:
            return SCORE_MAPPING[self.score]

    def save(self, *args, **kwargs):
        # Check if a record with the same match and contender already exists
        existing_match_score = MatchScore.objects.filter(match=self.match, contender=self.contender).first()

        if existing_match_score:
            # Update the existing record instead of creating a new one
            existing_match_score.score = self.score
            super(MatchScore, existing_match_score).save(*args, **kwargs)
        else:
            super(MatchScore, self).save(*args, **kwargs)

    @staticmethod
    def count_scores_by_contender():
        # Aggregate count of each score value for each contender and include contender names
        score_counts = MatchScore.objects.values('contender', 'contender__name', 'score').annotate(score_count=Count('score'))

        # Sort by count in descending order
        score_counts = score_counts.order_by('-score_count')

        return score_counts


class LegendCupScore(models.Model):
    contender = models.ForeignKey(Contender, on_delete=models.CASCADE, null=True, blank=True)
    score = models.DecimalField(max_digits=10, decimal_places=1)

    class Meta:
        ordering = ['-score']