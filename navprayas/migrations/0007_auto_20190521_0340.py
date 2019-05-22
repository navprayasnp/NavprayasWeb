# Generated by Django 2.2 on 2019-05-21 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navprayas', '0006_auto_20190521_0334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pr',
            name='category',
        ),
        migrations.AlterField(
            model_name='pr',
            name='class1',
            field=models.CharField(choices=[('', 'select'), ('7', '7 (Junior)'), ('8', '8 (Junior)'), ('9', '9 (Senior)'), ('10', '10 (Senior)')], max_length=2, verbose_name='Class'),
        ),
        migrations.AlterField(
            model_name='pr',
            name='class2',
            field=models.CharField(choices=[('', 'select'), ('7', '7 (Junior)'), ('8', '8 (Junior)'), ('9', '9 (Senior)'), ('10', '10 (Senior)')], max_length=2, verbose_name='Class'),
        ),
        migrations.AlterField(
            model_name='pr',
            name='class3',
            field=models.CharField(blank=True, choices=[('', 'select'), ('7', '7 (Junior)'), ('8', '8 (Junior)'), ('9', '9 (Senior)'), ('10', '10 (Senior)')], max_length=2, null=True, verbose_name='Class'),
        ),
    ]
