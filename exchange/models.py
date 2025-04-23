from django.db import models

class ExchangeMedciene(models.Model):
    class Status(models.TextChoices):
        SELL = 'Sell'
        BUY = 'Buy'

    operation = models.CharField(max_length=5, choices=Status.choices, blank=False)
    medicine = models.ForeignKey(
        'medicine.Medicine',  # String reference to avoid circular import
        on_delete=models.CASCADE,
        related_name='exchange_entries'  # Valid reverse relation name
    )
    quantity = models.IntegerField(null=False, blank=False, default=1)

    def __str__(self):
        return f"{self.medicine.name} - {self.operation} ({self.quantity})"