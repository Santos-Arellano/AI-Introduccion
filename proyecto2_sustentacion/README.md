Proyecto 2 — Sustentación: Motor de Inferencia por Resolución (Python)
=====================================================================

Descripción
-----------
Implementación **documentada** de un motor de **Prueba por Resolución** para:

1. **Lógica Proposicional** (sin variables).
2. **Lógica de Primer Orden (FOL)** con **unificación de Robinson** (incluye occurs-check) y **estandarización‑aparte**.

El sistema imprime una **traza paso a paso** para sustentar: qué cláusulas se resolvieron, qué literales/predicados fueron pivote, la **MGU θ** aplicada en FOL y el resolvente generado. La demostración incluye el ejercicio **“¿La curiosidad mató a Tuna?”**, conforme a la solución esperada en el campus. La organización y el estilo están alineados con el material previo del curso. fileciteturn3file0


## 📚 Información del Proyecto

- **Curso**: Inteligencia Artificial
- **Profesor**: Ing. Laura Juliana Mora Páez Msc
- **Grupo**: [5]
- **Integrantes**: 
- Alejandra Abaunza Suárez 
- Daniel Santiago Avila Medina
- Santos Alejandro Arellano Olarte
- Jeison Camilo Alfonso Moreno

Cumplimiento de la guía de la práctica
--------------------------------------
1) **Base de conocimiento en CNF (Forma Normal Conjuntiva)**  
   - Se trabaja sobre **conjunto de cláusulas** (cada cláusula es OR de literales).  
   - La conversión a CNF se realiza externamente y se pasa al motor ya clausulada.

2) **Negar la sentencia a probar** y **añadirla a la lista de axiomas**  
   - En el caso Tuna se añade `¬Muerto(Tuna)` a las cláusulas iniciales.

3) **Mientras haya cláusulas por resolver:**  
   - Proposicional: busca literales complementarios `l` y `~l`.  
   - FOL: estandariza-aparte el par, busca complementarios y **unifica** argumentos (Robinson).  
   - Se **genera el resolvente** y se añade si no es tautología ni duplicado.

4) **Añadir el resolvente** a la lista de cláusulas.  
   - Se mantiene un conjunto `seen` para descartar duplicados y, en FOL, una **forma canónica** para tratar alfa‑equivalencia.

5) **Si se produce la cláusula nula `□`, detener y reportar VERDADERA** la sentencia original.  
   - El motor retorna `True` e imprime la derivación de `□` en la traza.

6) **Si no se produce `□`, detener y reportar FALSA**.  
   - El bucle de resolución se satura sin novedades y el motor retorna `False`.

7) **No validar varias veces reglas ya utilizadas.**  
   - Se evita re-uso del mismo par de cláusulas con `processed_pairs` (índices `(i, j)` ya intentados).  
   - También se evita reinsertar resolventes repetidos con `seen` (y canónica en FOL).

Estructura del proyecto
-----------------------
```
proyecto2_sustentacion/
├─ __init__.py
├─ motor/
│  ├─ __init__.py
│  ├─ unification.py             # Términos + unificación de Robinson (occurs‑check)
│  ├─ first_order_resolution.py  # Resolución FOL (estandarización‑aparte, MGU, canónica)
│  └─ propositional_resolution.py# Resolución proposicional
└─ examples/
   └─ run_examples.py            # Ejecuciones: proposicional + Tuna
```

Requisitos
----------
- Python 3.9 o superior (recomendado 3.10+).
- Sin dependencias externas.

Ejecución
---------
Desde la carpeta raíz `proyecto2_sustentacion/`:

```bash
python -m examples.run_examples
# o
python examples/run_examples.py
```

Resultados esperados
--------------------
1) **Ejemplo Proposicional**  
   CNF: `(A ∨ B)`, `(¬A)`, `(¬B)`  
   Se deriva `□` (inconsistencia), con traza completa de pasos.

2) **Caso “¿La curiosidad mató a Tuna?” (FOL)**  
   Axiomas en CNF + `¬Muerto(Tuna)`.  
   Se deriva `□` y se concluye que `Muerto(Tuna)` es **verdadera**.

Modelado de Tuna (CNF utilizado)
--------------------------------
1. `¬Curioso(x) ∨ Mata(Curiosidad, x)`  
2. `¬Mata(y, x) ∨ Muerto(x)`  
3. `Gato(Tuna)`  
4. `¬Gato(x) ∨ Curioso(x)`  
5. `¬Muerto(Tuna)`  (negación de la meta)

Decisiones de diseño
--------------------
- **CNF externa** para visibilizar el proceso de clausulado en la sustentación.
- **Estandarización‑aparte por par** para evitar colisiones de variables y facilitar la unificación.
- **Deduplicación**:
  - Proposicional: `processed_pairs` + `seen`.
  - FOL: `processed_pairs` + `seen` + **canonicalización** por nombres de variables.
- **Trazas claras** aptas para explicar cada resolución durante la sustentación.

Cómo agregar nuevos ejercicios
------------------------------
### Proposicional
1. Convertir a CNF (AND de cláusulas; cada cláusula es OR de literales).
2. Literales como strings: `"A"`, `"~A"`.
3. Cargar con `parse_clause_list([...])` y ejecutar `resolve_propositional(...)`.

### Primer orden (FOL)
1. Convertir a CNF (eliminar →, ↔; empujar negaciones; skolemizar si aplica; quitar ∀; distribuir ∨ sobre ∧).
2. Modelar con `Var`, `Const`, `Func` y el helper `L("Pred", args..., neg=bool)`.
3. Añadir **negación de la meta** y ejecutar `resolve_first_order(...)`.

Notas de complejidad
--------------------
La resolución en FOL es semi‑decidible y puede crecer combinatoriamente. La deduplicación y la detección de tautologías reducen el espacio de búsqueda, sin eliminar el peor caso.

Referencias
-----------
- Robinson, J. A. (1965). A Machine-Oriented Logic Based on the Resolution Principle.
- Russell, S. & Norvig, P. (2010). Artificial Intelligence: A Modern Approach.
- Akerkar, R. & Sajja, P. (2010). Knowledge-Based Systems.
