# Proyecto — Motor de Inferencia por Resolución (Python)

Implementación en **Python** de un motor de inferencia por **resolución por refutación** en dos etapas:

1. **Lógica proposicional** (sin variables, sin unificación).
2. **Lógica de primer orden** con **unificación de Robinson** (incluye *occurs-check*) y **estandarización-aparte**.

El proyecto imprime una **explicación paso a paso en la terminal**: qué cláusulas se resuelven, qué literales (o predicados) complementarios se usan, y en primer orden la **sustitución θ (MGU)** aplicada. Incluye el clásico **caso de Marco**.

---
## 📚 Información del Proyecto

- **Curso**: Inteligencia Artificial
- **Profesor**: Ing. Laura Juliana Mora Páez Msc
- **Grupo**: [5]
- **Integrantes**: 
- Alejandra Abaunza Suárez 
- Daniel Santiago Avila Medina
- Santos Alejandro Arellano Olarte
- Jeison Camilo Alfonso Moreno
---

## ✅ Cómo cumple los requisitos

* **Motor de resolución proposicional (sin variables)**:
  Implementado en `src/propositional_resolution.py` (`resolve_propositional`).
  Se trabaja con **CNF**: literales tipo `"A"` o `"~A"` y cláusulas como disyunciones (sets inmutables).
  En consola se muestran **pasos de resolución** y la **cláusula vacía `□`** si hay refutación.

* **Ejemplo para validar (proposicional)**:
  Incluido en `examples/run_examples.py` (Ejemplo 1). Muestra contradicción por refutación.

* **Algoritmo de unificación de variables**:
  Implementado en `src/unification.py` (Robinson + *occurs-check*). Integrado en `src/first_order_resolution.py`.
  Se realiza **estandarización-aparte** para evitar colisiones de variables.

* **Ejemplo de Marco (primer orden)**:
  Incluido en `examples/run_examples.py` (Ejemplo 2). Se deriva `□` con `Humano(Marco)` y `¬Humano(x) ∨ Mortal(x)` + `¬Mortal(Marco)`, demostrando **Mortal(Marco)** por refutación.

* **Lenguaje procedural**: Python, con funciones claras y módulos separados.

---

## 🧩 Conceptos clave (muy breve)

* **Resolución por refutación**: para demostrar una meta `G`, se añade `¬G` a las premisas en CNF; si se deriva `□`, entonces `G` es consecuencia lógica.
* **Cláusula vacía `□`**: indica contradicción (éxito de la refutación).
* **Unificación**: encuentra la sustitución **θ (MGU)** que hace coincidir términos (variables, constantes, funciones); con *occurs-check* para evitar ciclos.
* **Estandarización-aparte**: renombra variables para que no colisionen entre cláusulas distintas.

---

## 🛠 Requisitos

* Python **3.9+** (recomendado 3.10+).
* Sin dependencias externas.

---

## 📁 Estructura

```
proyecto_resolucion/
├─ src/
│  ├─ __init__.py
│  ├─ propositional_resolution.py     # Resolución proposicional + traza didáctica
│  ├─ unification.py                  # Unificación (Robinson + occurs-check)
│  └─ first_order_resolution.py       # Resolución 1er orden + estandarización-aparte
└─ examples/
   └─ run_examples.py                 # Demostraciones narradas (proposicional y Marco)
```

---

## ▶️ Ejecución

Desde la **raíz** del proyecto:

```bash
python examples/run_examples.py
```

Verás dos bloques:

1. **Resolución Proposicional (sin variables)** – imprime **cada paso**:

   * qué cláusulas se resolvieron,
   * qué literales complementarios (`l` vs `~l`) se usaron,
   * el **resolvente** resultante,
   * y, si aplica, la derivación de `□`.

2. **Resolución de Primer Orden (con unificación) – Caso Marco** – imprime **cada paso**:

   * los dos literales complementarios que **unifican**,
   * la **sustitución θ** encontrada,
   * el **resolvente** resultante,
   * y el cierre con `□` cuando se alcanza la contradicción.

> Si quieres guardar la evidencia en un archivo de texto:
> `python examples/run_examples.py > evidencia.txt`

---

## 🧪 Ejemplos que se muestran

### 1) Proposicional (inconsistencia por refutación)

CNF:

```
1) A ∨ B
2) ¬A ∨ C
3) ¬B
4) ¬C
```

Explicación en consola (resumen):

* De `(A ∨ B)` y `(¬B)` se obtiene `A`.
* De `(¬A ∨ C)` y `A` se obtiene `C`.
* Con `¬C` se llega a contradicción → `□`.

### 2) Primer orden – Caso Marco (meta: Mortal(Marco))

Cláusulas:

```
Humano(Marco)
¬Humano(x) ∨ Mortal(x)         (∀x: Humano(x) → Mortal(x))
¬Mortal(Marco)                  (negación de la meta)
```

Explicación en consola (resumen):

* Unifica `Humano(x)` con `Humano(Marco)` con θ = `{ x → Marco }`.
* Obtiene `Mortal(Marco)`.
* Resuelve con `¬Mortal(Marco)` → `□`.
* Concluye: **Mortal(Marco)** es consecuencia lógica.

---

## 🧠 API rápida (por si quieres reusar los módulos)

### Proposicional

```python
from src.propositional_resolution import (
    resolve_propositional, parse_clause_list, pretty_clause, reconstruct_proof
)

raw = [["A","B"], ["~A","C"], ["~B"], ["~C"]]
clauses = parse_clause_list(raw)
entails, derived, proof, steps = resolve_propositional(clauses, keep_steps=True)
```

* `steps` trae la traza con los pares resueltos y el resolvente → ideal para explicar.
* `reconstruct_proof(□, proof)` reconstruye el orden de derivación.

### Primer orden

```python
from src.first_order_resolution import resolve_first_order, L, Var, Const, pretty_clause

clauses = {
    frozenset({ L("Humano", Const("Marco")) }),
    frozenset({ L("Humano", Var("x"), neg=True), L("Mortal", Var("x")) }),
    frozenset({ L("Mortal", Const("Marco"), neg=True) }),
}
entails, derived, proof, steps = resolve_first_order(clauses, keep_steps=True)
```

* Literales con `L("Pred", args..., neg=True|False)`
* Términos: `Var("x")`, `Const("Marco")`, `Func("f", (...))`
* `steps` incluye θ (MGU) por paso.

---

## ➕ Cómo agregar tus propios problemas

### Proposicional

1. Pasar tus fórmulas a **CNF** (AND de cláusulas; cada cláusula es OR de literales).
2. Representar literales como strings: `"A"`, `"~A"`.
3. Ejemplo:

   ```python
   raw = [["P", "Q"], ["~P"], ["~Q"]]
   clauses = parse_clause_list(raw)
   resolve_propositional(clauses, keep_steps=True)
   ```

### Primer orden

1. Modelar hechos y reglas en **forma clausal** (por ejemplo, `∀x (P(x) → Q(x))` como `¬P(x) ∨ Q(x)`).
2. Usar `Var`, `Const`, `Func` y el helper `L(...)`.
3. Ejemplo:

   ```python
   clauses = {
     frozenset({ L("Padre", Const("Juan"), Var("x")) }),
     frozenset({ L("Padre", Var("y"), Var("z"), neg=True), L("Abuelo", Var("y"), Var("z")) }),
     # + negación de la meta si vas por refutación
   }
   resolve_first_order(clauses, keep_steps=True)
   ```


---


## 📚 Referencias breves

* Robinson, J. A. (1965). *A Machine-Oriented Logic Based on the Resolution Principle*.
* Russell, S. & Norvig, P. (2010). *Artificial Intelligence: A Modern Approach*.
* Akerkar & Sajja (2010). *Knowledge-Based Systems*.

