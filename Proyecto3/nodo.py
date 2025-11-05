"""
Clase Nodo - Representa un nodo en una Red Bayesiana
"""

class Nodo:
    """
    Representa un nodo individual en la Red Bayesiana.
    
    Atributos:
        nombre (str): Identificador único del nodo
        padres (list): Lista de objetos Nodo que son padres de este nodo
        hijos (list): Lista de objetos Nodo que son hijos de este nodo
        tabla_probabilidad (dict): Tabla de probabilidad condicional (CPT)
        valores_posibles (list): Lista de valores que puede tomar el nodo (ej: [True, False])
    """
    
    def __init__(self, nombre, valores_posibles=None):
        """
        Inicializa un nodo de la red bayesiana.
        
        Args:
            nombre (str): Nombre identificador del nodo
            valores_posibles (list): Valores que puede tomar la variable (default: [True, False])
        """
        self.nombre = nombre
        self.padres = []
        self.hijos = []
        self.tabla_probabilidad = {}
        self.valores_posibles = valores_posibles if valores_posibles else [True, False]
    
    def agregar_padre(self, nodo_padre):
        """
        Agrega un nodo padre a este nodo.
        
        Args:
            nodo_padre (Nodo): Nodo que será padre de este nodo
        """
        if nodo_padre not in self.padres:
            self.padres.append(nodo_padre)
    
    def agregar_hijo(self, nodo_hijo):
        """
        Agrega un nodo hijo a este nodo.
        
        Args:
            nodo_hijo (Nodo): Nodo que será hijo de este nodo
        """
        if nodo_hijo not in self.hijos:
            self.hijos.append(nodo_hijo)
    
    def establecer_probabilidad(self, condicion, probabilidad):
        """
        Establece una probabilidad en la tabla de probabilidad condicional.
        
        Args:
            condicion (tuple): Tupla con los valores de los padres y el valor del nodo
                              Formato: ((padre1_val, padre2_val, ...), nodo_val)
                              Para nodos sin padres: ((), nodo_val)
            probabilidad (float): Valor de probabilidad entre 0 y 1
        """
        self.tabla_probabilidad[condicion] = probabilidad
    
    def obtener_probabilidad(self, valores_padres, valor_nodo):
        """
        Obtiene la probabilidad condicional P(nodo=valor_nodo | padres=valores_padres)
        
        Args:
            valores_padres (tuple): Valores de los nodos padres en orden
            valor_nodo: Valor del nodo para el cual se quiere la probabilidad
            
        Returns:
            float: Probabilidad condicional
        """
        condicion = (valores_padres, valor_nodo)
        return self.tabla_probabilidad.get(condicion, 0.0)
    
    def es_raiz(self):
        """
        Verifica si el nodo es raíz (no tiene padres).
        
        Returns:
            bool: True si el nodo no tiene padres
        """
        return len(self.padres) == 0
    
    def es_hoja(self):
        """
        Verifica si el nodo es hoja (no tiene hijos).
        
        Returns:
            bool: True si el nodo no tiene hijos
        """
        return len(self.hijos) == 0
    
    def obtener_nombres_padres(self):
        """
        Obtiene los nombres de los nodos padres.
        
        Returns:
            list: Lista con los nombres de los padres
        """
        return [padre.nombre for padre in self.padres]
    
    def obtener_nombres_hijos(self):
        """
        Obtiene los nombres de los nodos hijos.
        
        Returns:
            list: Lista con los nombres de los hijos
        """
        return [hijo.nombre for hijo in self.hijos]
    
    def mostrar_tabla_probabilidad(self):
        """
        Muestra la tabla de probabilidad condicional en formato texto legible.
        """
        print(f"\n{'='*60}")
        print(f"TABLA DE PROBABILIDAD CONDICIONAL: {self.nombre}")
        print(f"{'='*60}")
        
        if self.es_raiz():
            print("Nodo raíz (sin padres)\n")
            for (padres_vals, nodo_val), prob in sorted(self.tabla_probabilidad.items()):
                print(f"P({self.nombre} = {nodo_val}) = {prob:.4f}")
        else:
            nombres_padres = self.obtener_nombres_padres()
            print(f"Padres: {', '.join(nombres_padres)}\n")
            
            # Agrupar por valores de padres
            grupos = {}
            for (padres_vals, nodo_val), prob in self.tabla_probabilidad.items():
                if padres_vals not in grupos:
                    grupos[padres_vals] = []
                grupos[padres_vals].append((nodo_val, prob))
            
            # Mostrar cada grupo
            for padres_vals in sorted(grupos.keys()):
                # Crear cadena de condición
                condiciones = [f"{nombres_padres[i]}={padres_vals[i]}" 
                             for i in range(len(nombres_padres))]
                condicion_str = ", ".join(condiciones)
                
                print(f"Dado que: {condicion_str}")
                for nodo_val, prob in sorted(grupos[padres_vals]):
                    print(f"  P({self.nombre} = {nodo_val} | {condicion_str}) = {prob:.4f}")
                print()
    
    def __str__(self):
        """
        Representación en string del nodo.
        
        Returns:
            str: Descripción del nodo
        """
        padres_str = ', '.join(self.obtener_nombres_padres()) if self.padres else 'ninguno'
        hijos_str = ', '.join(self.obtener_nombres_hijos()) if self.hijos else 'ninguno'
        return f"Nodo({self.nombre}) - Padres: [{padres_str}], Hijos: [{hijos_str}]"
    
    def __repr__(self):
        return f"Nodo('{self.nombre}')"
