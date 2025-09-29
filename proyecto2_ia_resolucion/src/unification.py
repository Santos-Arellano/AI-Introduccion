# -*- coding: utf-8 -*-
"""
=========================================
UNIFICACIÓN DE ROBINSON (CON OCCURS-CHECK)
=========================================

Definiciones:
- Var("x")            : variable simbólica.
- Const("Marco")      : constante.
- Func("f", (t1,...)) : término funcional.

Funciones:
- apply_subst_term: aplica una sustitución {Var -> Term} a un término.
- occurs_check    : evita ciclos (x = f(x,...)).
- unify           : retorna MGU (unificador más general) o None si falla.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple, Optional, Set, Union

# ---------- Representación de términos ----------
@dataclass(frozen=True)
class Var:
    name: str
    def __str__(self) -> str:
        return self.name

@dataclass(frozen=True)
class Const:
    name: str
    def __str__(self) -> str:
        return self.name

@dataclass(frozen=True)
class Func:
    name: str
    args: Tuple['Term', ...]
    def __str__(self) -> str:
        return f"{self.name}({', '.join(map(str, self.args))})" if self.args else self.name

Term = Union[Var, Const, Func]


# ---------- Sustituciones ----------
def apply_subst_term(t: Term, subst: Dict[Var, Term]) -> Term:
    """
    Aplica la sustitución a un término, propagando recursivamente.
    """
    if isinstance(t, Var):
        return apply_subst_term(subst[t], subst) if t in subst else t
    if isinstance(t, Const):
        return t
    return Func(t.name, tuple(apply_subst_term(a, subst) for a in t.args))


def occurs_check(v: Var, t: Term, subst: Dict[Var, Term]) -> bool:
    """
    Chequeo de ocurrencia: ¿v aparece dentro de t (con sustituciones aplicadas)?
    Evita unificaciones cíclicas tipo x = f(x,...).
    """
    t = apply_subst_term(t, subst)
    if isinstance(t, Var):   return t == v
    if isinstance(t, Const): return False
    return any(occurs_check(v, a, subst) for a in t.args)


# ---------- Unificación de Robinson ----------
def unify(t1: Term, t2: Term, subst: Optional[Dict[Var, Term]] = None) -> Optional[Dict[Var, Term]]:
    """
    Intenta unificar t1 y t2. Devuelve el MGU (dict Var->Term) o None si falla.
    """
    if subst is None:
        subst = {}

    # Normalizamos según sustituciones previas
    t1 = apply_subst_term(t1, subst)
    t2 = apply_subst_term(t2, subst)

    if t1 == t2:
        return subst

    if isinstance(t1, Var):
        if occurs_check(t1, t2, subst):
            return None
        subst = dict(subst); subst[t1] = t2
        return subst

    if isinstance(t2, Var):
        if occurs_check(t2, t1, subst):
            return None
        subst = dict(subst); subst[t2] = t1
        return subst

    if isinstance(t1, Const) and isinstance(t2, Const):
        return subst if t1.name == t2.name else None

    if isinstance(t1, Func) and isinstance(t2, Func) and t1.name == t2.name and len(t1.args) == len(t2.args):
        for a, b in zip(t1.args, t2.args):
            subst = unify(a, b, subst)
            if subst is None:
                return None
        return subst

    return None
