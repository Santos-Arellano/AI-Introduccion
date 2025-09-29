# -*- coding: utf-8 -*-
"""
==============================================
EJEMPLOS DE EJECUCIÓN - MOTOR DE INFERENCIA
==============================================
Imprime en la terminal dos demostraciones **ultra-explicadas**:
1) Resolución proposicional (sin variables)
2) Resolución de primer orden (con unificación) - Caso 'Marco'

Ejecuta: python examples/run_examples.py
"""

import sys
import os

# Permitimos importaciones desde la raíz del proyecto:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.propositional_resolution import (
    resolve_propositional, parse_clause_list, pretty_clause as pretty_prop, reconstruct_proof
)
from src.first_order_resolution import (
    resolve_first_order, L, Var, Const, pretty_clause as pretty_fo
)

# ---------- Utilidades de impresión didáctica ----------
def linea(titulo: str):
    print("\n" + "=" * 70)
    print(titulo)
    print("=" * 70)

def explica_resolucion_prop(steps):
    """
    Explica paso a paso la resolución proposicional:
    Qué par de cláusulas resolvemos, qué literales complementarios se usan,
    y cuál es el resolvente que se genera.
    """
    if not steps:
        print("  (No se generaron pasos intermedios.)")
        return
    print("\n🔎 Detalle paso a paso (proposicional):")
    for k, s in enumerate(steps, 1):
        print(f"\n  Paso {k} (iteración {s.iteration}):")
        print(f"    Cláusula 1: {pretty_prop(s.parent1)}")
        print(f"    Cláusula 2: {pretty_prop(s.parent2)}")
        print(f"    Literales complementarios: {s.resolved_lit}  vs  {s.resolved_compl}")
        if s.resolvent:
            print(f"    Resolvente: {pretty_prop(s.resolvent)}")
            print(f"    (Explicación: quitamos {s.resolved_lit} de la primera y {s.resolved_compl} de la segunda, "
                  f"y unimos lo que queda.)")
        else:
            print("    Resolvente: □ (cláusula vacía)")
            print("    (Explicación: al resolver l y ¬l, no queda ningún literal → contradicción)")

def formatea_theta(subst):
    """
    Sustitución θ en formato amigable: {x → Marco, y → f(a)}
    """
    if not subst:
        return "{}"
    pares = []
    for v, t in subst.items():
        pares.append(f"{v} → {t}")
    return "{ " + ", ".join(pares) + " }"

def explica_resolucion_fol(steps):
    """
    Explica paso a paso en Primer Orden:
    Muestra literales que unifican, la sustitución θ y el resolvente resultante.
    """
    if not steps:
        print("  (No se generaron pasos intermedios.)")
        return
    print("\n🔎 Detalle paso a paso (primer orden):")
    for k, s in enumerate(steps, 1):
        print(f"\n  Paso {k} (iteración {s.iteration}):")
        print(f"    Cláusula 1: {pretty_fo(s.parent1)}")
        print(f"    Cláusula 2: {pretty_fo(s.parent2)}")
        print(f"    Literales complementarios que UNIFICAN:")
        print(f"      • {s.lit1}")
        print(f"      • {s.lit2}")
        print(f"    Sustitución θ = {formatea_theta(s.subst)}")
        if s.resolvent:
            print(f"    Resolvente: {pretty_fo(s.resolvent)}")
            print("    (Explicación: eliminamos los literales complementarios y "
                  "aplicamos θ al resto de literales de ambas cláusulas.)")
        else:
            print("    Resolvente: □ (cláusula vacía)")
            print("    (Explicación: tras aplicar θ y eliminar los complementarios, no queda ningún literal → contradicción)")

# ------------------ EJEMPLO 1: PROPOSICIONAL ------------------
def ejemplo_proposicional():
    linea("EJEMPLO 1: RESOLUCIÓN PROPOSICIONAL (SIN VARIABLES)")

    print("\n📚 Problema (CNF):")
    print("  1) A ∨ B             (al menos una de A o B es verdadera)")
    print("  2) ¬A ∨ C            (si A, entonces C)")
    print("  3) ¬B                (B es falsa)")
    print("  4) ¬C                (C es falsa)")
    print("\n🎯 Pregunta: ¿es consistente este conjunto de afirmaciones?")

    raw = [["A", "B"], ["~A", "C"], ["~B"], ["~C"]]

    print("\n📝 Cláusulas iniciales:")
    for i, clause in enumerate(raw, 1):
        print(f"  {i}. {' ∨ '.join(clause)}")

    clauses = parse_clause_list(raw)

    print("\n⚙️ Ejecutando resolución proposicional (con pasos)...")
    print("-" * 70)
    entails, derived, proof, steps = resolve_propositional(clauses, keep_steps=True)
    print("-" * 70)

    explica_resolucion_prop(steps)

    if entails:
        print("\n✅ Resultado: ¡CONTRADICCIÓN ENCONTRADA! → '□'")
        print("   Conclusión: el conjunto de cláusulas es INCONSISTENTE.")
        empty = next(c for c in derived if len(c) == 0)
        order = reconstruct_proof(empty, proof)
        print("\n📊 Árbol resumido de derivación (premisas → ... → '□'):")
        for c in order:
            if c in proof:
                p1, p2 = proof[c]
                print(f"  {pretty_prop(c)}  ←  ({pretty_prop(p1)} , {pretty_prop(p2)})")
            else:
                print(f"  {pretty_prop(c)}  (premisa)")
    else:
        print("\n❌ No se encontró contradicción. Conjunto consistente.")

# ------------------ EJEMPLO 1B: TEOREMA PROPOSICIONAL ------------------
def ejemplo_teorema_proposicional():
    print("\n" + "=" * 70)
    print("EJEMPLO 1B: TEOREMA PROPOSICIONAL VIA REFUTACIÓN (probar C)")
    print("=" * 70)
    print("\nPremisas:")
    print("  1) A")
    print("  2) ¬A ∨ C   (A → C)")
    print("Meta: C   → trabajamos con {A, ¬A ∨ C, ¬C} y buscamos □")

    raw = [["A"], ["~A", "C"], ["~C"]]  # premisas + negación de la meta
    
    clauses = parse_clause_list(raw)
    entails, derived, proof, steps = resolve_propositional(clauses, keep_steps=True)

    # Explicación de pasos (como en el ejemplo 1)
    print("\nPasos:")
    for k, s in enumerate(steps, 1):
        print(f"  Paso {k}: ({pretty_prop(s.parent1)})  RES  ({pretty_prop(s.parent2)})")
        print(f"           l={s.resolved_lit}  vs  ~l={s.resolved_compl}  ⇒  {pretty_prop(s.resolvent)}")

    if entails:
        print("\n✅ Se derivó □ con ¬C en las premisas → C es consecuencia lógica de {A, ¬A∨C}.")
        empty = next(c for c in derived if len(c) == 0)
        order = reconstruct_proof(empty, proof)
        print("\nÁrbol resumido:")
        for c in order:
            if c in proof:
                p1, p2 = proof[c]
                print(f"  {pretty_prop(c)}  ←  ({pretty_prop(p1)} , {pretty_prop(p2)})")
            else:
                print(f"  {pretty_prop(c)}   (premisa)")
    else:
        print("\n❌ No se derivó contradicción (revisa las premisas).")

# ------------------ EJEMPLO 2: PRIMER ORDEN ------------------
def ejemplo_marco():
    linea("EJEMPLO 2: RESOLUCIÓN DE PRIMER ORDEN — CASO 'MARCO'")

    print("\n📚 Contexto lógico:")
    print("  • Axioma: ∀x (Humano(x) → Mortal(x))  ⇔  ¬Humano(x) ∨ Mortal(x)")
    print("  • Hecho : Humano(Marco)")
    print("  • Meta  : Mortal(Marco)  (probaremos por refutación agregando ¬Mortal(Marco))")

    clauses = {
        frozenset({ L("Humano", Const("Marco")) }),                         # Hecho
        frozenset({ L("Humano", Var("x"), neg=True), L("Mortal", Var("x")) }),  # Regla
        frozenset({ L("Mortal", Const("Marco"), neg=True) }),              # Negación de la meta
    }

    print("\n📝 Cláusulas en el sistema:")
    for i, c in enumerate(clauses, 1):
        print(f"  {i}. {pretty_fo(c)}")

    print("\n⚙️ Ejecutando resolución de primer orden (con pasos + θ)...")
    print("-" * 70)
    entail, derived, proof, steps = resolve_first_order(clauses, keep_steps=True)
    print("-" * 70)

    explica_resolucion_fol(steps)

    if entail:
        print("\n✅ Resultado: ¡CONTRADICCIÓN ENCONTRADA! → '□'")
        print("   Conclusión: Mortal(Marco) se deduce lógicamente de las premisas.")
        empty = next(c for c in derived if len(c) == 0)
        if empty in proof:
            p1, p2 = proof[empty]
            print("\n📌 Paso final que produce '□':")
            print(f"  {pretty_fo(p1)}")
            print(f"  {pretty_fo(p2)}")
    else:
        print("\n❌ No se derivó contradicción.")

        

# ------------------ MAIN ------------------
if __name__ == "__main__":
    ejemplo_proposicional()
    ejemplo_teorema_proposicional()  # ← opcional, recomendado
    ejemplo_marco()



