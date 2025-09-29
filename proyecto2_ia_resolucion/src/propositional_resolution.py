# -*- coding: utf-8 -*-
"""
===========================================================
RESOLUCIÓN POR REFUTACIÓN — LÓGICA PROPOSICIONAL (SIN VARIABLES)
===========================================================

Este módulo implementa la regla de resolución para lógica proposicional:
- Literal = "A" o "~A" (negación con ~).
- Cláusula = disyunción (OR) de literales, representada como 'frozenset[str]'.
- Conjunto de cláusulas en **CNF** (AND de cláusulas).

NOVEDAD (para impresión didáctica):
- Guardamos una lista de "pasos" (PropStep) con:
  * pares de cláusulas resueltas,
  * literales complementarios usados,
  * resolvente obtenido,
  * número de iteración.

Así luego podemos explicar cada paso en la terminal de forma clara.
"""

from dataclasses import dataclass
from typing import Set, FrozenSet, Tuple, Dict, List, Optional

# ---------- Tipos básicos ----------
Literal = str               # p.ej. "A" o "~A"
Clause = FrozenSet[Literal] # p.ej. frozenset({"A","B"})

# ---------- Paso de resolución (para explicar) ----------
@dataclass
class PropStep:
    iteration: int                # número de iteración del bucle principal
    parent1: Clause               # cláusula 1
    parent2: Clause               # cláusula 2
    resolved_lit: Literal         # literal l en parent1 que se resolvió
    resolved_compl: Literal       # literal complementario ~l en parent2
    resolvent: Clause             # cláusula resultante


# ---------- Helpers de literales ----------
def is_neg(l: Literal) -> bool:
    """Indica si el literal está negado ('~X')."""
    return l.startswith("~")


def negate(l: Literal) -> Literal:
    """Niega un literal: A -> ~A, ~A -> A."""
    return l[1:] if is_neg(l) else "~" + l


# ---------- I/O de cláusulas ----------
def parse_clause_list(raw: List[List[str]]) -> Set[Clause]:
    """
    Convierte listas de literales a un conjunto de cláusulas inmutables.
    Ejemplo:
      raw = [["A","B"], ["~A","C"], ["~B"], ["~C"]]
    """
    return set(frozenset(map(str.strip, clause)) for clause in raw)


# ---------- Regla de resolución proposicional ----------
def _resolvents_with_witness(c1: Clause, c2: Clause):
    """
    Genera (resolvent, literal_elegido, complemento) para cada emparejamiento válido.
    Esto nos permite registrar EXACTAMENTE qué par de literales se usó.
    """
    for l in c1:
        comp = negate(l)
        if comp in c2:
            resolvent = frozenset((c1 - {l}) | (c2 - {comp}))
            yield resolvent, l, comp


# ---------- Motor de resolución por refutación ----------
def resolve_propositional(
    clauses: Set[Clause],
    max_iterations: int = 5000,
    keep_steps: bool = True
):
    """
    Ejecuta la saturación por resolución.
    - Si 'keep_steps' es True, también devuelve la lista de pasos PropStep.

    Retorna:
      - entailment (bool): True si se deriva la cláusula vacía '□' (frozenset()).
      - derived (Set[Clause]): todas las cláusulas conocidas (iniciales + derivadas).
      - proof (Dict[Clause, Tuple[Clause, Clause]]): padres de cada resolvente.
      - steps (List[PropStep]) [solo si keep_steps=True]: traza de pasos.
    """
    derived = set(clauses)
    proof: Dict[Clause, Tuple[Clause, Clause]] = {}
    steps: List[PropStep] = []
    new = set()
    processed_pairs = set()

    iteration = 0
    while iteration < max_iterations:
        iteration += 1
        items = list(derived)

        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                c1, c2 = items[i], items[j]
                if (c1, c2) in processed_pairs:
                    continue
                processed_pairs.add((c1, c2))

                # Generamos resolventes junto con evidencia del literal complementario usado
                for resolvent, l, comp in _resolvents_with_witness(c1, c2):
                    # Registramos el paso para explicarlo luego
                    if keep_steps:
                        steps.append(PropStep(
                            iteration=iteration,
                            parent1=c1, parent2=c2,
                            resolved_lit=l, resolved_compl=comp,
                            resolvent=resolvent
                        ))

                    if not resolvent:  # '□' -> éxito inmediato
                        proof[resolvent] = (c1, c2)
                        derived.add(resolvent)
                        return True, derived, proof, steps

                    if resolvent not in derived and resolvent not in new:
                        new.add(resolvent)
                        proof[resolvent] = (c1, c2)

        if new.issubset(derived):  # punto fijo: no hay nada nuevo
            return False, derived, proof, steps

        derived |= new
        new = set()

    # Límite alcanzado sin '□'
    return False, derived, proof, steps


# ---------- Pretty-print y reconstrucción de prueba ----------
def pretty_clause(c: Clause) -> str:
    """Devuelve una cadena legible para una cláusula; vacía = '□'."""
    return " ∨ ".join(sorted(c)) if c else "□"


def reconstruct_proof(empty_clause: Clause, proof: Dict[Clause, Tuple[Clause, Clause]]) -> List[Clause]:
    """
    Reconstruye un orden plausible de derivación partiendo desde '□'.
    Inserta primero premisas, luego resolventes, y al final '□'.
    """
    order: List[Clause] = []
    stack = [empty_clause]
    visited = set()

    while stack:
        c = stack.pop()
        if c in visited:
            continue
        visited.add(c)
        order.append(c)
        if c in proof:
            p1, p2 = proof[c]
            stack.extend([p1, p2])

    return list(reversed(order))
