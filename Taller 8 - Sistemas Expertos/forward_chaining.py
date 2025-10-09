"""
Sistema de Inferencia con Encadenamiento Hacia Adelante (Forward Chaining)
Descripción: Implementación de un motor de inferencia que utiliza encadenamiento
            hacia adelante para derivar nuevos hechos a partir de reglas y hechos conocidos.
"""

class Regla:
    """
    Clase que representa una regla en el sistema de inferencia.
    Cada regla tiene premisas (antecedentes) y una conclusión (consecuente).
    """
    def __init__(self, nombre, premisas, conclusion):
        """
        Constructor de la clase Regla.
        
        Args:
            nombre (str): Identificador de la regla (ej: "R1", "R2")
            premisas (list): Lista de strings que representan las condiciones
            conclusion (str): String que representa la conclusión de la regla
        """
        self.nombre = nombre
        self.premisas = premisas
        self.conclusion = conclusion
        self.disparada = False  # Indica si la regla ya fue aplicada
    
    def evaluar(self, hechos):
        """
        Evalúa si todas las premisas de la regla están en los hechos conocidos.
        
        Args:
            hechos (set): Conjunto de hechos conocidos
            
        Returns:
            bool: True si todas las premisas están satisfechas, False en caso contrario
        """
        return all(premisa in hechos for premisa in self.premisas)
    
    def __str__(self):
        """Representación en string de la regla"""
        premisas_str = " & ".join(self.premisas)
        return f"{self.nombre}: Si {premisas_str} => {self.conclusion}"


class MotorInferencia:
    """
    Motor de inferencia que implementa el algoritmo de encadenamiento hacia adelante.
    """
    def __init__(self):
        """Constructor del motor de inferencia"""
        self.reglas = []
        self.hechos = set()
        self.historial = []  # Guarda el historial de inferencias
        
    def agregar_regla(self, regla):
        """
        Agrega una regla al sistema.
        
        Args:
            regla (Regla): Regla a agregar
        """
        self.reglas.append(regla)
        
    def agregar_hecho(self, hecho):
        """
        Agrega un hecho inicial a la base de conocimientos.
        
        Args:
            hecho (str): Hecho a agregar
        """
        self.hechos.add(hecho)
        self.historial.append(f"Hecho inicial: {hecho}")
        
    def inferir(self, verbose=True):
        """
        Ejecuta el proceso de inferencia con encadenamiento hacia adelante.
        
        Args:
            verbose (bool): Si True, muestra el proceso paso a paso
            
        Returns:
            set: Conjunto final de hechos después de la inferencia
        """
        iteracion = 0
        nuevos_hechos = True
        
        if verbose:
            print("\n" + "="*80)
            print("INICIANDO PROCESO DE INFERENCIA - FORWARD CHAINING")
            print("="*80)
            print("\nHechos iniciales:")
            for i, hecho in enumerate(self.hechos, 1):
                print(f"  {i}. {hecho}")
        
        # Continuar mientras se generen nuevos hechos
        while nuevos_hechos:
            nuevos_hechos = False
            iteracion += 1
            
            if verbose:
                print(f"\n--- Iteración {iteracion} ---")
            
            # Evaluar cada regla
            for regla in self.reglas:
                # Solo evaluar reglas que no han sido disparadas
                if not regla.disparada:
                    if verbose:
                        print(f"\nEvaluando {regla.nombre}:")
                        print(f"  Premisas: {' & '.join(regla.premisas)}")
                    
                    # Verificar cada premisa
                    premisas_satisfechas = []
                    premisas_faltantes = []
                    
                    for premisa in regla.premisas:
                        if premisa in self.hechos:
                            premisas_satisfechas.append(premisa)
                            if verbose:
                                print(f"    ✓ '{premisa}' - VERDADERO")
                        else:
                            premisas_faltantes.append(premisa)
                            if verbose:
                                print(f"    ✗ '{premisa}' - FALSO/DESCONOCIDO")
                    
                    # Si todas las premisas están satisfechas
                    if regla.evaluar(self.hechos):
                        # Agregar la conclusión si no está ya en los hechos
                        if regla.conclusion not in self.hechos:
                            self.hechos.add(regla.conclusion)
                            regla.disparada = True
                            nuevos_hechos = True
                            
                            mensaje = f"¡REGLA {regla.nombre} DISPARADA! Nuevo hecho: {regla.conclusion}"
                            self.historial.append(mensaje)
                            
                            if verbose:
                                print(f"  → {mensaje}")
                        else:
                            if verbose:
                                print(f"  → Conclusión '{regla.conclusion}' ya existe en los hechos")
                    else:
                        if verbose:
                            print(f"  → Regla NO puede dispararse (faltan premisas)")
            
            if not nuevos_hechos and verbose:
                print("\nNo se generaron nuevos hechos en esta iteración.")
        
        if verbose:
            print("\n" + "="*80)
            print("PROCESO DE INFERENCIA COMPLETADO")
            print("="*80)
            print("\nHechos finales:")
            for i, hecho in enumerate(sorted(self.hechos), 1):
                print(f"  {i}. {hecho}")
            print("\n")
        
        return self.hechos
    
    def reiniciar(self):
        """Reinicia el motor de inferencia"""
        self.hechos.clear()
        self.historial.clear()
        for regla in self.reglas:
            regla.disparada = False


def ejemplo_clase():
    """
    Ejecuta el ejemplo dado en las diapositivas de clase.
    Hechos iniciales: A, L
    """
    print("\n" + "#"*80)
    print("# EJEMPLO 1: SISTEMA DE LAS DIAPOSITIVAS DE CLASE")
    print("#"*80)
    
    # Crear el motor de inferencia
    motor = MotorInferencia()
    
    # Definir las reglas según la imagen
    reglas = [
        Regla("R1", ["A", "N"], "E"),
        Regla("R2", ["A"], "M"),
        Regla("R3", ["D", "M"], "Z"),
        Regla("R4", ["Q", "¬W", "¬Z"], "N"),  # Nota: ¬ representa negación
        Regla("R5", ["Z", "L"], "S"),
        Regla("R6", ["L", "M"], "E"),
        Regla("R7", ["B", "C"], "Q")
    ]
    
    # Agregar las reglas al motor
    for regla in reglas:
        motor.agregar_regla(regla)
        print(f"Regla agregada: {regla}")
    
    # Agregar los hechos iniciales
    print("\nHechos iniciales: A, L")
    motor.agregar_hecho("A")
    motor.agregar_hecho("L")
    
    # Ejecutar la inferencia
    hechos_finales = motor.inferir()
    
    print("\nRESUMEN DE LA INFERENCIA:")
    print("Hechos iniciales: {A, L}")
    print(f"Hechos finales: {{{', '.join(sorted(hechos_finales))}}}")
    print("\nSecuencia de inferencias:")
    print("1. Primera iteración: A => M (por R2), obtenemos {A, L, M}")
    print("2. Segunda iteración: L & M => E (por R6), obtenemos {A, L, M, E}")
    print("3. Tercera iteración: No se pueden disparar más reglas")


def ejemplo_weather():
    """
    Ejecuta el ejemplo del sistema de pronóstico del clima (Weather Forecasting).
    """
    print("\n" + "#"*80)
    print("# EJEMPLO 2: SISTEMA DE PRONÓSTICO DEL CLIMA (WEATHER FORECASTING)")
    print("#"*80)
    
    # Crear un nuevo motor de inferencia
    motor = MotorInferencia()
    
    # Definir las reglas del sistema de pronóstico del clima
    reglas_weather = [
        Regla("Rule I", 
              ["we suspect temperature is less than 20°", "there is humidity in the air"],
              "there are chances of rain"),
        
        Regla("Rule II",
              ["Sun is behind the clouds", "air is very cool"],
              "we suspect temperature is less than 20°"),
        
        Regla("Rule III",
              ["air is very heavy"],
              "there is humidity in the air")
    ]
    
    # Agregar las reglas al motor
    print("\nReglas del sistema:")
    for regla in reglas_weather:
        motor.agregar_regla(regla)
        print(f"  {regla}")
    
    # Agregar los hechos iniciales
    print("\nHechos iniciales proporcionados:")
    print("  1. Sun is behind the clouds")
    print("  2. Air is very heavy and cool")
    
    # Nota: "Air is very heavy and cool" se descompone en dos hechos atómicos
    motor.agregar_hecho("Sun is behind the clouds")
    motor.agregar_hecho("air is very heavy")
    motor.agregar_hecho("air is very cool")
    
    # Ejecutar la inferencia
    hechos_finales = motor.inferir()
    
    # Verificar si se llegó a la conclusión esperada
    print("\nVERIFICACIÓN DEL RESULTADO:")
    if "there are chances of rain" in hechos_finales:
        print("✓ ÉXITO: Se ha concluido que 'there are chances of rain'")
        print("\nCadena de razonamiento:")
        print("1. 'air is very cool' & 'Sun is behind the clouds' => 'we suspect temperature is less than 20°'")
        print("2. 'air is very heavy' => 'there is humidity in the air'")
        print("3. 'we suspect temperature is less than 20°' & 'there is humidity in the air' => 'there are chances of rain'")
    else:
        print("✗ No se pudo concluir que hay posibilidades de lluvia")


if __name__ == "__main__":
    """
    Función principal que ejecuta los ejemplos del sistema.
    """
    print("╔" + "═"*78 + "╗")
    print("║" + " SISTEMA DE INFERENCIA - FORWARD CHAINING ".center(78) + "║")
    print("╚" + "═"*78 + "╝")
    
    # Ejecutar el ejemplo de las diapositivas
    ejemplo_clase()
    
    # Ejecutar el ejemplo del pronóstico del clima
    ejemplo_weather()
    
    print("\nPrograma finalizado.")
 