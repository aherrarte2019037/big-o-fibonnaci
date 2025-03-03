import time
import json
import os

class SimuladorTuring:

    def __init__(self, archivo_configuracion):
        self.cargar_configuracion(archivo_configuracion)
        self.cinta = []
        self.cabezal = 0
        self.estado_actual = self.estado_inicial
        self.pasos = 0
        self.tiempo_inicio = 0
        
    def cargar_configuracion(self, archivo):
        try:
            with open(archivo, 'r') as f:
                config = json.load(f)
                
            self.estados = config["estados"]
            self.simbolos_entrada = config["alfabeto_entrada"]
            self.simbolos_cinta = config["alfabeto_cinta"]
            self.estado_inicial = config["estado_inicial"]
            self.simbolo_blanco = config["simbolo_blanco"]
            self.estados_finales = config["estados_finales"]
            self.tabla_transicion = config["tabla_transicion"]
            
            print(f"Configuración cargada con éxito: {len(self.estados)} estados, " 
                  f"{len(self.simbolos_cinta)} símbolos")
                  
        except Exception as e:
            print(f"Error al cargar la configuración: {e}")
            raise
            
    def inicializar_cinta(self, entrada):
        for simbolo in entrada:
            if simbolo not in self.simbolos_entrada:
                raise ValueError(f"Símbolo inválido en entrada: {simbolo}")
        
        margen = 50
        self.cinta = ([self.simbolo_blanco] * 5) + list(entrada) + ([self.simbolo_blanco] * margen)
        self.cabezal = 5
        self.estado_actual = self.estado_inicial
        self.pasos = 0
    
    def obtener_simbolo_actual(self):
        return self.cinta[self.cabezal]
    
    def ejecutar_paso(self):
        simbolo_actual = self.obtener_simbolo_actual()
        
        if self.estado_actual not in self.tabla_transicion:
            print(f"Advertencia: No hay transiciones definidas para el estado '{self.estado_actual}'")
            print("Finalizando ejecución...")
            return True
            
        if simbolo_actual not in self.tabla_transicion[self.estado_actual]:
            print(f"Advertencia: No hay transición para el símbolo '{simbolo_actual}' en el estado '{self.estado_actual}'")
            print("Finalizando ejecución...")
            return True
        
        transicion = self.tabla_transicion[self.estado_actual][simbolo_actual]
        nuevo_estado, nuevo_simbolo, movimiento = transicion
        
        self.cinta[self.cabezal] = nuevo_simbolo
        self.estado_actual = nuevo_estado
        self.cabezal += movimiento
        
        if self.cabezal >= len(self.cinta) - 2:
            self.cinta.extend([self.simbolo_blanco] * 20)
        elif self.cabezal <= 1:
            self.cinta = ([self.simbolo_blanco] * 20) + self.cinta
            self.cabezal += 20
            
        self.pasos += 1
        
        self.mostrar_estado()
        
        terminado = self.estado_actual in self.estados_finales
        
        if not terminado:
            simbolo_siguiente = self.obtener_simbolo_actual()
            if (self.estado_actual not in self.tabla_transicion or 
                simbolo_siguiente not in self.tabla_transicion[self.estado_actual]):
                print(f"Advertencia: No hay transición definida para el símbolo '{simbolo_siguiente}' en el estado '{self.estado_actual}'")
                print("Finalizando ejecución...")
                terminado = True
                
        return terminado
        
    def mostrar_estado(self):
        inicio = max(0, self.cabezal - 10)
        fin = min(len(self.cinta), self.cabezal + 11)
        porcion_cinta = self.cinta[inicio:fin]
        
        representacion = ""
        for i in range(len(porcion_cinta)):
            if inicio + i == self.cabezal:
                representacion += f"[{porcion_cinta[i]}]"
            else:
                representacion += f" {porcion_cinta[i]} "
                
        print(f"Paso {self.pasos} | Estado: {self.estado_actual}")
        print(f"Cabezal en posición: {self.cabezal}")
        print(representacion)
        print("=" * 40)
    
    def ejecutar(self, entrada):
        self.inicializar_cinta(entrada)
        self.tiempo_inicio = time.time()
        print(f"\nIniciando máquina de Turing para entrada: {entrada}")
        print("=" * 40)
        
        terminado = False
        while not terminado:
            terminado = self.ejecutar_paso()
            if self.pasos > 1000:
                print("Límite de pasos alcanzado - posible bucle infinito")
                break
                
        tiempo_total = time.time() - self.tiempo_inicio
        print(f"\nEjecución finalizada en {self.pasos} pasos")
        print(f"Tiempo total: {tiempo_total:.6f} segundos")
        
        resultado = self.cinta.count('1')
        
        print(f"\nResultado: {resultado}")
        print(f"Contenido final de la cinta: {''.join(self.cinta).replace('B', '□')}")
        
        return resultado
    
    def analizar_rendimiento(self, entradas):
        resultados = []
        
        for entrada in entradas:
            self.inicializar_cinta(entrada)
            self.tiempo_inicio = time.time()
            
            terminado = False
            while not terminado and self.pasos <= 1000:
                terminado = self.ejecutar_paso()
                
            tiempo_total = time.time() - self.tiempo_inicio
            resultado = self.cinta.count('1')
            
            resultados.append({
                'entrada': entrada,
                'longitud': len(entrada),
                'resultado': resultado,
                'pasos': self.pasos,
                'tiempo': tiempo_total
            })
            
            print(f"Entrada: {entrada} ({len(entrada)}) → Resultado: {resultado} → Tiempo: {tiempo_total:.6f}s")
            
        return resultados