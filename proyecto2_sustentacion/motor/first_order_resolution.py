# -*- coding: utf-8 -*-
"""
motor/first_order_resolution.py
===============================
Motor de **resolución por refutación** para Lógica de Primer Orden (FOL).

Este módulo implementa exactamente el paso a paso indicado por la asignación:

1) Trabajar con la base de conocimiento en **Forma Normal Conjuntiva (CNF)**.
   - Cada cláusula es una disyunción de literales; la KB es un conjunto de cláusulas.
2) **Negar la meta** a demostrar y añadirla a la KB (también en CNF).
3) Mientras haya cláusulas por resolver:
   - Estandarizar-aparte el par (renombrar variables con sufijos únicos).
   - Seleccionar literales complementarios (mismo predicado, signos opuestos).
   - Intentar **unificar** sus argumentos (Robinson + occurs-check).
   - Construir el **resolvente** aplicando la MGU θ al resto de literales.
   - Añadir el resolvente si **no** es tautológico ni duplicado.
4) Si se deriva la **cláusula vacía `□`**, detener y reportar que la sentencia original es **verdadera**.
5) Si ya no se generan nuevas cláusulas, **detener y reportar falsa**.
6) El sistema evita **validar varias veces** reglas/pares ya usados con un conjunto `processed_pairs`.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Set, Iterable
from motor.unification import Var, Const, Func, Term, Subst, unify, apply_subst_term

# -----------------------------------------------------------------------------
# Predicados, literales y cláusulas (FOL)
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class Pred:
    """Símbolo de predicado con sus argumentos (términos)."""
    name: str
    args: Tuple[Term, ...]
    def __str__(self) -> str:
        if not self.args: return self.name
        return f'{self.name}({", ".join(map(str, self.args))})'

@dataclass(frozen=True)
class Literal:
    """Literal = predicado con posible negación."""
    pred: Pred
    neg: bool = False
    def __str__(self) -> str:
        s = str(self.pred)
        return f'¬{s}' if self.neg else s
    def negate(self) -> "Literal":
        return Literal(self.pred, not self.neg)

Clause = frozenset[Literal]

# -----------------------------------------------------------------------------
# Sustituciones a nivel de predicados/literales/cláusulas
# -----------------------------------------------------------------------------

def apply_subst_pred(p: Pred, s: Subst) -> Pred:
    return Pred(p.name, tuple(apply_subst_term(a, s) for a in p.args))

def apply_subst_lit(l: Literal, s: Subst) -> Literal:
    return Literal(apply_subst_pred(l.pred, s), l.neg)

def apply_subst_clause(c: Clause, s: Subst) -> Clause:
    return frozenset(apply_subst_lit(l, s) for l in c)

# -----------------------------------------------------------------------------
# Variables y renombrado (estandarización-aparte)
# -----------------------------------------------------------------------------

def vars_in_term(t: Term) -> Set[Var]:
    if isinstance(t, Var): return {t}
    if isinstance(t, Const): return set()
    vs: Set[Var] = set()
    if isinstance(t, Func):
        for a in t.args:
            vs |= vars_in_term(a)
    return vs

def vars_in_pred(p: Pred) -> Set[Var]:
    vs: Set[Var] = set()
    for a in p.args: vs |= vars_in_term(a)
    return vs

def vars_in_clause(c: Clause) -> Set[Var]:
    vs: Set[Var] = set()
    for l in c: vs |= vars_in_pred(l.pred)
    return vs

def rename_vars_clause(c: Clause, ren: Dict[Var, Var]) -> Clause:
    def ren_term(t: Term) -> Term:
        if isinstance(t, Var): return ren.get(t, t)
        if isinstance(t, Const): return t
        return Func(t.name, tuple(ren_term(a) for a in t.args))
    def ren_pred(p: Pred) -> Pred:
        return Pred(p.name, tuple(ren_term(a) for a in p.args))
    def ren_lit(l: Literal) -> Literal:
        return Literal(ren_pred(l.pred), l.neg)
    return frozenset(ren_lit(l) for l in c)

def standardize_apart(c: Clause, suffix: str) -> Clause:
    """Renombra variables con un sufijo único para evitar colisiones entre cláusulas."""
    ren: Dict[Var, Var] = {}
    for v in vars_in_clause(c):
        ren[v] = Var(f'{v.name}_{suffix}')
    return rename_vars_clause(c, ren)

# -----------------------------------------------------------------------------
# Otras utilidades: complementarios, tautologías, forma canónica, pretty print
# -----------------------------------------------------------------------------

def literal_complementary(a: Literal, b: Literal) -> bool:
    """Retorna True si a y b son el mismo predicado (misma aridad) y signos opuestos."""
    return (a.pred.name == b.pred.name) and (a.neg != b.neg) and (len(a.pred.args) == len(b.pred.args))

def is_tautology(c: Clause) -> bool:
    """
    Una cláusula es tautológica si contiene un literal y su negación con los mismos argumentos.
    Se verifica tras aplicar θ al resolvente.
    """
    seen = {}
    for l in c:
        key = (l.pred.name, tuple(l.pred.args))
        if key in seen and seen[key] != l.neg:
            return True
        seen[key] = l.neg
    return False

def canonicalize_clause(c: Clause) -> Clause:
    """
    Renombra variables a v1,v2,... para comparar cláusulas alfa-equivalentes.
    Esto permite evitar reinsertar resolventes duplicados que difieren solo en nombres.
    """
    mapping: Dict[Var, Var] = {}
    def note(v: Var) -> Var:
        if v not in mapping:
            mapping[v] = Var(f'v{len(mapping)+1}')
        return mapping[v]
    def canon_term(t: Term) -> Term:
        if isinstance(t, Var): return note(t)
        if isinstance(t, Const): return t
        return Func(t.name, tuple(canon_term(a) for a in t.args))
    def canon_pred(p: Pred) -> Pred:
        return Pred(p.name, tuple(canon_term(a) for a in p.args))
    return frozenset(Literal(canon_pred(l.pred), l.neg) for l in c)

def pretty_clause(c: Clause) -> str:
    return " ∨ ".join(sorted(map(str, c))) if c else "□"

# -----------------------------------------------------------------------------
# Traza para sustentación
# -----------------------------------------------------------------------------

@dataclass
class FolStep:
    """Un paso de resolución FOL para impresión y sustentación."""
    iteration: int
    left_id: int
    right_id: int
    left_lit: Literal
    right_lit: Literal
    theta: Subst
    resolvent: Clause

# -----------------------------------------------------------------------------
# Resolución FOL (núcleo)
# -----------------------------------------------------------------------------

def resolve_first_order(clauses_init: Iterable[Clause], keep_steps: bool = True):
    """
    Ejecuta la resolución FOL sobre una KB en CNF con los criterios de la práctica.
    Retorna: (entails_empty, derived_set, proof_map, steps)

    - `entails_empty` es True si se derivó `□` (la sentencia original es verdadera).
    - `derived_set` contiene todas las cláusulas visitadas/derivadas (canónicas).
    - `proof_map` enlaza resolventes con sus padres (opcional para reconstrucción).
    - `steps` trae la traza completa si `keep_steps=True`.
    """
    clauses: List[Clause] = []
    seen: Set[Clause] = set()  # almacenamiento de cláusulas en forma canónica
    proof: Dict[Clause, Tuple[Clause, Clause]] = {}
    steps: List[FolStep] = []

    def add_clause(c: Clause, parents: Optional[Tuple[Clause, Clause]] = None) -> bool:
        canon = canonicalize_clause(c)
        if canon in seen:
            return False
        seen.add(canon)
        clauses.append(canon)
        if parents:
            proof[canon] = parents
        return True

    # Carga inicial
    for c in clauses_init:
        add_clause(c)

    processed_pairs: Set[Tuple[int, int]] = set()  # evita re-uso de pares
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

                Ci = clauses[i]
                Cj = clauses[j]

                # Estandarización-aparte por par
                Ci_std = standardize_apart(Ci, f'a{i}')
                Cj_std = standardize_apart(Cj, f'b{j}')

                # Intenta todas las parejas de literales complementarios
                for li in Ci_std:
                    for lj in Cj_std:
                        if not literal_complementary(li, lj):
                            continue

                        theta: Subst = {}
                        # Unifica argumento a argumento
                        for a, b in zip(li.pred.args, lj.pred.args):
                            theta = unify(a, b, theta)
                            if theta is None:
                                break
                        if theta is None:
                            continue  # no unificó este par

                        # Construir resolvente (sin los pivotes) y aplicar θ
                        Ri = frozenset(x for x in Ci_std if x != li)
                        Rj = frozenset(x for x in Cj_std if x != lj)
                        R  = apply_subst_clause(Ri.union(Rj), theta)

                        if is_tautology(R):
                            continue

                        if keep_steps:
                            steps.append(FolStep(iteration, i, j, li, lj, dict(theta), R))

                        if not add_clause(R, parents=(clauses[i], clauses[j])):
                            continue

                        new_any = True
                        if len(R) == 0:
                            return True, set(clauses), proof, steps

        if not new_any:
            return False, set(clauses), proof, steps

# -----------------------------------------------------------------------------
# Helper para crear literales de forma legible en ejemplos
# -----------------------------------------------------------------------------

def L(name: str, *args: Term, neg: bool = False) -> Literal:
    """Crea un literal: L('Predicado', arg1, arg2, ..., neg=True|False)."""
    return Literal(Pred(name, args), neg)
