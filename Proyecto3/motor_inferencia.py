"""
Motor de Inferencia por Enumeración para Redes Bayesianas
"""

from typing import Dict, List

from red_bayesiana import RedBayesiana


class MotorInferencia:
    def __init__(self, red: RedBayesiana, traza_activa: bool = False):
        self.red = red
        self.traza_activa = traza_activa
        self.nivel_traza = 0

    def inferir(self, consulta: Dict[str, object], evidencia: Dict[str, object]):
        """
        Calcula P(variable_consulta=valor | evidencia) por enumeración exacta.
        Args:
            consulta: dict con un par {variable: valor}
            evidencia: dict con valores observados
        Returns:
            float: Probabilidad solicitada
        """
        if len(consulta) != 1:
            raise ValueError("Consulta debe contener exactamente una variable")
        (var_consulta, valor_consulta), = consulta.items()

        # Variables a considerar
        todas = list(self.red.nodos.keys())

        # Numerador para valor específico
        asignacion_base = dict(evidencia)
        asignacion_base[var_consulta] = valor_consulta
        numerador = self._enumerar_todas(todas, asignacion_base)

        # Denominador: suma sobre todos los valores de la consulta
        denominador = 0.0
        for v in self.red.nodos[var_consulta].valores_posibles:
            asign = dict(evidencia)
            asign[var_consulta] = v
            denominador += self._enumerar_todas(todas, asign)

        if denominador == 0:
            return 0.0
        resultado = numerador / denominador
        if self.traza_activa:
            print(f"P({var_consulta}={valor_consulta} | evidencia) = {resultado:.4f}")
        return resultado

    def _enumerar_todas(self, variables: List[str], asignacion: Dict[str, object]) -> float:
        """
        Enumeración recursiva sobre variables ocultas.
        """
        # Si todas las variables relevantes están asignadas, calcular prob conjunta
        faltantes = [v for v in variables if v not in asignacion]
        if not faltantes:
            return self._calcular_probabilidad_conjunta(asignacion)

        # Tomar la primera variable faltante y sumar sobre su dominio
        var = faltantes[0]
        total = 0.0
        for valor in self.red.nodos[var].valores_posibles:
            nueva = dict(asignacion)
            nueva[var] = valor
            total += self._enumerar_todas(variables, nueva)
        return total

    def _calcular_probabilidad_conjunta(self, asignacion: Dict[str, object]) -> float:
        """
        Calcula P(X1=x1, X2=x2, ...) = ∏ P(Xi | Parents(Xi)).
        """
        producto = 1.0
        for nombre, valor in asignacion.items():
            nodo = self.red.nodos[nombre]
            # Obtener valores de los padres en el orden definido
            padres = nodo.obtener_nombres_padres()
            valores_padres = tuple(asignacion[p] for p in padres) if padres else ()
            prob = nodo.obtener_probabilidad(valores_padres, valor)
            producto *= prob
        return producto