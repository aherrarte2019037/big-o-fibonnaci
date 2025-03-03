import time
import json
import matplotlib.pyplot as plt
import numpy as np

ARCHIVO_CONFIG = 'config.json'

class SimuladorFibonacci:

    def __init__(self, cinta, tabla_transiciones, posicion_inicial=1):
        self.cinta = cinta
        self.posicion = posicion_inicial
        self.tabla_transiciones = tabla_transiciones
        self.valor_actual = self.cinta[self.posicion]
        self.estado_actual = "0"
        self.contador_pasos = 0
    
    def avanzar_paso(self):
        # Leer el valor actual de la cinta
        self.valor_actual = self.cinta[self.posicion]
        
        # Verificar si hay una transición definida para el estado y símbolo actuales
        if self.valor_actual not in self.tabla_transiciones[self.estado_actual]:
            print(f"Error: No hay transición definida para el estado {self.estado_actual} y el símbolo {self.valor_actual}")
            return True
        
        # Obtener la nueva configuración de la tabla de transiciones
        nueva_transicion = self.tabla_transiciones[self.estado_actual][self.valor_actual]
        
        # Actualizar el estado, el símbolo en la cinta y la posición del cabezal
        self.estado_actual = nueva_transicion[0]
        self.cinta[self.posicion] = nueva_transicion[1]
        self.posicion += nueva_transicion[2]
        
        # Verificar si necesitamos expandir la cinta
        if self.posicion >= len(self.cinta) - 2:
            self.cinta.extend(["X"] * 20)
        elif self.posicion <= 1:
            self.cinta = ["X"] * 20 + self.cinta
            self.posicion += 20
        
        self.contador_pasos += 1
        
        self.mostrar_estado()
        
        return self.estado_actual == "18"
    
    def mostrar_estado(self):
        rango_visible = 20
        inicio = max(0, self.posicion - rango_visible // 2)
        fin = min(len(self.cinta), self.posicion + rango_visible // 2)
        
        cinta_visible = self.cinta[inicio:fin]
        
        representacion = ""
        for i, simbolo in enumerate(cinta_visible):
            if inicio + i == self.posicion:
                representacion += f"[{simbolo}]"
            else:
                representacion += f" {simbolo} "
        
        print(f"Paso {self.contador_pasos} | Estado: {self.estado_actual} | Posición: {self.posicion}")
        print(representacion)
        print("-" * 40)
    
    def ejecutar(self):
        inicio = time.time()
        terminado = False
        
        print("Iniciando ejecución de la máquina de Turing para Fibonacci...")
        print("-" * 40)
        
        while not terminado and self.contador_pasos < 30000:
            terminado = self.avanzar_paso()
        
        tiempo_ejecucion = time.time() - inicio
        print(f"Tiempo de ejecución: {tiempo_ejecucion:.6f} segundos")
        
        if self.contador_pasos >= 1500:
            print("¡Advertencia! Se alcanzó el límite máximo de pasos.")
        
        resultado = self.cinta.count('1')
        
        cinta_final = "".join(self.cinta).replace("X", "B")
        print(f"\nResultado: {resultado}")
        print(f"Cinta final: {cinta_final}")
        
        return resultado, self.contador_pasos, tiempo_ejecucion

def cargar_configuracion(archivo):
    try:
        with open(archivo, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"¡Error! No se encontró el archivo de configuración: {archivo}")
        print("Generando archivo de configuración predeterminado...")

def analizar_rendimiento():
    print("\nAnalizando rendimiento para n=1 hasta n=10...")
    
    configuracion = cargar_configuracion(ARCHIVO_CONFIG)
    tabla_transiciones = configuracion["transiciones"]
    
    resultados = []
    valores_esperados = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    
    for n in range(1, 11):
        entrada = "1" * n
        
        cinta = ["X"] + list(entrada) + ["X"] * 100
        
        maquina = SimuladorFibonacci(cinta, tabla_transiciones)
        resultado, pasos, tiempo = maquina.ejecutar()
        
        resultados.append({
            "n": n,
            "entrada": entrada,
            "resultado": resultado,
            "esperado": valores_esperados[n-1],
            "correcto": resultado == valores_esperados[n-1],
            "pasos": pasos,
            "tiempo": tiempo
        })
    
    print("\n===== RESULTADOS DE FIBONACCI =====")
    print("n\tEntrada\tResultado\tEsperado\tCorrecto\tPasos\tTiempo (s)")
    print("-" * 80)
    
    for r in resultados:
        correcto = "✓" if r["correcto"] else "✗"
        print(f"{r['n']}\t{r['entrada']}\t{r['resultado']}\t\t{r['esperado']}\t\t{correcto}\t\t{r['pasos']}\t{r['tiempo']:.6f}")
    
    errores = [r for r in resultados if not r["correcto"]]
    if errores:
        print("\n⚠️ ERRORES DETECTADOS:")
        for e in errores:
            print(f"- Para n={e['n']}, esperaba {e['esperado']} pero obtuve {e['resultado']}")
    else:
        print("\n✅ Todos los resultados son correctos")
    
    crear_graficas(resultados)

def crear_graficas(resultados):
    n_valores = [r["n"] for r in resultados]
    pasos = [r["pasos"] for r in resultados]
    tiempos = [r["tiempo"] for r in resultados]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    ax1.plot(n_valores, tiempos, 'o-', color='blue')
    ax1.set_title('Tiempo de ejecución vs n')
    ax1.set_xlabel('n')
    ax1.set_ylabel('Tiempo (segundos)')
    ax1.grid(True)
    
    if len(n_valores) >= 3:
        coef = np.polyfit(n_valores, tiempos, 2)
        poly = np.poly1d(coef)
        x_new = np.linspace(min(n_valores), max(n_valores), 100)
        y_new = poly(x_new)
        ax1.plot(x_new, y_new, 'r--', label=f'Ajuste: {poly}')
        ax1.legend()
    
    ax2.plot(n_valores, pasos, 'o-', color='green')
    ax2.set_title('Número de pasos vs n')
    ax2.set_xlabel('n')
    ax2.set_ylabel('Número de pasos')
    ax2.grid(True)
    
    if len(n_valores) >= 3:
        coef = np.polyfit(n_valores, pasos, 2)
        poly = np.poly1d(coef)
        x_new = np.linspace(min(n_valores), max(n_valores), 100)
        y_new = poly(x_new)
        ax2.plot(x_new, y_new, 'r--', label=f'Ajuste: {poly}')
        ax2.legend()
    
    plt.tight_layout()
    plt.savefig('Rendimiento Fibonacci.png')

def ejecutar_fibonacci():
    configuracion = cargar_configuracion(ARCHIVO_CONFIG)
    tabla_transiciones = configuracion["transiciones"]
    
    print("\nIntroduce un número en notación unaria:")
    entrada = input().strip()
    
    if not all(c == '1' for c in entrada):
        print("Error: La entrada debe contener solo caracteres '1'")
        return
    
    n = len(entrada)
    print(f"\nCalculando Fibonacci({n})...")
    
    cinta = ["X"] + list(entrada) + ["X"] * 100
    
    maquina = SimuladorFibonacci(cinta, tabla_transiciones)
    resultado, pasos, tiempo = maquina.ejecutar()
    
    print(f"\nFibonacci({n}) = {resultado}")
    print(f"\nFibonacci({n}) = {resultado}")
    print(f"Pasos totales: {pasos}")
    print(f"Tiempo de ejecución: {tiempo:.6f} segundos")

def menu_principal():
    while True:
        print("\n========================================")
        print("    MÁQUINA DE TURING PARA FIBONACCI    ")
        print("========================================")
        print("1. Calcular Fibonacci para una entrada")
        print("2. Analizar rendimiento")
        print("3. Salir")
        
        opcion = input("\nSelecciona una opción (1-3): ").strip()
        
        if opcion == "1":
            ejecutar_fibonacci()
        elif opcion == "2":
            analizar_rendimiento()
        elif opcion == "3":
            print("\nSaliendo del programa...")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    menu_principal()