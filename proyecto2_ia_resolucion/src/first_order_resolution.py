# -*- coding: utf-8 -*-
"""
==========================================================
RESOLUCIÓN DE PRIMER ORDEN (UNIFICACIÓN + ESTANDARIZACIÓN)
==========================================================

Extiende la resolución proposicional para manejar variables y términos.
NOVEDAD (para impresión didáctica):
- Guardamos pasos (FolStep) con:
  * las DOS cláusulas resueltas,
  * los DOS literales complementarios concretos,
  * la sustitución θ (MGU) usada,
  * el resolvente resultante,
  * la iteración.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Dict, List, Set, FrozenSet, Optional
from .unification import Var, Const, Func, Term, unify, apply_subst_term

# ---------- Predicados / Literales / Cláusulas ----------
@dataclass(frozen=True)
class Pred:
    name: str
    args: Tuple[Term, ...]
    def __str__(self) -> str:
        return f"{self.name}({', '.join(map(str, self.args))})" if self.args else self.name

@dataclass(frozen=True)
class Literal:
    pred: Pred
    negated: bool = False
    def __str__(self) -> str:
        return ("¬" if self.negated else "") + str(self.pred)

Clause = FrozenSet[Literal]

# ---------- Paso de resolución (para explicar) ----------
@dataclass
class FolStep:
    iteration: int
    parent1: Clause
    parent2: Clause
    lit1: Literal              # literal en c1
    lit2: Literal              # literal en c2 (complementario de lit1)
    subst: Dict[Var, Term]     # MGU
    resolvent: Clause          # cláusula derivada


# ---------- Sustituciones a literales/cláusulas ----------
def apply_subst_literal(l: Literal, subst: Dict[Var, Term]) -> Literal:
    """Aplica sustitución Var->Term a todos los argumentos del literal."""
    new_args = tuple(apply_subst_term(a, subst) for a in l.pred.args)
    return Literal(Pred(l.pred.name, new_args), l.negated)


def apply_subst_clause(c: Clause, subst: Dict[Var, Term]) -> Clause:
    """Aplica una sustitución a toda la cláusula."""
    return frozenset(apply_subst_literal(l, subst) for l in c)


# ---------- Estandarización-aparte ----------
class _VarGen:
    """Genera nombres frescos de variables (x1, x2, V3, ...)."""
    def __init__(self) -> None:
        self._i = 0
    def fresh(self, base: str = "V") -> Var:
        self._i += 1
        return Var(f"{base}{self._i}")


def vars_in_term(t: Term) -> Set[Var]:
    if isinstance(t, Var): return {t}
    if isinstance(t, Const): return set()
    vs: Set[Var] = set()
    for a in t.args: vs |= vars_in_term(a)
    return vs


def vars_in_literal(l: Literal) -> Set[Var]:
    vs: Set[Var] = set()
    for a in l.pred.args: vs |= vars_in_term(a)
    return vs


def vars_in_clause(c: Clause) -> Set[Var]:
    vs: Set[Var] = set()
    for l in c: vs |= vars_in_literal(l)
    return vs


def standardize_apart(c: Clause, vargen: _VarGen, used: Set[str]) -> Clause:
    """
    Renombra variables para evitar colisiones entre cláusulas distintas.
    Mantiene la coherencia dentro de la misma cláusula.
    """
    mapping: Dict[Var, Var] = {}
    for v in vars_in_clause(c):
        base = v.name if (v.name and v.name[0].islower()) else "V"
        nv = vargen.fresh(base)
        while nv.name in used:
            nv = vargen.fresh(base)
        mapping[v] = nv
        used.add(nv.name)
    return apply_subst_clause(c, mapping)


# ---------- Unificación de literales complementarios ----------
def unify_complement(l1: Literal, l2: Literal) -> Optional[Dict[Var, Term]]:
    """
    Devuelve θ (MGU) si l1 y l2:
      - tienen signos opuestos,
      - mismo predicado,
      - misma aridad,
      - y sus argumentos unifican.
    En caso contrario, retorna None.
    """
    if l1.negated == l2.negated:             # signos opuestos
        return None
    if l1.pred.name != l2.pred.name:         # mismo predicado
        return None
    if len(l1.pred.args) != len(l2.pred.args):  # misma aridad
        return None

    subst: Dict[Var, Term] = {}
    for a, b in zip(l1.pred.args, l2.pred.args):
        subst = unify(a, b, subst)
        if subst is None:
            return None
    return subst


# ---------- Resolventes y motor principal ----------
def _resolvents_with_witness(c1: Clause, c2: Clause):
    """
    Genera tuplas (resolvent, lit1, lit2, subst) para cada par de literales
    complementarios que unifican. Esto alimenta la traza didáctica.
    """
    for l1 in c1:
        for l2 in c2:
            subst = unify_complement(l1, l2)
            if subst is not None:
                rest = (c1 - {l1}) | (c2 - {l2})
                res = apply_subst_clause(frozenset(rest), subst)
                yield frozenset(res), l1, l2, subst


def resolve_first_order(
    clauses: Set[Clause],
    max_iterations: int = 5000,
    keep_steps: bool = True
):
    """
    Resolución por refutación en primer orden.
    Retorna:
      - entail (bool), derived (Set[Clause]), proof (Dict), steps (List[FolStep] si keep_steps=True)
    """
    vargen = _VarGen()
    used: Set[str] = set()

    # Estandarizamos las iniciales
    std: Set[Clause] = set()
    for c in clauses:
        std.add(standardize_apart(c, vargen, used))

    derived = set(std)
    proof: Dict[Clause, Tuple[Clause, Clause]] = {}
    steps: List[FolStep] = []
    processed_pairs = set()
    new: Set[Clause] = set()

    it = 0
    while it < max_iterations:
        it += 1
        lst = list(derived)
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                c1, c2 = lst[i], lst[j]
                if (c1, c2) in processed_pairs:
                    continue
                processed_pairs.add((c1, c2))

                # Estandarización extra por par (seguridad)
                sc1 = standardize_apart(c1, vargen, used)
                sc2 = standardize_apart(c2, vargen, used)

                for res, l1, l2, subst in _resolvents_with_witness(sc1, sc2):
                    if keep_steps:
                        steps.append(FolStep(
                            iteration=it,
                            parent1=c1, parent2=c2,   # referenciamos las "versiones" base
                            lit1=l1, lit2=l2,
                            subst=subst,
                            resolvent=res
                        ))

                    if not res:  # '□'
                        proof[res] = (c1, c2)
                        derived.add(res)
                        return True, derived, proof, steps

                    if res not in derived and res not in new:
                        new.add(res)
                        proof[res] = (c1, c2)

        if new.issubset(derived):
            return False, derived, proof, steps

        derived |= new
        new = set()

    return False, derived, proof, steps


# ---------- Helpers de construcción e impresión ----------
def L(name: str, *args, neg: bool = False) -> Literal:
    """Constructor directo de literales: L("Mortal", Const("Marco")) == Mortal(Marco)"""
    return Literal(Pred(name, tuple(args)), neg)


def pretty_clause(c: Clause) -> str:
    """Impresión legible; '□' para vacía."""
    return " ∨ ".join(sorted(map(str, c))) if c else "□"
