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

Este proyecto desarrolla un sistema de **Redes Semánticas** en Prolog que modela el mundo del fútbol colombiano. Permite representar jugadores, equipos y sus características usando herencia de propiedades a través de jerarquías de clases, similar a como funciona la programación orientada a objetos.

## 🎯 Objetivos

1. **Crear** un sistema que permita heredar características entre clases relacionadas
2. **Implementar** el ejemplo básico de jugadores de fútbol con sus propiedades
3. **Expandir** el modelo incluyendo equipos del fútbol profesional colombiano
4. **Validar** que el sistema funcione correctamente con consultas prácticas

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

## 📝 Comandos y Consultas del Sistema

### 🎯 Consulta Principal - Demostración
```prolog
?- demo.
```
**Descripción**: Ejecuta una demostración completa del sistema mostrando herencia, capacidades, relaciones y perfiles.

### 🔍 Consultas de Propiedades

#### Obtener propiedades específicas
```prolog
?- obtener_propiedad(Objeto, Atributo, Valor).
```
**Ejemplos**:
```prolog
?- obtener_propiedad(miguel, altura, X).        % Altura de Miguel
?- obtener_propiedad(adith, pie_habil, X).      % Pie hábil de Adith
?- obtener_propiedad(miguel, numero_goles, X).  % Goles promedio de Miguel
?- obtener_propiedad(defensa, numero_goles, X). % Goles típicos de un defensa
?- obtener_propiedad(millonarios, ciudad, X).   % Ciudad del equipo Millonarios
?- obtener_propiedad(nacional, fundacion, X).   % Año de fundación del Nacional
```

#### Listar todas las propiedades de un objeto
```prolog
?- listar_propiedades(Objeto).
```
**Ejemplos**:
```prolog
?- listar_propiedades(miguel).      % Todas las propiedades de Miguel
?- listar_propiedades(adith).       % Todas las propiedades de Adith
?- listar_propiedades(millonarios). % Todas las propiedades de Millonarios
?- listar_propiedades(santa_fe).    % Todas las propiedades de Santa Fe
?- listar_propiedades(nacional).    % Todas las propiedades del Nacional
```

### ⚽ Consultas de Capacidades y Acciones

#### Verificar si alguien puede hacer algo
```prolog
?- puede(Objeto, Accion, Sobre).
```
**Ejemplos**:
```prolog
?- puede(miguel, patea, balon).  % ¿Puede Miguel patear un balón?
?- puede(adith, patea, balon).   % ¿Puede Adith patear un balón?
?- puede(X, patea, balon).       % ¿Quién puede patear un balón?
```

### 👥 Consultas de Relaciones

#### Verificar compañeros de equipo
```prolog
?- companeros(Jugador1, Jugador2).
```
**Ejemplos**:
```prolog
?- companeros(miguel, adith).    % ¿Son Miguel y Adith compañeros?
?- companeros(miguel, X).        % ¿Quiénes son compañeros de Miguel?
?- companeros(X, Y).             % Encontrar todos los pares de compañeros
```

#### Verificar en qué equipo juega alguien
```prolog
?- juega_en(Jugador, Equipo).
```
**Ejemplos**:
```prolog
?- juega_en(miguel, X).          % ¿En qué equipo juega Miguel?
?- juega_en(adith, X).           % ¿En qué equipo juega Adith?
?- juega_en(X, millonarios).     % ¿Quién juega en Millonarios?
```

### 🏗️ Consultas de Jerarquías y Clasificación

#### Verificar pertenencia a clases
```prolog
?- pertenece_a(Objeto, Clase).
```
**Ejemplos**:
```prolog
?- pertenece_a(miguel, persona).           % ¿Miguel es una persona?
?- pertenece_a(adith, jugador_futbol).     % ¿Adith es jugador de fútbol?
?- pertenece_a(millonarios, organizacion). % ¿Millonarios es una organización?
?- pertenece_a(X, delantero).              % ¿Quién es delantero?
```

#### Verificar relaciones de herencia entre clases
```prolog
?- subclase_de(ClaseHija, ClasePadre).
```
**Ejemplos**:
```prolog
?- subclase_de(defensa, persona).                    % ¿Defensa hereda de persona?
?- subclase_de(equipo_primera_division, organizacion). % ¿Equipos de primera son organizaciones?
?- subclase_de(X, jugador_futbol).                   % ¿Qué clases heredan de jugador_futbol?
```

#### Listar objetos de una clase específica
```prolog
?- objetos_de_clase(Clase, Objeto).
```
**Ejemplos**:
```prolog
?- objetos_de_clase(jugador_futbol, X).        % ¿Quiénes son jugadores de fútbol?
?- objetos_de_clase(equipo_primera_division, X). % ¿Qué equipos están en primera división?
?- objetos_de_clase(persona, X).               % ¿Quiénes son personas?
?- objetos_de_clase(delantero, X).             % ¿Quiénes son delanteros?
?- objetos_de_clase(defensa, X).               % ¿Quiénes son defensas?
```

### 🔎 Consultas Avanzadas con Variables

#### Encontrar todos los valores de un atributo
```prolog
?- obtener_propiedad(_, Atributo, Valor).
```
**Ejemplos**:
```prolog
?- obtener_propiedad(_, ciudad, X).      % Todas las ciudades mencionadas
?- obtener_propiedad(_, altura, X).      % Todas las alturas definidas
?- obtener_propiedad(_, numero_goles, X). % Todos los promedios de goles
?- obtener_propiedad(_, colores, X).     % Todos los colores de equipos
```

#### Encontrar todos los objetos con una propiedad específica
```prolog
?- obtener_propiedad(Objeto, Atributo, ValorEspecifico).
```
**Ejemplos**:
```prolog
?- obtener_propiedad(X, ciudad, bogota).    % ¿Qué está en Bogotá?
?- obtener_propiedad(X, altura, 1.85).      % ¿Quién mide 1.85?
?- obtener_propiedad(X, deporte, futbol).   % ¿Qué practica fútbol?
?- obtener_propiedad(X, pie_habil, derecho). % ¿Quién es diestro?
```

### 📊 Consultas con Findall (Recopilar Resultados)

#### Obtener listas completas
```prolog
?- findall(Variable, Condicion, Lista).
```
**Ejemplos**:
```prolog
% Todos los jugadores
?- findall(X, pertenece_a(X, jugador_futbol), Jugadores).

% Todos los equipos
?- findall(X, pertenece_a(X, equipo_primera_division), Equipos).

% Todas las ciudades
?- findall(Ciudad, obtener_propiedad(_, ciudad, Ciudad), Ciudades).

% Todos los años de fundación
?- findall(Año, obtener_propiedad(_, fundacion, Año), Años).

% Todas las propiedades de una clase
?- findall(Prop-Valor, obtener_propiedad(jugador_futbol, Prop, Valor), Props).
```

### 🎮 Consultas Interactivas

#### Explorar el sistema paso a paso
```prolog
% Ver la jerarquía completa
?- es_un(X, Y).

% Ver todas las instancias
?- instancia_de(X, Y).

% Ver todas las propiedades definidas
?- propiedad(X, Y, Z).

% Verificar herencia transitiva
?- subclase_de(X, Y).

% Explorar todas las relaciones
?- pertenece_a(X, Y).
```

## 🏗️ Cómo funciona el sistema

### Estructura principal

#### 1. **Jerarquías de clases**
- **Jugadores:** `persona → hombre_adulto → jugador_futbol → {defensa, delantero}`
- **Equipos:** `organizacion → equipo_futbol → equipo_profesional → equipo_primera_division`

#### 2. **Herencia de características**
Cuando buscas una propiedad, el sistema:
1. Primero mira si el objeto la tiene directamente
2. Si no, busca en su clase padre
3. Sigue subiendo por la jerarquía hasta encontrarla

#### 3. **Tipos de relaciones**
- `es_un/2`: Define jerarquías (ej: defensa es_un jugador_futbol)
- `instancia_de/2`: Conecta objetos con clases (ej: miguel instancia_de delantero)
- `propiedad/3`: Asigna características (ej: miguel tiene equipo millonarios)
- `juega_en/2`: Relaciona jugadores con equipos
- `companeros/2`: Encuentra jugadores del mismo equipo

## 📊 Ejemplo de cómo se organiza la información

```prolog
% Definir jerarquías
es_un(jugador_futbol, hombre_adulto).
es_un(hombre_adulto, persona).

% Crear jugadores específicos
instancia_de(miguel, delantero).
instancia_de(adith, defensa).

% Asignar características
propiedad(persona, pie_habil, derecho).        % Todos heredan esto
propiedad(jugador_futbol, altura, 1.85).       % Solo los jugadores
propiedad(miguel, equipo, millonarios).        % Solo Miguel
```

## 🧪 Ejemplos de funcionamiento

### Herencia básica
```prolog
% Adith obtiene su altura de la clase jugador_futbol
?- obtener_propiedad(adith, altura, 1.85).
true.
```

### Herencia de varios niveles
```prolog
% Miguel hereda el pie hábil desde la clase persona (3 niveles arriba)
?- obtener_propiedad(miguel, pie_habil, derecho).
true.
```

### Propiedades específicas por posición
```prolog
% Los defensas tienen menos goles que los delanteros
?- obtener_propiedad(defensa, numero_goles, 1).
true.
```

### Relaciones entre jugadores y equipos
```prolog
% Miguel y Adith son compañeros porque ambos juegan en Millonarios
?- companeros(miguel, adith).
true.
```

## 📈 Características implementadas

### 1. **Equipos de fútbol colombiano** ✅
- Jerarquía completa desde organizaciones hasta equipos de primera división
- Incluye los tres grandes: Millonarios, Santa Fe y Nacional
- Cada equipo tiene su ciudad, año de fundación y colores

### 2. **Conexiones entre jugadores y equipos** ✅
- Los jugadores pueden pertenecer a equipos específicos
- Sistema para encontrar compañeros de equipo automáticamente

### 3. **Consultas útiles** ✅
- Ver todas las propiedades de cualquier objeto
- Listar todos los miembros de una clase
- Demostración interactiva del sistema completo

## 🐛 Problemas comunes y soluciones

### "undefined procedure" al hacer consultas
```prolog
% Primero carga el archivo
?- [redes_semanticas].
```

### Las consultas devuelven "false"
```prolog
% Revisa que los nombres estén escritos exactamente igual
% Prolog distingue entre mayúsculas y minúsculas
?- instancia_de(Miguel, delantero).  % ❌ INCORRECTO
?- instancia_de(miguel, delantero).  % ✅ CORRECTO
```

### Ver todas las respuestas posibles
```prolog
% Presiona ; (punto y coma) para ver más resultados
?- objetos_de_clase(equipo_primera_division, X).
X = millonarios ;  % Presiona ; aquí
X = santa_fe ;
X = nacional.
```

## 📚 Referencias

- Russell & Norvig, *Artificial Intelligence: A Modern Approach*
- E. Rich, *Inteligencia Artificial*, 1994
- Jorge Baier, *Redes Semánticas y PLN en Prolog*, PUC de Chile
- Documentación SWI-Prolog: https://www.swi-prolog.org/

## 🤝 Desarrollo del proyecto

Este proyecto fue desarrollado colaborativamente para el Taller 6 de Inteligencia Artificial:

- **Implementación base**: Sistema de herencia y jugadores de fútbol
- **Expansión**: Jerarquía de equipos del fútbol colombiano
- **Documentación**: Guías de uso y ejemplos prácticos
- **Pruebas**: Validación completa del funcionamiento

## 💡 Consejos para Usar los Comandos

### En Prolog Online (SWISH)
1. **Copia y pega** el código completo de `redes_semanticas.pl`
2. **Ejecuta las consultas** una por una en la consola
3. **Usa punto y coma (;)** para ver más soluciones: `?- companeros(X, Y).` luego presiona `;`
4. **Termina con punto (.)** para finalizar una consulta

### Navegación de Resultados
- **Variables libres**: `?- obtener_propiedad(X, altura, Y).` muestra todos los objetos con altura
- **Múltiples soluciones**: Presiona `;` para ver la siguiente solución o `.` para terminar
- **Consultas específicas**: `?- obtener_propiedad(miguel, altura, 1.85).` verifica si es verdadero

### Patrones Útiles
```prolog
% Buscar por patrón
?- obtener_propiedad(X, ciudad, bogota).     % Todo lo que esté en Bogotá
?- obtener_propiedad(miguel, X, Y).          % Todas las propiedades de Miguel
?- pertenece_a(X, jugador_futbol).           % Todos los jugadores

% Verificar relaciones
?- subclase_de(defensa, Y).                  % ¿De qué hereda defensa?
?- pertenece_a(miguel, Y).                   % ¿A qué clases pertenece Miguel?

% Explorar el sistema
?- propiedad(X, Y, Z).                       % Ver todas las propiedades definidas
?- es_un(X, Y).                              % Ver toda la jerarquía
```

### 🎯 Consultas Recomendadas para Empezar
```prolog
% 1. Primero ejecuta la demostración
?- demo.

% 2. Explora las propiedades de los jugadores
?- listar_propiedades(miguel).
?- listar_propiedades(adith).

% 3. Verifica la herencia
?- obtener_propiedad(miguel, pie_habil, X).
?- obtener_propiedad(adith, altura, X).

% 4. Prueba las capacidades
?- puede(miguel, patea, balon).

% 5. Explora los equipos
?- listar_propiedades(millonarios).
?- companeros(miguel, adith).

% 6. Descubre el sistema
?- objetos_de_clase(jugador_futbol, X).
?- objetos_de_clase(equipo_primera_division, X).
```

## 📄 Licencia

Este proyecto es de uso académico para el curso de Inteligencia Artificial.

## ✉️ Contacto

Para preguntas o sugerencias sobre este proyecto:
- **Email:** [arellanosantoso6@gmail.com]



