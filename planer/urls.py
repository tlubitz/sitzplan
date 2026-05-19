from django.urls import path
from . import views

urlpatterns = [
    # Klassen
    path('', views.klassen_list, name='klassen_list'),
    path('klasse/<int:pk>/', views.klasse_detail, name='klasse_detail'),
    path('klasse/<int:pk>/loeschen/', views.klasse_delete, name='klasse_delete'),

    # Tische
    path('klasse/<int:klasse_pk>/tisch/hinzufuegen/', views.tisch_add, name='tisch_add'),
    path('klasse/<int:klasse_pk>/tisch/<int:pk>/loeschen/', views.tisch_delete, name='tisch_delete'),

    # SchülerInnen
    path('klasse/<int:klasse_pk>/schueler/hinzufuegen/', views.schuelerIn_add, name='schuelerIn_add'),
    path('klasse/<int:klasse_pk>/schueler/<int:pk>/loeschen/', views.schuelerIn_delete, name='schuelerIn_delete'),

    # Vorlieben
    path('klasse/<int:klasse_pk>/vorliebe/hinzufuegen/', views.vorliebe_add, name='vorliebe_add'),
    path('klasse/<int:klasse_pk>/vorliebe/<int:pk>/loeschen/', views.vorliebe_delete, name='vorliebe_delete'),

    # Verboten
    path('klasse/<int:klasse_pk>/verboten/hinzufuegen/', views.verboten_add, name='verboten_add'),
    path('klasse/<int:klasse_pk>/verboten/<int:pk>/loeschen/', views.verboten_delete, name='verboten_delete'),

    # TischVorlieben
    path('klasse/<int:klasse_pk>/tischvorliebe/hinzufuegen/', views.tisch_vorliebe_add, name='tisch_vorliebe_add'),
    path('klasse/<int:klasse_pk>/tischvorliebe/<int:pk>/loeschen/', views.tisch_vorliebe_delete, name='tisch_vorliebe_delete'),

    # Sitzplan
    path('klasse/<int:klasse_pk>/berechnen/', views.sitzplan_berechnen, name='sitzplan_berechnen'),
    path('sitzplan/<int:pk>/', views.sitzplan_detail, name='sitzplan_detail'),
    path('sitzplan/<int:pk>/loeschen/', views.sitzplan_delete, name='sitzplan_delete'),
]
