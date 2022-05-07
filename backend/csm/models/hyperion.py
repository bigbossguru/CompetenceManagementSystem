from django.db import models


class Hyperion(models.Model):
    """Hyperion Database Model"""

    code = models.CharField(max_length=7, primary_key=True)
    name = models.CharField(max_length=250, null=True)
    function = models.CharField(max_length=250, null=True)

    def __str__(self) -> str:
        return f"{self.code}: {self.name}"
