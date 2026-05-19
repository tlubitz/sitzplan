from ortools.sat.python import cp_model

schuelerInnen = ["lumina", "lilli", "otto_m", "eros", "justus", "constantin",
                 "clara", "luisa", "holly", "lotte", "nica", "luci", "elli", "juri", "benni", "noura",
                 "linda", "ella_l", "nova", "mila", "nuri", "otto_ls", "ilias", "alisha", "lucia"]

tische = {
    "tisch 1": 2,
    "tisch 2": 2,
    "tisch 3": 2,
    "tisch 4": 2,
    "tisch 5": 7,
    "tisch 6": 6,
    "tisch 7": 2,
    "tisch 8": 2    
}

vorlieben = { ("lumina", "lotte"): 10, ("lumina", "ella_l"): 10, ("lumina", "lucia"): 10, ("lumina", "holly"): 10,
    ("lilli", "lotte"): 10, ("lilli", "clara"): 10, ("lilli", "constantin"): 10, ("lilli", "lumina"): 10,
    ("otto_m", "eros"): 10, ("otto_m", "ilias"): 10, ("otto_m", "benni"): 10, ("otto_m", "justus"): 10,
    ("eros", "ilias"): 10, ("eros", "otto_m"): 10, ("eros", "benni"): 10, ("eros", "justus"): 10,
    ("justus", "benni"): 10, ("justus", "eros"): 10, ("justus", "constantin"): 10, ("justus", "nuri"): 10,
    ("constantin", "lilli"): 10, ("constantin", "justus"): 10, ("constantin", "juri"): 10, ("constantin", "lumina"): 10,
    ("clara", "luisa"): 10, ("clara", "luci"): 10, ("clara", "lotte"): 10, ("clara", "nica"): 10,
    ("luisa", "clara"): 10, ("luisa", "luci"): 10, ("luisa", "lotte"): 10, ("luisa", "nica"): 10,
    ("holly", "ella_l"): 10, ("holly", "lotte"): 10, ("holly", "lumina"): 10, ("holly", "mila"): 10,
    ("lotte", "luisa"): 10, ("lotte", "ella_l"): 10, ("lotte", "noura"): 10, ("lotte", "mila"): 10,
    ("nica", "luisa"): 10, ("nica", "luci"): 10, ("nica", "clara"): 10, ("nica", "lotte"): 10,
    ("luci", "clara"): 10, ("luci", "luisa"): 10, ("luci", "lotte"): 10, ("luci", "elli"): 10,
    ("elli", "clara"): 10, ("elli", "luisa"): 10, ("elli", "luci"): 10, ("elli", "lotte"): 10,
    ("juri", "ella_l"): 10, ("juri", "otto_m"): 10, ("juri", "nuri"): 10, ("juri", "constantin"): 10,
    ("benni", "ilias"): 10, ("benni", "otto_ls"): 10, ("benni", "nuri"): 10, ("benni", "justus"): 10,
    ("noura", "alisha"): 10, ("noura", "nova"): 10, ("noura", "mila"): 10, ("noura", "linda"): 10,
    ("linda", "ella_l"): 10, ("linda", "mila"): 10, ("linda", "nova"): 10, ("linda", "noura"): 10,
    ("ella_l", "linda"): 10, ("ella_l", "mila"): 10, ("ella_l", "nuri"): 10, ("ella_l", "otto_ls"): 10,
    ("nova", "mila"): 10, ("nova", "linda"): 10, ("nova", "alisha"): 10, ("nova", "noura"): 10,
    ("mila", "nova"): 10, ("mila", "ella_l"): 10, ("mila", "alisha"): 10, ("mila", "noura"): 10,
    ("nuri", "ella_l"): 10, ("nuri", "mila"): 10, ("nuri", "linda"): 10, ("nuri", "otto_ls"): 10,
    ("otto_ls", "ella_l"): 10, ("otto_ls", "mila"): 10, ("otto_ls", "linda"): 10, ("otto_ls", "nuri"): 10,
    ("ilias", "eros"): 10, ("ilias", "otto_ls"): 10, ("ilias", "nuri"): 10, ("ilias", "justus"): 10,
    ("alisha", "noura"): 10, ("alisha", "nova"): 10, ("alisha", "alisha"): 10, ("alisha", "linda"): 10,
    ("lucia", "mila"): 10, ("lucia", "nova"): 10, ("lucia", "ella_l"): 10, ("lucia", "lumina"): 10
}

verboten = {    
    ("justus", "nuri"),
    ("justus", "otto_ls"),
    ("justus", "lucia"),
    ("noura", "lucia"),
    ("noura", "ilias"),
    ("otto_ls", "ilias"),
    ("otto_ls", "lucia"),
    ("ilias", "lucia"),
    ("lucia", "eros"),
    ("lucia", "justus"),
}

tisch_vorlieben = {
    "lumina": {2: 10, 6: -10, 7: -10},
    "lilli": {2: 10, 6: -10, 7: -10},
    "otto_m": {2: 10, 6: 10, 7: 10},
    "eros": {2: -20, 6: 10, 7: 10},
    "justus": {2: 10, 6: 10, 7: 10},
    "constantin": {2: 10, 6: 10, 7: 10},
    "clara": {2: 10, 6: 10, 7: 10},
    "luisa": {2: 10, 6: 10, 7: 10},
    "holly": {2: 10, 6: 10, 7: 10},
    "lotte": {2: 10, 6: 10, 7: 10},
    "nica": {2: 10, 6: 10, 7: 10},
    "luci": {2: 10, 6: 10, 7: 10},
    "elli": {2: 10, 6: 10, 7: 10},
    "juri": {2: 10, 6: 10, 7: 10},
    "benni": {2: 10, 6: 10, 7: 10},
    "noura": {2: 10, 6: 10, 7: 10},
    "linda": {2: 10, 6: 10, 7: 10},
    "ella_l": {2: 10, 6: 10, 7: 10},
    "nova": {2: 10, 6: -10, 7: -10},
    "mila": {2: 10, 6: -10, 7: -10},
    "nuri": {2: -10, 6: 10, 7: 10},
    "otto_ls": {2: -10, 6: 10, 7: 10},
    "ilias": {2: -10, 6: 10, 7: 10},
    "alisha": {2: 10, 6: -10, 7: -10},
    "lucia": {2: 10, 6: 10, 7: 10}
}

print('Variablen fertig')


score = 0
model = cp_model.CpModel()

# x[pupil, table] = 1 if pupil sits at that table, else 0
x = {}

for schuelerIn in schuelerInnen:
    for tisch in tische:
        x[(schuelerIn, tisch)] = model.NewBoolVar(f"x_{schuelerIn}_{tisch}")


# Constraints/Bedingungen
for schuelerIn in schuelerInnen:
    model.Add(
        sum(x[(schuelerIn, tisch)] for tisch in tische) == 1
    )

for tisch, kapazitaet in tische.items():
    model.Add(
        sum(x[(schuelerIn, tisch)] for schuelerIn in schuelerInnen) <= kapazitaet
    )

for schuelerIn_a, schuelerIn_b in verboten:
    for tisch in tische:
        model.Add(
            x[(schuelerIn_a, tisch)] + x[(schuelerIn_b, tisch)] <= 1
        )


objective_terms = []
for (schuelerIn_a, schuelerIn_b), score in vorlieben.items():
    for tisch in tische:
        together = model.NewBoolVar(f"together_{schuelerIn_a}_{schuelerIn_b}_{tisch}")

        # together = 1 only if both pupils are at this table
        model.Add(together <= x[(schuelerIn_a, tisch)])
        model.Add(together <= x[(schuelerIn_b, tisch)])
        model.Add(together >= x[(schuelerIn_a, tisch)] + x[(schuelerIn_b, tisch)] - 1)

        objective_terms.append(score * together)


for schuelerIn in schuelerInnen:
    for tisch, kapazitaet in tische.items():
        size_score = tisch_vorlieben.get(schuelerIn, {}).get(kapazitaet, 0)

        if size_score != 0:
            objective_terms.append(size_score * x[(schuelerIn, tisch)])

model.Maximize(sum(objective_terms))



# now running the model to find the optimal seating arrangement
solver = cp_model.CpSolver()

# Optional: limit solving time
solver.parameters.max_time_in_seconds = 10

status = solver.Solve(model)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print("Lösung gefunden!")
    print("Gesamtglück:", solver.ObjectiveValue())
    print()

    for tisch in tische:
        seated_schuelerInnen = []

        for schuelerIn in schuelerInnen:
            if solver.Value(x[(schuelerIn, tisch)]) == 1:
                seated_schuelerInnen.append(schuelerIn)

        print(f"{tisch}: {', '.join(seated_schuelerInnen)}")

else:
    print("Keine Lösung gefunden")

