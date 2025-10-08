# Sistema de Inferencia con Forward Chaining

# 📚 Taller 8 - sistema completo de inferencia con encadenamiento hacia adelante 

## 📋 Información del Proyecto

**Curso:** Inteligencia Artificial  
**Taller:** 8 - Sistemas Expertos  
**Grupo:** 5  
**Integrantes:** 
- Santos Alejandro Arellano Olarte
- Alejandra Abaunza Suárez 
- Daniel Santiago Avila Medina
- Jeison Camilo Alfonso Moreno

## 📚 Descripción

Este proyecto implementa un **motor de inferencia** que utiliza el algoritmo de **encadenamiento hacia adelante** (forward chaining) para derivar nuevos hechos a partir de un conjunto de reglas y hechos iniciales. Es una implementación educativa para el curso de Introducción a la Inteligencia Artificial.

### ¿Qué es Forward Chaining?

El encadenamiento hacia adelante es una estrategia de inferencia que:
1. Comienza con hechos conocidos
2. Aplica reglas cuyas premisas están satisfechas
3. Deriva nuevos hechos de las conclusiones
4. Repite el proceso hasta que no se puedan derivar más hechos

## 🚀 Características

- **Motor de inferencia completo** con encadenamiento hacia adelante
- **Manejo de hechos atómicos** (representados como strings)
- **Sistema de reglas** con múltiples premisas
- **Modo verbose** para seguir el proceso de inferencia paso a paso
- **Ejemplos precargados** según los requisitos de la tarea
- **Modo interactivo** para crear sistemas de reglas personalizados

## 📋 Requisitos

- Python 3.6 o superior
- No requiere librerías externas

## 💻 Instalación y Ejecución

1. **Clonar o descargar el archivo**
   ```bash
   # Guardar el archivo como forward_chaining.py
   ```

2. **Ejecutar el programa**
   ```bash
   python forward_chaining.py
   ```

   O en algunos sistemas:
   ```bash
   python3 forward_chaining.py
   ```

## 🏗️ Estructura del Código

### Clases Principales

#### `Regla`
Representa una regla de inferencia con:
- **nombre**: Identificador de la regla (ej: "R1", "Rule I")
- **premisas**: Lista de condiciones que deben cumplirse
- **conclusion**: Hecho que se deriva si se cumplen las premisas
- **disparada**: Bandera para evitar aplicar la misma regla múltiples veces

#### `MotorInferencia`
Implementa el algoritmo de forward chaining con métodos para:
- `agregar_regla()`: Añade reglas al sistema
- `agregar_hecho()`: Añade hechos iniciales
- `inferir()`: Ejecuta el proceso de inferencia
- `reiniciar()`: Limpia el estado para nuevas inferencias

### Funciones de Ejemplo

1. **`ejemplo_clase()`**: Ejecuta el ejemplo de las diapositivas con reglas R1-R7
2. **`ejemplo_weather()`**: Ejecuta el ejemplo del sistema de pronóstico del clima
3. **`menu_interactivo()`**: Permite crear sistemas de reglas personalizados

## 📖 Ejemplos Incluidos

### Ejemplo 1: Sistema de las Diapositivas

**Reglas:**
- R1: Si A & N => E
- R2: Si A => M
- R3: Si D & M => Z
- R4: Si Q & ¬W & ¬Z => N
- R5: Si Z & L => S
- R6: Si L & M => E
- R7: Si B & C => Q

**Hechos iniciales:** A, L

**Resultado esperado:** {A, L, M, E}

### Ejemplo 2: Weather Forecasting System

**Reglas:**
- Rule I: Si "temperature < 20°" Y "humidity in air" => "chances of rain"
- Rule II: Si "sun behind clouds" Y "air very cool" => "temperature < 20°"
- Rule III: Si "air very heavy" => "humidity in air"

**Hechos iniciales:**
- Sun is behind the clouds
- Air is very heavy and cool

**Resultado esperado:** "there are chances of rain"

## 🎯 Proceso de Inferencia

El programa ejecuta las siguientes etapas:

1. **Inicialización**: Carga reglas y hechos iniciales
2. **Iteración**: Para cada iteración:
   - Evalúa cada regla no disparada
   - Verifica si todas las premisas están en los hechos conocidos
   - Si se cumplen las premisas, añade la conclusión a los hechos
   - Marca la regla como disparada
3. **Terminación**: Cuando no se pueden derivar nuevos hechos

## 📊 Salida del Programa

El programa muestra:
- Las reglas cargadas en el sistema
- Los hechos iniciales
- Cada iteración del proceso de inferencia
- Evaluación detallada de cada regla
- Los hechos finales derivados
- Verificación del resultado esperado

### Ejemplo de Salida

```
=================================================================================
INICIANDO PROCESO DE INFERENCIA - FORWARD CHAINING
=================================================================================

Hechos iniciales:
  1. Sun is behind the clouds
  2. air is very heavy
  3. air is very cool

--- Iteración 1 ---

Evaluando Rule I:
  Premisas: we suspect temperature is less than 20° & there is humidity in the air
    ✗ 'we suspect temperature is less than 20°' - FALSO/DESCONOCIDO
    ✗ 'there is humidity in the air' - FALSO/DESCONOCIDO
  → Regla NO puede dispararse (faltan premisas)

Evaluando Rule II:
  Premisas: Sun is behind the clouds & air is very cool
    ✓ 'Sun is behind the clouds' - VERDADERO
    ✓ 'air is very cool' - VERDADERO
  → ¡REGLA Rule II DISPARADA! Nuevo hecho: we suspect temperature is less than 20°

[... continúa con más iteraciones ...]
```





## 🧪 Validación

El programa valida automáticamente:
- ✅ Que se alcancen las conclusiones esperadas
- ✅ Que el proceso de inferencia termine correctamente
- ✅ Que no se apliquen reglas redundantemente

## 📝 Notas Importantes

1. **Hechos Atómicos**: Los hechos se manejan como strings completos sin variables
2. **Case Sensitive**: Los hechos distinguen mayúsculas y minúsculas
3. **Sin Negación Explícita**: El sistema no maneja negación de hechos (excepto como parte del string)
4. **Terminación Garantizada**: El algoritmo siempre termina al no poder derivar nuevos hechos

## 🎓 Aplicaciones Educativas

Este sistema es útil para:
- Comprender el funcionamiento del forward chaining
- Estudiar sistemas basados en reglas
- Practicar conceptos de IA simbólica
- Implementar sistemas expertos simples

## 🤝 Contribuciones

Este es un proyecto educativo. Las sugerencias y mejoras son bienvenidas para fines de aprendizaje.

## 📄 Licencia

Proyecto educativo para el curso de Introducción a la Inteligencia Artificial.

---

**Autor**: Sistema desarrollado para la clase de Introducción a IA  
**Versión**: 1.0  
**Fecha**: 2024