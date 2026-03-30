from django.db import migrations


def seed_categories(apps, schema_editor):
    Category = apps.get_model('inventory', 'Category')

    categories = [
        'HARDWARE',
        'SOFTWARE',
        'ACCESSORIES',
        'PERIPHERY',
    ]

    for category_name in categories:
        Category.objects.get_or_create(name=category_name)


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_product_category'),
    ]

    operations = [
        migrations.RunPython(seed_categories),
    ]