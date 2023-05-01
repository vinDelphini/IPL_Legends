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


class IndexedTimeStampedModel(models.Model):
    created = AutoCreatedField("created", db_index=True)
    modified = AutoLastModifiedField("modified", db_index=True)

    class Meta:
        abstract = True


class SafeAutoSlugField(AutoSlugField):
    def slug_generator(self, original_slug, start):
        """
        Appends a random integer to duplicate slugs. Should issue fewer database
        queries and cause fewer errors during a Qualys web application scan than
        the default implementation.
        """
        yield original_slug
        for i in range(start, self.max_unique_query_attempts):
            slug = original_slug
            end = "%s%s" % (self.separator, random.randint(2, 999999))
            end_len = len(end)
            if self.slug_len and len(slug) + end_len > self.slug_len:
                slug = slug[: self.slug_len - end_len]
                slug = self._slug_strip(slug)
            slug = "%s%s" % (slug, end)
            yield slug
        raise RuntimeError(
            "max slug attempts for %s exceeded (%s)"
            % (original_slug, self.max_unique_query_attempts)
        )


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)


class SoftDeletionModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def _delete_related(self, related):
        rel = related.get_accessor_name()

        # Sometimes there is nothing to delete
        if not hasattr(self, rel):
            return

        try:
            if related.one_to_one:
                getattr(self, rel).delete()
            else:
                getattr(self, rel).all().delete()
        except AttributeError:
            pass

    def delete(self, **kwargs):
        """Soft delete, including soft-deletable related objects."""
        self.deleted_at = timezone.now()
        all_related = [
            f
            for f in self._meta.get_fields()
            if (f.one_to_many or f.one_to_one)
            and f.auto_created
            and not f.concrete
            and hasattr(
                self._meta.get_fields()[1].model, "deleted_at"
            )  # Inherits from SoftDeletionModel
        ]
        for obj in all_related:
            self._delete_related(obj)
        self.save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()


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
        blank=True,
        null=True,
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
