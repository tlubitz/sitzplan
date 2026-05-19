from django.contrib import admin
from .models import Klasse, Tisch, SchuelerIn, Vorliebe, Verboten, TischVorliebe, Sitzplan, Zuweisung

admin.site.register(Klasse)
admin.site.register(Tisch)
admin.site.register(SchuelerIn)
admin.site.register(Vorliebe)
admin.site.register(Verboten)
admin.site.register(TischVorliebe)
admin.site.register(Sitzplan)
admin.site.register(Zuweisung)
