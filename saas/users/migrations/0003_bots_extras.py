# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_cpf_userprofile_trial_ends_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='extra_bots',
            field=models.IntegerField(default=0, help_text='Bots adicionais (além do plano base)'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='monthly_price',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Preço mensal atual (calculado automaticamente)', max_digits=10),
        ),
    ]



