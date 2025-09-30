# -*- coding: utf-8 -*-
"""
examples/run_examples.py
========================
Demostraciones ejecutables del **Proyecto 2 - Sustentación**:

1) Ejemplo proposicional inconsistente (deriva `□`).
2) Caso "¿La curiosidad mató a Tuna?" (FOL) que demuestra `Muerto(Tuna)` por refutación.
"""

from __future__ import annotations

from motor.propositional_resolution import resolve_propositional, parse_clause_list, pretty_clause
from motor.first_order_resolution import resolve_first_order, L, pretty_clause as pretty_clause_fol
from motor.unification import Var, Const

# -----------------------------------------------------------------------------
# Impresión de pasos (trazas) para sustentación
# -----------------------------------------------------------------------------

def show_prop_steps(steps):
    print("\n--- Traza (proposicional) ---")
    for st in steps:
        print(f"[it={st.iteration}] C{st.left_id} ⟂ C{st.right_id}   usando {st.pivot_left} / {st.pivot_right}   ⇒   {pretty_clause(st.resolvent)}")

def show_fol_steps(steps):
    print("\n--- Traza (1er orden) ---")
    for st in steps:
        theta_str = ", ".join(f"{v.name}←{t}" for v, t in st.theta.items())
        print(f"[it={st.iteration}] C{st.left_id} ⟂ C{st.right_id}   con ({st.left_lit}) & ({st.right_lit})   θ={{ {theta_str} }}   ⇒   {pretty_clause_fol(st.resolvent)}")

# -----------------------------------------------------------------------------
# 1) Ejemplo proposicional
# -----------------------------------------------------------------------------

def example_propositional():
    print("=== EJEMPLO PROPOSICIONAL ===")
    # CNF: (A ∨ B), (¬A), (¬B)  → inconsistente
    raw = [["A", "B"], ["~A"], ["~B"]]
    clauses = parse_clause_list(raw)

    entails, derived, proof, steps = resolve_propositional(clauses, keep_steps=True)
    show_prop_steps(steps)
    print("\nResultado:", "□ derivada → contradicción (inconsistente)" if entails else "No contradicción")

# -----------------------------------------------------------------------------
# 2) Caso "¿La curiosidad mató a Tuna?" (FOL)
# -----------------------------------------------------------------------------

def example_tuna():
    print("\n=== CASO: ¿La curiosidad mató a Tuna? (1ER ORDEN) ===")
    # Axiomas en CNF + negación de la meta Muerto(Tuna)
    # 1) Curioso(x) → Mata(Curiosidad, x)   ⇒  ¬Curioso(x) ∨ Mata(Curiosidad, x)
    # 2) Mata(y, x) → Muerto(x)            ⇒  ¬Mata(y, x) ∨ Muerto(x)
    # 3) Gato(Tuna)
    # 4) Gato(x) → Curioso(x)              ⇒  ¬Gato(x) ∨ Curioso(x)
    # 5) ¬Muerto(Tuna)                     (negación de la meta)

    x1, x2, x3, y1 = Var("x1"), Var("x2"), Var("x3"), Var("y1")
    Tuna = Const("Tuna"); Curiosidad = Const("Curiosidad")

    C1 = frozenset({ L("Curioso", x1, neg=True),        L("Mata", Curiosidad, x1) })
    C2 = frozenset({ L("Mata", y1, x2, neg=True),       L("Muerto", x2) })
    C3 = frozenset({ L("Gato", Tuna) })
    C4 = frozenset({ L("Gato", x3, neg=True),           L("Curioso", x3) })
    C5 = frozenset({ L("Muerto", Tuna, neg=True) })  # ¬Meta

    clauses = [C1, C2, C3, C4, C5]

    entails, derived, proof, steps = resolve_first_order(clauses, keep_steps=True)
    show_fol_steps(steps)
    print("\nResultado:", "□ derivada → 'Muerto(Tuna)' es verdadera" if entails else "No se pudo derivar '□'")

if __name__ == "__main__":
    example_propositional()
    example_tuna()
