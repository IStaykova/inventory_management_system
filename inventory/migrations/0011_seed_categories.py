from django.db import migrations

def create_categories(apps, schema_editor):
    category = apps.get_model('inventory', 'Category')
    default_categories = ['Hardware', 'Software', 'Periphery', 'Monitors', 'Accessories']

    for name in default_categories:
        category.objects.get_or_create(name=name)

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_alter_product_options_alter_product_slug'),
    ]

    operations = [
        migrations.RunPython(create_categories),
    ]