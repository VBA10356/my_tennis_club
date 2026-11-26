from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0004_populate_and_unique_member_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="member",
            name="image",
            field=models.ImageField(blank=True, upload_to="member_images/"),
        ),
    ]
