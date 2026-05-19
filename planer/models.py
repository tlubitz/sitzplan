from django.db import models


class Klasse(models.Model):
    """A classroom / class group that has pupils and tables."""
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tisch(models.Model):
    """A table in a classroom with a fixed capacity."""
    klasse = models.ForeignKey(Klasse, on_delete=models.CASCADE, related_name='tische')
    name = models.CharField(max_length=100)
    kapazitaet = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.kapazitaet} Plätze)"


class SchuelerIn(models.Model):
    """A pupil that belongs to a class."""
    klasse = models.ForeignKey(Klasse, on_delete=models.CASCADE, related_name='schuelerinnen')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Vorliebe(models.Model):
    """How much pupil_a wants to sit with pupil_b (positive = together, negative = apart)."""
    klasse = models.ForeignKey(Klasse, on_delete=models.CASCADE, related_name='vorlieben')
    schuelerIn_a = models.ForeignKey(SchuelerIn, on_delete=models.CASCADE, related_name='vorlieben_als_a')
    schuelerIn_b = models.ForeignKey(SchuelerIn, on_delete=models.CASCADE, related_name='vorlieben_als_b')
    score = models.IntegerField(default=10)

    class Meta:
        unique_together = ('schuelerIn_a', 'schuelerIn_b')

    def __str__(self):
        return f"{self.schuelerIn_a} ↔ {self.schuelerIn_b}: {self.score}"


class Verboten(models.Model):
    """Two pupils that must NOT sit at the same table."""
    klasse = models.ForeignKey(Klasse, on_delete=models.CASCADE, related_name='verboten')
    schuelerIn_a = models.ForeignKey(SchuelerIn, on_delete=models.CASCADE, related_name='verboten_als_a')
    schuelerIn_b = models.ForeignKey(SchuelerIn, on_delete=models.CASCADE, related_name='verboten_als_b')

    class Meta:
        unique_together = ('schuelerIn_a', 'schuelerIn_b')

    def __str__(self):
        return f"{self.schuelerIn_a} ✗ {self.schuelerIn_b}"


class TischVorliebe(models.Model):
    """How much a pupil likes/dislikes tables of a given capacity."""
    klasse = models.ForeignKey(Klasse, on_delete=models.CASCADE, related_name='tisch_vorlieben')
    schuelerIn = models.ForeignKey(SchuelerIn, on_delete=models.CASCADE, related_name='tisch_vorlieben')
    kapazitaet = models.PositiveIntegerField()
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = ('schuelerIn', 'kapazitaet')

    def __str__(self):
        return f"{self.schuelerIn} @ Tisch(Kap={self.kapazitaet}): {self.score}"


class Sitzplan(models.Model):
    """A computed seating plan for a class."""
    klasse = models.ForeignKey(Klasse, on_delete=models.CASCADE, related_name='sitzplaene')
    created_at = models.DateTimeField(auto_now_add=True)
    gesamt_glueck = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('solved', 'Gelöst'), ('infeasible', 'Keine Lösung')],
        default='pending',
    )

    def __str__(self):
        return f"Sitzplan für {self.klasse} ({self.created_at:%d.%m.%Y %H:%M})"


class Zuweisung(models.Model):
    """Assignment of one pupil to one table in a Sitzplan."""
    sitzplan = models.ForeignKey(Sitzplan, on_delete=models.CASCADE, related_name='zuweisungen')
    schuelerIn = models.ForeignKey(SchuelerIn, on_delete=models.CASCADE)
    tisch = models.ForeignKey(Tisch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.schuelerIn} → {self.tisch}"
