from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .models import Klasse, Tisch, SchuelerIn, Vorliebe, Verboten, TischVorliebe, Sitzplan
from .forms import (
    KlasseForm, TischForm, SchuelerInForm,
    VorliebeForm, VerbotenForm, TischVorliebeForm,
)
from .solver import solve_and_save


# ── Klassen ────────────────────────────────────────────────────────────────────

@login_required
def klassen_list(request):
    klassen = Klasse.objects.prefetch_related('schuelerinnen', 'tische').order_by('name')
    form = KlasseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Klasse erstellt.')
        return redirect('klassen_list')
    return render(request, 'planer/klassen_list.html', {'klassen': klassen, 'form': form})


@login_required
def klasse_detail(request, pk):
    klasse = get_object_or_404(Klasse, pk=pk)
    schuelerinnen = klasse.schuelerinnen.order_by('name')
    tische = klasse.tische.order_by('name')
    vorlieben = klasse.vorlieben.select_related('schuelerIn_a', 'schuelerIn_b')
    verboten = klasse.verboten.select_related('schuelerIn_a', 'schuelerIn_b')
    tisch_vorlieben = klasse.tisch_vorlieben.select_related('schuelerIn')
    sitzplaene = klasse.sitzplaene.order_by('-created_at')[:10]
    return render(request, 'planer/klasse_detail.html', {
        'klasse': klasse,
        'schuelerinnen': schuelerinnen,
        'tische': tische,
        'vorlieben': vorlieben,
        'verboten': verboten,
        'tisch_vorlieben': tisch_vorlieben,
        'sitzplaene': sitzplaene,
    })


@login_required
def klasse_delete(request, pk):
    klasse = get_object_or_404(Klasse, pk=pk)
    if request.method == 'POST':
        klasse.delete()
        messages.success(request, 'Klasse gelöscht.')
        return redirect('klassen_list')
    return render(request, 'planer/confirm_delete.html', {'object': klasse, 'cancel_url': 'klassen_list'})


# ── Tische ─────────────────────────────────────────────────────────────────────

@login_required
def tisch_add(request, klasse_pk):
    klasse = get_object_or_404(Klasse, pk=klasse_pk)
    form = TischForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        tisch = form.save(commit=False)
        tisch.klasse = klasse
        tisch.save()
        messages.success(request, f'Tisch „{tisch.name}" hinzugefügt.')
        return redirect('klasse_detail', pk=klasse_pk)
    return render(request, 'planer/form_page.html', {
        'form': form, 'title': 'Tisch hinzufügen', 'klasse': klasse,
    })


@login_required
def tisch_delete(request, klasse_pk, pk):
    tisch = get_object_or_404(Tisch, pk=pk, klasse_id=klasse_pk)
    if request.method == 'POST':
        tisch.delete()
        messages.success(request, 'Tisch gelöscht.')
        return redirect('klasse_detail', pk=klasse_pk)
    return render(request, 'planer/confirm_delete.html', {
        'object': tisch, 'cancel_url': 'klasse_detail', 'cancel_pk': klasse_pk,
    })


# ── SchülerInnen ───────────────────────────────────────────────────────────────

@login_required
def schuelerIn_add(request, klasse_pk):
    klasse = get_object_or_404(Klasse, pk=klasse_pk)
    form = SchuelerInForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        s = form.save(commit=False)
        s.klasse = klasse
        s.save()
        messages.success(request, f'Schüler*in „{s.name}" hinzugefügt.')
        return redirect('klasse_detail', pk=klasse_pk)
    return render(request, 'planer/form_page.html', {
        'form': form, 'title': 'Schüler*in hinzufügen', 'klasse': klasse,
    })


@login_required
def schuelerIn_delete(request, klasse_pk, pk):
    s = get_object_or_404(SchuelerIn, pk=pk, klasse_id=klasse_pk)
    if request.method == 'POST':
        s.delete()
        messages.success(request, 'Schüler*in gelöscht.')
        return redirect('klasse_detail', pk=klasse_pk)
    return render(request, 'planer/confirm_delete.html', {
        'object': s, 'cancel_url': 'klasse_detail', 'cancel_pk': klasse_pk,
    })


# ── Vorlieben ──────────────────────────────────────────────────────────────────

@login_required
def vorliebe_add(request, klasse_pk):
    klasse = get_object_or_404(Klasse, pk=klasse_pk)
    form = VorliebeForm(request.POST or None, klasse=klasse)
    if request.method == 'POST' and form.is_valid():
        v = form.save(commit=False)
        v.klasse = klasse
        v.save()
        messages.success(request, 'Vorliebe gespeichert.')
        return redirect('klasse_detail', pk=klasse_pk)
    return render(request, 'planer/form_page.html', {
        'form': form, 'title': 'Vorliebe hinzufügen', 'klasse': klasse,
    })


@login_required
def vorliebe_delete(request, klasse_pk, pk):
    v = get_object_or_404(Vorliebe, pk=pk, klasse_id=klasse_pk)
    if request.method == 'POST':
        v.delete()
        return redirect('klasse_detail', pk=klasse_pk)
    return render(request, 'planer/confirm_delete.html', {
        'object': v, 'cancel_url': 'klasse_detail', 'cancel_pk': klasse_pk,
    })


# ── Verboten ───────────────────────────────────────────────────────────────────

@login_required
def verboten_add(request, klasse_pk):
    klasse = get_object_or_404(Klasse, pk=klasse_pk)
    form = VerbotenForm(request.POST or None, klasse=klasse)
    if request.method == 'POST' and form.is_valid():
        v = form.save(commit=False)
        v.klasse = klasse
        v.save()
        messages.success(request, 'Verbotene Kombination gespeichert.')
        return redirect('klasse_detail', pk=klasse_pk)
    return render(request, 'planer/form_page.html', {
        'form': form, 'title': 'Verbotene Kombination hinzufügen', 'klasse': klasse,
    })


@login_required
def verboten_delete(request, klasse_pk, pk):
    v = get_object_or_404(Verboten, pk=pk, klasse_id=klasse_pk)
    if request.method == 'POST':
        v.delete()
        return redirect('klasse_detail', pk=klasse_pk)
    return render(request, 'planer/confirm_delete.html', {
        'object': v, 'cancel_url': 'klasse_detail', 'cancel_pk': klasse_pk,
    })


# ── TischVorlieben ─────────────────────────────────────────────────────────────

@login_required
def tisch_vorliebe_add(request, klasse_pk):
    klasse = get_object_or_404(Klasse, pk=klasse_pk)
    form = TischVorliebeForm(request.POST or None, klasse=klasse)
    if request.method == 'POST' and form.is_valid():
        tv = form.save(commit=False)
        tv.klasse = klasse
        tv.save()
        messages.success(request, 'Tischvorliebe gespeichert.')
        return redirect('klasse_detail', pk=klasse_pk)
    return render(request, 'planer/form_page.html', {
        'form': form, 'title': 'Tischvorliebe hinzufügen', 'klasse': klasse,
    })


@login_required
def tisch_vorliebe_delete(request, klasse_pk, pk):
    tv = get_object_or_404(TischVorliebe, pk=pk, klasse_id=klasse_pk)
    if request.method == 'POST':
        tv.delete()
        return redirect('klasse_detail', pk=klasse_pk)
    return render(request, 'planer/confirm_delete.html', {
        'object': tv, 'cancel_url': 'klasse_detail', 'cancel_pk': klasse_pk,
    })


# ── Solver ─────────────────────────────────────────────────────────────────────

@login_required
def sitzplan_berechnen(request, klasse_pk):
    klasse = get_object_or_404(Klasse, pk=klasse_pk)
    if request.method == 'POST':
        sitzplan = solve_and_save(klasse)
        if sitzplan.status == 'solved':
            messages.success(request, f'Sitzplan berechnet! Gesamtglück: {sitzplan.gesamt_glueck:.0f}')
        else:
            messages.error(request, 'Keine Lösung gefunden. Bitte Bedingungen überprüfen.')
        return redirect('sitzplan_detail', pk=sitzplan.pk)
    return redirect('klasse_detail', pk=klasse_pk)


@login_required
def sitzplan_detail(request, pk):
    sitzplan = get_object_or_404(
        Sitzplan.objects.select_related('klasse').prefetch_related(
            'zuweisungen__schuelerIn', 'zuweisungen__tisch'
        ),
        pk=pk,
    )
    # Group assignments by table
    tische_map = {}
    for z in sitzplan.zuweisungen.all():
        tische_map.setdefault(z.tisch, []).append(z.schuelerIn)

    return render(request, 'planer/sitzplan_detail.html', {
        'sitzplan': sitzplan,
        'tische_map': tische_map,
    })


@login_required
def sitzplan_delete(request, pk):
    sitzplan = get_object_or_404(Sitzplan, pk=pk)
    klasse_pk = sitzplan.klasse_id
    if request.method == 'POST':
        sitzplan.delete()
        messages.success(request, 'Sitzplan gelöscht.')
        return redirect('klasse_detail', pk=klasse_pk)
    return render(request, 'planer/confirm_delete.html', {
        'object': sitzplan, 'cancel_url': 'klasse_detail', 'cancel_pk': klasse_pk,
    })
