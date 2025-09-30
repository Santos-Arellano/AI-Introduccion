# -*- coding: utf-8 -*-
"""
motor/propositional_resolution.py
=================================
Motor de **resolución por refutación** para **lógica proposicional**.

Cumple el algoritmo solicitado por la práctica:
1) Trabajar en CNF (conjunto de cláusulas).
2) Negar la meta y añadirla a la KB.
3) Mientras haya pares por resolver:
   - Buscar literales complementarios,
   - Generar resolventes y añadir si son nuevos.
4) Si se deriva `□` ⇒ la sentencia original es **verdadera**.
5) Si no hay más resoluciones ⇒ **falsa**.
6) Evita re-uso de pares y duplicados de cláusulas.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional, Set, Dict, Iterable, FrozenSet

Literal = str            # "A" o "~A"
Clause  = FrozenSet[str] # frozenset({"A","~B"})

# -----------------------------------------------------------------------------
# Estructura de traza para explicación en sustentación
# -----------------------------------------------------------------------------

@dataclass
class PropStep:
    iteration: int
    left_id: int
    right_id: int
    pivot_left: str
    pivot_right: str
    resolvent: Clause

# -----------------------------------------------------------------------------
# Utilidades
# -----------------------------------------------------------------------------

def neg(l: str) -> str:
    """Complemento de un literal: A <-> ~A."""
    return l[1:] if l.startswith("~") else "~" + l

def is_tautology(c: Clause) -> bool:
    """Una cláusula es tautológica si contiene un literal y su complemento."""
    return any(neg(l) in c for l in c)

def parse_clause_list(raw: Iterable[Iterable[str]]) -> List[Clause]:
    """Construye una lista de cláusulas desde listas de literales en texto."""
    return [frozenset(map(str, clause)) for clause in raw]

def pretty_clause(c: Clause) -> str:
    return " ∨ ".join(sorted(c)) if c else "□"

# -----------------------------------------------------------------------------
# Resolución proposicional
# -----------------------------------------------------------------------------

def resolve_propositional(clauses_init: Iterable[Clause], keep_steps: bool = True):
    """
    Ejecuta la resolución proposicional sobre una KB en CNF.
    Retorna: (entails_empty, derived_set, proof_map, steps)
    """
    clauses: List[Clause] = []
    seen: Set[Clause] = set()
    proof: Dict[Clause, Tuple[Clause, Clause]] = {}
    steps: List[PropStep] = []

    def add_clause(c: Clause, parents: Optional[Tuple[Clause, Clause]] = None) -> bool:
        if c in seen:
            return False
        seen.add(c); clauses.append(c)
        if parents: proof[c] = parents
        return True

    # Carga inicial
    for c in clauses_init:
        add_clause(frozenset(c))

    processed_pairs: Set[Tuple[int, int]] = set()
    iteration = 0

    while True:
        new_any = False
        iteration += 1

        for i in range(len(clauses)):
            for j in range(i+1, len(clauses)):
                key = (i, j)
                if key in processed_pairs: 
                    continue
                processed_pairs.add(key)

                Ci, Cj = clauses[i], clauses[j]

                # Para cada literal de Ci, busca su complemento en Cj
                for l in Ci:
                    comp = neg(l)
                    if comp not in Cj:
                        continue

                    # Resolvente = (Ci - {l}) ∪ (Cj - {~l})
                    R = (Ci - {l}) | (Cj - {comp})
                    if is_tautology(R):
                        continue

                    if keep_steps:
                        steps.append(PropStep(iteration, i, j, l, comp, R))

                    if not add_clause(R, parents=(Ci, Cj)):
                        continue

                    new_any = True
                    if len(R) == 0:
                        return True, set(clauses), proof, steps

        if not new_any:
            return False, set(clauses), proof, steps
