# 📚 Taller 6 - Implementación de Redes Semánticas en Prolog

## 📋 Información del Proyecto

**Curso:** Inteligencia Artificial  
**Taller:** 6 - Redes Semánticas  
**Grupo:** 5  
**Integrantes:** 
- Santos Alejandro Arellano Olarte
- Alejandra Abaunza Suárez 
- Daniel Santiago Avila Medina
- Jeison Camilo Alfonso Moreno


## 📝 Descripción

Este proyecto implementa un sistema de **Redes Semánticas** en Prolog para representar conocimiento sobre jugadores de fútbol y equipos. El sistema utiliza mecanismos de herencia de propiedades mediante relaciones jerárquicas (`es-un`) y de instanciación (`instancia-de`).

## 🎯 Objetivos

1. **Diseñar** un mecanismo de herencia de propiedades utilizando Prolog
2. **Implementar** el ejemplo base de redes semánticas visto en clase
3. **Ampliar** el modelo con una nueva jerarquía para equipos de fútbol
4. **Demostrar** el funcionamiento correcto mediante consultas y pruebas

## 📁 Estructura del Proyecto

```
Taller6-Grup5/
│
├── README.md                       # Este archivo
├── redes_semanticas.pl            # Código principal en Prolog
├── red_semantica_ampliada.html    # Visualización de la red
├── presentacion_taller6.pptx      # Presentación con diagramas
│
├── capturas/
│   ├── primera_entrega/           # Pantallazos del caso base
│   │   ├── demo_basico.png
│   │   ├── consulta_altura.png
│   │   ├── consulta_pie_habil.png
│   │   └── consulta_patear.png
│   │
│   └── entrega_final/             # Pantallazos del caso ampliado
│       ├── demo_completo.png
│       ├── propiedades_equipo.png
│       ├── objetos_clase.png
│       └── companeros_equipo.png
│
└── documentacion/
    ├── diagrama_red_base.png
    └── diagrama_red_ampliada.png
```

## 🚀 Instalación y Requisitos

### Requisitos Previos
- **SWI-Prolog** versión 8.0 o superior
- Editor de texto (recomendado: VSCode con extensión Prolog)

### Instalación de SWI-Prolog

#### Windows
```bash
# Descargar desde https://www.swi-prolog.org/download/stable
# Ejecutar el instalador .exe
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install swi-prolog
```

#### macOS
```bash
brew install swi-prolog
```

## 💻 Uso del Sistema

### 1. Cargar el programa

```bash
# Iniciar SWI-Prolog
swipl

# Cargar el archivo
?- [redes_semanticas].
```

### 2. Ejecutar la demostración completa

```prolog
?- demo.
```

### 3. Consultas Básicas

#### Herencia de Propiedades
```prolog
% Obtener la altura de Adith (heredada de jugador_futbol)
?- obtener_propiedad(adith, altura, X).
X = 1.85.

% Obtener el pie hábil de Miguel (heredado de persona)
?- obtener_propiedad(miguel, pie_habil, X).
X = derecho.
```

#### Verificación de Capacidades
```prolog
% ¿Puede Miguel patear un balón?
?- puede(miguel, patea, balon).
true.

% ¿Puede Adith patear un balón?
?- puede(adith, patea, balon).
true.
```

#### Consultas sobre Equipos
```prolog
% Listar todas las propiedades de Millonarios
?- listar_propiedades(millonarios).

% Obtener todos los equipos de primera división
?- objetos_de_clase(equipo_primera_division, X).
X = millonarios ;
X = santa_fe ;
X = nacional.
```

#### Relaciones entre Jugadores y Equipos
```prolog
% ¿En qué equipo juega Miguel?
?- juega_en(miguel, X).
X = millonarios.

% ¿Son compañeros Miguel y Adith?
?- companeros(miguel, adith).
true.
```

### 4. Consultas Avanzadas

```prolog
% Obtener todos los jugadores de fútbol
?- objetos_de_clase(jugador_futbol, X).

% Verificar si una clase es subclase de otra
?- subclase_de(defensa, persona).

% Obtener jugadores del mismo equipo
?- companeros(X, Y).
```

## 🏗️ Arquitectura del Sistema

### Componentes Principales

#### 1. **Jerarquía de Clases**
- **Personas:** `persona → hombre_adulto → jugador_futbol → {defensa, delantero}`
- **Equipos:** `organizacion → equipo_futbol → equipo_profesional → equipo_primera_division`

#### 2. **Mecanismo de Herencia**
```prolog
% Búsqueda de propiedades con prioridad local
obtener_propiedad(Objeto, Atributo, Valor) :-
    % 1. Busca propiedad directa
    % 2. Si es instancia, busca en su clase
    % 3. Si es clase, busca en superclases
```

#### 3. **Relaciones Implementadas**
- `es_un/2`: Relación de subclase
- `instancia_de/2`: Relación de pertenencia
- `propiedad/3`: Asignación de atributos
- `juega_en/2`: Relación jugador-equipo
- `companeros/2`: Jugadores del mismo equipo

## 📊 Modelo de Datos

### Ejemplo de Estructura
```prolog
% Jerarquía
es_un(jugador_futbol, hombre_adulto).
es_un(hombre_adulto, persona).

% Instancias
instancia_de(miguel, delantero).
instancia_de(adith, defensa).

% Propiedades
propiedad(persona, pie_habil, derecho).
propiedad(jugador_futbol, altura, 1.85).
propiedad(miguel, equipo, millonarios).
```

## 🧪 Casos de Prueba

### Test 1: Herencia Simple
```prolog
% Adith hereda altura de jugador_futbol
?- obtener_propiedad(adith, altura, 1.85).
true.
```

### Test 2: Herencia Múltiple Niveles
```prolog
% Miguel hereda pie_habil de persona (3 niveles arriba)
?- obtener_propiedad(miguel, pie_habil, derecho).
true.
```

### Test 3: Sobrescritura de Propiedades
```prolog
% Defensa tiene su propio numero_goles que sobrescribe el de jugador_futbol
?- obtener_propiedad(defensa, numero_goles, 1).
true.
```

### Test 4: Relaciones Entre Jerarquías
```prolog
% Miguel y Adith son compañeros porque juegan en Millonarios
?- companeros(miguel, adith).
true.
```

## 📈 Ampliaciones Implementadas

### 1. **Jerarquía de Equipos** ✅
- Nueva rama completa desde `Organización` hasta equipos específicos
- Tres instancias de equipos: Millonarios, Santa Fe, Nacional
- Propiedades específicas: ciudad, fundación, colores

### 2. **Relaciones Inter-jerárquicas** ✅
- Conexión entre jugadores y equipos mediante `juega_en/2`
- Predicado `companeros/2` para encontrar jugadores del mismo equipo

### 3. **Consultas Mejoradas** ✅
- `listar_propiedades/1`: Muestra todas las propiedades de un objeto
- `objetos_de_clase/2`: Obtiene todas las instancias de una clase
- `demo/0`: Demostración completa del sistema

## 🐛 Solución de Problemas Comunes

### Error: "undefined procedure"
```prolog
% Asegúrate de haber cargado el archivo
?- [redes_semanticas].
```

### Error: "false" en consultas esperadas
```prolog
% Verifica la escritura exacta de los nombres
% Los átomos en Prolog son sensibles a mayúsculas
?- instancia_de(Miguel, delantero).  % INCORRECTO
?- instancia_de(miguel, delantero).  % CORRECTO
```

### Consultas sin resultados
```prolog
% Usa ; para obtener más soluciones
?- objetos_de_clase(equipo_primera_division, X).
X = millonarios ;  % Presiona ; para continuar
X = santa_fe ;
X = nacional.
```

## 📚 Referencias

- Russell & Norvig, *Artificial Intelligence: A Modern Approach*
- E. Rich, *Inteligencia Artificial*, 1994
- Jorge Baier, *Redes Semánticas y PLN en Prolog*, PUC de Chile
- Documentación SWI-Prolog: https://www.swi-prolog.org/

## 🤝 Contribuciones

Este proyecto fue desarrollado como parte del Taller 6 del curso de Inteligencia Artificial. Las contribuciones de los integrantes incluyen:

- **[Estudiante 1]**: Implementación del mecanismo de herencia y caso base
- **[Estudiante 2]**: Ampliación con jerarquía de equipos y documentación

## 📄 Licencia

Este proyecto es de uso académico para el curso de Inteligencia Artificial.

## ✉️ Contacto

Para preguntas o sugerencias sobre este proyecto:
- **Email:** [arellanosantoso6@gmail.com]



