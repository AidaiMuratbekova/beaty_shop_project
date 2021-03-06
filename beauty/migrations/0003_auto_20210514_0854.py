# Generated by Django 3.1 on 2021-05-14 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('beauty', '0002_auto_20210514_0821'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('rating', models.PositiveSmallIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='beauty.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.CheckConstraint(check=models.Q(('rating__gte', 1), ('rating__lte', 5)), name='rating__range'),
        ),
    ]
