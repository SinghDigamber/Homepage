from django.db import models

# Create your models here.

class Alternative(models.Model):
    AName = models.CharField(max_length=140)

    def __str__(self):
        return str(self.AName);


class Сriterion(models.Model):
    CName = models.CharField(max_length=140)
    CRange = models.IntegerField(blank=True)
    CWeight = models.IntegerField(blank=True)
    CType = models.CharField(max_length=140, blank=True)
    OptimType = models.CharField(max_length=140, blank=True)
    EdIzmer = models.CharField(max_length=140, blank=True)
    ScaleType = models.CharField(max_length=140, blank=True)

    def __str__(self):
        return str(self.CName);


class Mark(models.Model):
    IdCrit = models.ForeignKey(
        'Сriterion',
        on_delete=models.CASCADE,
        blank=True
    )
    MName = models.CharField(max_length=140, blank=True)
    MRange = models.IntegerField(blank=True)
    NumMark = models.IntegerField(blank=True)
    NormMark = models.IntegerField(blank=True)

    def __str__(self):
        return str(self.IdCrit.CName+": "+self.MName)


class Vector(models.Model):
    class Meta:
        ordering = ['IdMark']
    IdAlt = models.ForeignKey(
        'Alternative',
        on_delete=models.CASCADE,
        blank=True
    )
    IdMark = models.ForeignKey(
        'Mark',
        on_delete=models.CASCADE,
        blank=True
    )

    def __str__(self):
        return "[" + self.IdAlt.AName + "] " + self.IdMark.IdCrit.CName + ": " + self.IdMark.MName



class LPR(models.Model):
    LName = models.CharField(max_length=140)
    LRange = models.IntegerField(blank=True)


class Result(models.Model):
    IdLPR = models.ForeignKey(
        'LPR',
        on_delete=models.CASCADE,
        blank=True
    )
    IdAlt = models.ForeignKey(
        'Alternative',
        on_delete=models.CASCADE,
        blank=True
    )
    Range = models.IntegerField(blank=True)
    AWeight = models.IntegerField(blank=True)
