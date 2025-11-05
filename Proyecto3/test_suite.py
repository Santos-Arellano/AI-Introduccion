"""
Suite de Pruebas Automatizadas para el Sistema de Red Bayesiana
"""

from nodo import Nodo
from arco import Arco
from red_bayesiana import RedBayesiana
from motor_inferencia import MotorInferencia


def prueba_crear_nodo():
    """
    Prueba la creación de nodos.
    """
    print("\n" + "="*70)
    print("PRUEBA 1: Creación de Nodos")
    print("="*70)
    
    nodo = Nodo("TestNodo", valores_posibles=[True, False])
    print(f"✓ Nodo creado: {nodo}")
    print(f"✓ Es raíz: {nodo.es_raiz()}")
    print(f"✓ Es hoja: {nodo.es_hoja()}")
    print(f"✓ Valores posibles: {nodo.valores_posibles}")
    
    return True


def prueba_crear_arco():
    """
    Prueba la creación de arcos.
    """
    print("\n" + "="*70)
    print("PRUEBA 2: Creación de Arcos")
    print("="*70)
    
    nodo1 = Nodo("Padre")
    nodo2 = Nodo("Hijo")
    arco = Arco(nodo1, nodo2)
    
    print(f"✓ Arco creado: {arco}")
    print(f"✓ Padre de Hijo: {nodo2.obtener_nombres_padres()}")
    print(f"✓ Hijo de Padre: {nodo1.obtener_nombres_hijos()}")
    print(f"✓ Arco válido: {arco.es_valido()}")
    
    return True


def prueba_red_simple():
    """
    Prueba la creación de una red simple.
    """
    print("\n" + "="*70)
    print("PRUEBA 3: Red Bayesiana Simple")
    print("="*70)
    
    # Crear red simple: A -> B -> C
    red = RedBayesiana()
    
    # Crear nodos
    nodo_a = Nodo("A")
    nodo_b = Nodo("B")
    nodo_c = Nodo("C")
    
    # Agregar nodos a la red
    red.agregar_nodo(nodo_a)
    red.agregar_nodo(nodo_b)
    red.agregar_nodo(nodo_c)
    
    # Crear arcos
    red.agregar_arco("A", "B")
    red.agregar_arco("B", "C")
    
    # Establecer probabilidades
    nodo_a.establecer_probabilidad(((), True), 0.3)
    nodo_a.establecer_probabilidad(((), False), 0.7)
    
    nodo_b.establecer_probabilidad(((True,), True), 0.8)
    nodo_b.establecer_probabilidad(((True,), False), 0.2)
    nodo_b.establecer_probabilidad(((False,), True), 0.4)
    nodo_b.establecer_probabilidad(((False,), False), 0.6)
    
    nodo_c.establecer_probabilidad(((True,), True), 0.9)
    nodo_c.establecer_probabilidad(((True,), False), 0.1)
    nodo_c.establecer_probabilidad(((False,), True), 0.2)
    nodo_c.establecer_probabilidad(((False,), False), 0.8)
    
    print(f"✓ Red creada con {len(red.nodos)} nodos y {len(red.arcos)} arcos")
    print(f"✓ Nodos raíz: {[n.nombre for n in red.obtener_raices()]}")
    
    red.mostrar_estructura()
    
    return red


def prueba_inferencia_simple(red):
    """
    Prueba inferencia en red simple.
    
    Args:
        red (RedBayesiana): Red a probar
    """
    print("\n" + "="*70)
    print("PRUEBA 4: Inferencia Simple")
    print("="*70)
    
    motor = MotorInferencia(red, traza_activa=False)
    
    # P(C=True | A=True)
    print("\nCalculando P(C=True | A=True)...")
    resultado = motor.inferir(
        consulta={'C': True},
        evidencia={'A': True}
    )
    
    print(f"✓ Resultado: {resultado}")
    
    return True


def prueba_red_compleja():
    """
    Prueba con la red de ejemplo (Lluvia-Aspersor-Césped).
    """
    print("\n" + "="*70)
    print("PRUEBA 5: Red Compleja desde Archivos")
    print("="*70)
    
    red = RedBayesiana()
    
    try:
        red.cargar_estructura_desde_archivo("estructura.txt")
        red.cargar_probabilidades_desde_archivo("probabilidades.txt")
        
        print("\n✓ Red cargada exitosamente")
        
        # Validar
        if red.validar_red():
            print("✓ Red válida")
        
        # Realizar inferencia
        motor = MotorInferencia(red, traza_activa=False)
        
        print("\n--- Inferencia 1: P(Lluvia=True | Cesped_Mojado=True) ---")
        resultado1 = motor.inferir(
            consulta={'Lluvia': True},
            evidencia={'Cesped_Mojado': True}
        )
        
        print("\n--- Inferencia 2: P(Aspersor=True | Cesped_Mojado=True, Lluvia=False) ---")
        resultado2 = motor.inferir(
            consulta={'Aspersor': True},
            evidencia={'Cesped_Mojado': True, 'Lluvia': False}
        )
        
        return True
        
    except FileNotFoundError:
        print("⚠ Archivos de ejemplo no encontrados. Saltando esta prueba.")
        return False


def prueba_probabilidad_conjunta():
    """
    Prueba el cálculo de probabilidad conjunta.
    """
    print("\n" + "="*70)
    print("PRUEBA 6: Probabilidad Conjunta")
    print("="*70)
    
    # Crear red simple
    red = RedBayesiana()
    nodo_a = Nodo("A")
    nodo_b = Nodo("B")
    
    red.agregar_nodo(nodo_a)
    red.agregar_nodo(nodo_b)
    red.agregar_arco("A", "B")
    
    # Probabilidades
    nodo_a.establecer_probabilidad(((), True), 0.6)
    nodo_a.establecer_probabilidad(((), False), 0.4)
    nodo_b.establecer_probabilidad(((True,), True), 0.7)
    nodo_b.establecer_probabilidad(((True,), False), 0.3)
    nodo_b.establecer_probabilidad(((False,), True), 0.2)
    nodo_b.establecer_probabilidad(((False,), False), 0.8)
    
    motor = MotorInferencia(red, traza_activa=False)
    
    # Calcular P(A=True, B=True)
    # Debería ser: P(A=True) * P(B=True | A=True) = 0.6 * 0.7 = 0.42
    
    asignacion = {'A': True, 'B': True}
    prob = motor._calcular_probabilidad_conjunta(asignacion)
    
    print(f"P(A=True, B=True) = {prob:.4f}")
    print(f"Valor esperado: 0.4200")
    
    if abs(prob - 0.42) < 0.0001:
        print("✓ Cálculo correcto")
        return True
    else:
        print("✗ Error en el cálculo")
        return False


def prueba_deteccion_ciclos():
    """
    Prueba la detección de ciclos en la red.
    """
    print("\n" + "="*70)
    print("PRUEBA 7: Detección de Ciclos")
    print("="*70)
    
    # Crear red con ciclo: A -> B -> C -> A
    red = RedBayesiana()
    nodo_a = Nodo("A")
    nodo_b = Nodo("B")
    nodo_c = Nodo("C")
    
    red.agregar_nodo(nodo_a)
    red.agregar_nodo(nodo_b)
    red.agregar_nodo(nodo_c)
    
    red.agregar_arco("A", "B")
    red.agregar_arco("B", "C")
    red.agregar_arco("C", "A")  # Esto crea un ciclo
    
    if red._tiene_ciclos():
        print("✓ Ciclo detectado correctamente")
        return True
    else:
        print("✗ No se detectó el ciclo")
        return False


def ejecutar_todas_pruebas():
    """
    Ejecuta todas las pruebas del sistema.
    """
    print("\n" + "#"*70)
    print("# SUITE DE PRUEBAS AUTOMATIZADAS")
    print("# Sistema de Red Bayesiana con Motor de Inferencia")
    print("#"*70)
    
    pruebas = [
        ("Creación de Nodos", prueba_crear_nodo),
        ("Creación de Arcos", prueba_crear_arco),
        ("Red Simple", lambda: prueba_red_simple() is not None),
        ("Inferencia Simple", lambda: prueba_inferencia_simple(prueba_red_simple())),
        ("Red Compleja", prueba_red_compleja),
        ("Probabilidad Conjunta", prueba_probabilidad_conjunta),
        ("Detección de Ciclos", prueba_deteccion_ciclos),
    ]
    
    resultados = []
    
    for nombre, prueba in pruebas:
        try:
            resultado = prueba()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"\n✗ Error en prueba '{nombre}': {str(e)}")
            resultados.append((nombre, False))
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE PRUEBAS")
    print("="*70)
    
    exitosas = sum(1 for _, r in resultados if r)
    total = len(resultados)
    
    for nombre, resultado in resultados:
        simbolo = "✓" if resultado else "✗"
        print(f"{simbolo} {nombre}")
    
    print(f"\nPruebas exitosas: {exitosas}/{total} ({exitosas*100//total}%)")
    
    if exitosas == total:
        print("\n¡Todas las pruebas pasaron exitosamente! ✓")
    else:
        print(f"\n{total - exitosas} prueba(s) fallaron. ✗")


if __name__ == "__main__":
    ejecutar_todas_pruebas()
