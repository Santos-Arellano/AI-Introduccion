# -*- coding: utf-8 -*-
"""
motor/unification.py
====================
Módulo de **unificación de Robinson** con *occurs-check* para lógica de primer orden.

Responsabilidades principales:
- Definir los tipos de término: Var, Const, Func.
- Aplicar sustituciones (variables -> términos) a términos.
- Verificar occurs-check.
- Implementar `unify(t1, t2)` que retorna la MGU (most general unifier) o None.

Este archivo es autocontenible y sin dependencias externas.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Dict, Optional, Union

# -----------------------------------------------------------------------------
# Definición de términos
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class Var:
    """Variable lógica, identificada por su nombre."""
    name: str
    def __str__(self) -> str: return self.name

@dataclass(frozen=True)
class Const:
    """Constante lógica, identificada por su nombre."""
    name: str
    def __str__(self) -> str: return self.name

@dataclass(frozen=True)
class Func:
    """
    Función lógica con símbolo y aridad definidos por la tupla de argumentos.
    Ejemplos: f(), padre(Juan), g(x, h(y))
    """
    name: str
    args: Tuple["Term", ...]
    def __str__(self) -> str:
        if not self.args: return self.name
        return f'{self.name}({", ".join(map(str, self.args))})'

# Unión de tipos para anotar "término"
Term = Union[Var, Const, Func]

# Sustitución: asigna variables a términos
Subst = Dict[Var, Term]

# -----------------------------------------------------------------------------
# Sustitución y occurs-check
# -----------------------------------------------------------------------------

def apply_subst_term(t: Term, s: Subst) -> Term:
    """
    Aplica sustitución `s` a un término `t`.
    Si `t` es variable y está en `s`, se sustituye y se vuelve a aplicar (transitivamente).
    """
    if isinstance(t, Var):
        return apply_subst_term(s[t], s) if t in s else t
    if isinstance(t, Const):
        return t
    # Func
    return Func(t.name, tuple(apply_subst_term(a, s) for a in t.args))

def occurs_check(v: Var, t: Term, s: Subst) -> bool:
    """
    Verifica si `v` ocurre (tras aplicar `s`) dentro de `t`.
    Evita unificaciones ilegales como x = f(x).
    """
    t = apply_subst_term(t, s)
    if isinstance(t, Var): return t == v
    if isinstance(t, Const): return False
    # Func
    return any(occurs_check(v, a, s) for a in t.args)

# -----------------------------------------------------------------------------
# Unificación de Robinson
# -----------------------------------------------------------------------------

def unify(t1: Term, t2: Term, subst: Optional[Subst] = None) -> Optional[Subst]:
    """
    Retorna la MGU que unifica t1 y t2, o None si no son unificables.
    Reglas clave:
      - Si t1 == t2 ⇒ devolver `subst`.
      - Var vs algo ⇒ asignar salvo occurs-check.
      - Const vs Const ⇒ nombres iguales.
      - Func vs Func ⇒ mismo símbolo y aridad, unificar argumentos en orden.
    """
    if subst is None: subst = {}

    # Normalizar según sustitución acumulada
    t1 = apply_subst_term(t1, subst)
    t2 = apply_subst_term(t2, subst)

    if t1 == t2:
        return subst

    if isinstance(t1, Var):
        if occurs_check(t1, t2, subst): return None
        new = dict(subst); new[t1] = t2
        return new
    if isinstance(t2, Var):
        if occurs_check(t2, t1, subst): return None
        new = dict(subst); new[t2] = t1
        return new

    if isinstance(t1, Const) and isinstance(t2, Const):
        return subst if t1.name == t2.name else None

    if isinstance(t1, Func) and isinstance(t2, Func) and t1.name == t2.name and len(t1.args) == len(t2.args):
        for a, b in zip(t1.args, t2.args):
            subst = unify(a, b, subst)
            if subst is None: return None
        return subst

    return None
