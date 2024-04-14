# Generated by Django 4.2 on 2024-04-14 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='legendcupscore',
            options={'ordering': ['-score']},
        ),
        migrations.AlterField(
            model_name='match',
            name='team_1',
            field=models.CharField(choices=[('CSK', 'Chennai Super Kings'), ('DC', 'Delhi Capitals'), ('GT', 'Gujrat Titans'), ('KKR', 'Kolkata Knight Riders'), ('LKN', 'Lucknow Super Giants'), ('MI', 'Mumbai Indians'), ('KIXP', 'Punjab Kings'), ('RR', 'Rajasthan Royals'), ('RCB', 'Royal Challengers Bangalore'), ('SRH', 'Sunrisers Hyderabad')], max_length=256, verbose_name='Team Name'),
        ),
        migrations.AlterField(
            model_name='match',
            name='team_2',
            field=models.CharField(choices=[('CSK', 'Chennai Super Kings'), ('DC', 'Delhi Capitals'), ('GT', 'Gujrat Titans'), ('KKR', 'Kolkata Knight Riders'), ('LKN', 'Lucknow Super Giants'), ('MI', 'Mumbai Indians'), ('KIXP', 'Punjab Kings'), ('RR', 'Rajasthan Royals'), ('RCB', 'Royal Challengers Bangalore'), ('SRH', 'Sunrisers Hyderabad')], max_length=256, verbose_name='Team Name'),
        ),
        migrations.AlterField(
            model_name='matchscore',
            name='score',
            field=models.IntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), ('Miss', 'Miss')], null=True),
        ),
    ]
