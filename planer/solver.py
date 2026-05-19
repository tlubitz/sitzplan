"""
OR-Tools CP-SAT solver that computes an optimal seating plan for a Klasse.

Call `solve(klasse)` which returns a dict:
    {
        "status": "solved" | "infeasible",
        "gesamt_glueck": float,
        "zuweisungen": [(schuelerIn_id, tisch_id), ...],
    }
"""

from ortools.sat.python import cp_model

from .models import Klasse, Sitzplan, Zuweisung


def solve(klasse: Klasse, max_seconds: int = 30) -> dict:
    schuelerinnen = list(klasse.schuelerinnen.all())
    tische = list(klasse.tische.all())

    if not schuelerinnen:
        return {"status": "infeasible", "gesamt_glueck": None, "zuweisungen": []}
    if not tische:
        return {"status": "infeasible", "gesamt_glueck": None, "zuweisungen": []}

    # Index lists for faster lookup
    s_ids = [s.id for s in schuelerinnen]
    t_ids = [t.id for t in tische]
    t_kap = {t.id: t.kapazitaet for t in tische}

    model = cp_model.CpModel()

    # x[(s_id, t_id)] = 1 if pupil sits at table
    x = {}
    for s_id in s_ids:
        for t_id in t_ids:
            x[(s_id, t_id)] = model.NewBoolVar(f"x_{s_id}_{t_id}")

    # Every pupil sits at exactly one table
    for s_id in s_ids:
        model.Add(sum(x[(s_id, t_id)] for t_id in t_ids) == 1)

    # Capacity constraints
    for t_id, kap in t_kap.items():
        model.Add(sum(x[(s_id, t_id)] for s_id in s_ids) <= kap)

    # Forbidden pairs
    for v in klasse.verboten.select_related('schuelerIn_a', 'schuelerIn_b'):
        a, b = v.schuelerIn_a_id, v.schuelerIn_b_id
        if a in s_ids and b in s_ids:
            for t_id in t_ids:
                model.Add(x[(a, t_id)] + x[(b, t_id)] <= 1)

    objective_terms = []

    # Preference scores between pairs
    for pref in klasse.vorlieben.select_related('schuelerIn_a', 'schuelerIn_b'):
        a, b = pref.schuelerIn_a_id, pref.schuelerIn_b_id
        if a not in s_ids or b not in s_ids:
            continue
        for t_id in t_ids:
            together = model.NewBoolVar(f"tog_{a}_{b}_{t_id}")
            model.Add(together <= x[(a, t_id)])
            model.Add(together <= x[(b, t_id)])
            model.Add(together >= x[(a, t_id)] + x[(b, t_id)] - 1)
            objective_terms.append(pref.score * together)

    # Table-size preferences
    for tv in klasse.tisch_vorlieben.select_related('schuelerIn'):
        s_id = tv.schuelerIn_id
        if s_id not in s_ids or tv.score == 0:
            continue
        for t_id in t_ids:
            if t_kap[t_id] == tv.kapazitaet:
                objective_terms.append(tv.score * x[(s_id, t_id)])

    model.Maximize(sum(objective_terms))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = max_seconds
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        zuweisungen = []
        for s_id in s_ids:
            for t_id in t_ids:
                if solver.Value(x[(s_id, t_id)]) == 1:
                    zuweisungen.append((s_id, t_id))
                    break
        return {
            "status": "solved",
            "gesamt_glueck": solver.ObjectiveValue(),
            "zuweisungen": zuweisungen,
        }
    else:
        return {"status": "infeasible", "gesamt_glueck": None, "zuweisungen": []}


def solve_and_save(klasse: Klasse, max_seconds: int = 30) -> Sitzplan:
    """Run the solver and persist the result as a Sitzplan with Zuweisungen."""
    result = solve(klasse, max_seconds)

    sitzplan = Sitzplan.objects.create(
        klasse=klasse,
        gesamt_glueck=result["gesamt_glueck"],
        status=result["status"],
    )

    if result["status"] == "solved":
        tisch_map = {t.id: t for t in klasse.tische.all()}
        schueler_map = {s.id: s for s in klasse.schuelerinnen.all()}
        Zuweisung.objects.bulk_create([
            Zuweisung(sitzplan=sitzplan, schuelerIn=schueler_map[s_id], tisch=tisch_map[t_id])
            for s_id, t_id in result["zuweisungen"]
        ])

    return sitzplan
