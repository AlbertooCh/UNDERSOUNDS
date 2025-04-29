from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_avatar_user_songs'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='backend',
            field=models.CharField(default='django.contrib.auth.backends.ModelBackend', max_length=255),
        ),
    ]
