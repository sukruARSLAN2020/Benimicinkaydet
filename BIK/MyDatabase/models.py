from django.db import models

class Ders(models.Model):
    dersadı=models.CharField(max_length=15)
    konu=models.CharField(max_length=50)
    altkonu=models.CharField(max_length=200)

    def __str__(self):
        return self.dersadı

class DersCalısGoruntule(models.Model):
    konucalısgoruntule=models.ForeignKey('Ders',on_delete=models.CASCADE)
    ozetekle=models.TextField()
    zamanata=models.DateTimeField()
    islenmedurumu=models.BooleanField(default='false')

    #def __str__(self):
    #   return self.konucalısgoruntule

class CanlıDersKaydı(models.Model):
    canliderskonu=models.ForeignKey('Ders',on_delete=models.CASCADE)
    platform=models.CharField(max_length=15)
    platformzamanata=models.DateTimeField()

    def __str__(self):
        return self.platform

class Sınavlar(models.Model):
    sınavaltkonu=models.ForeignKey('Ders',on_delete=models.CASCADE)
    sinavtipi=models.CharField(max_length=25)
    sinavzamanata=models.DateTimeField()
    sinavdogrusayisi=models.PositiveSmallIntegerField()
    sinavyanlissayisi=models.PositiveSmallIntegerField()
    sınavbossayisi=models.PositiveSmallIntegerField()

    def __str__(self):
        return self.sinavtipi    