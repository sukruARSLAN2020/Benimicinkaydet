from django.contrib import admin
from .models import Ders,DersCalısGoruntule,CanlıDersKaydı,Sınavlar

class PostDers(admin.ModelAdmin):
    list_display = ['dersadı', 'konu','altkonu']
    list_display_links = ['altkonu']
    list_filter = ['dersadı']
    search_fields = ['dersadı', 'konu']
    #list_editable = ['altkonu']
    class Meta:
        model = Ders
admin.site.register(Ders, PostDers)
 

class PostDersCalısGoruntule(admin.ModelAdmin):
    list_display = ['konucalısgoruntule', 'zamanata']
    list_display_links = ['konucalısgoruntule']
    list_filter = ['konucalısgoruntule']
    search_fields = ['konucalısgoruntule']
    #list_editable = ['zamanata']
    class Meta:
        model = DersCalısGoruntule
admin.site.register(DersCalısGoruntule,PostDersCalısGoruntule)

class PostCanlıDersKaydı(admin.ModelAdmin):
    list_display = ['platform','platformzamanata']
    list_display_links = ['platform']
    list_filter = ['platform']
    search_fields = ['canlıderskonu', 'platform']
    #list_editable = ['zamanata']
    class Meta:
        model = CanlıDersKaydı
admin.site.register(CanlıDersKaydı,PostCanlıDersKaydı)

class PostSınavlar(admin.ModelAdmin):
    list_display = ['sınavaltkonu','sinavtipi']
    list_display_links = ['sinavtipi']
    list_filter = ['sinavtipi']
    search_fields = ['sınavaltkonu', 'sinavtipi']
    #list_editable = ['zamanata']
    class Meta:
        model = Sınavlar
admin.site.register(Sınavlar,PostSınavlar)


