import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import random
import networkx as nx
import matplotlib.pyplot as plt

# -----------------------------------------------------------
# Función para generar la matriz de adyacencia
# -----------------------------------------------------------
def generar_matriz(n, modo):
    matriz = [[0]*n for _ in range(n)]
    if modo == 1:  # Manual
        for i in range(n):
            for j in range(n):
                val = simpledialog.askinteger(
                    "Matriz de adyacencia",
                    f"Ingrese 0 o 1 para la posición ({i+1}, {j+1})",
                    minvalue=0,
                    maxvalue=1
                )
                if val is None:
                    val = 0
                matriz[i][j] = val
    else:  # Aleatorio
        for i in range(n):
            for j in range(n):
                if i != j:
                    matriz[i][j] = random.randint(0, 1)
    return matriz

# -----------------------------------------------------------
# Algoritmo de Warshall para matriz de caminos
# -----------------------------------------------------------
def matriz_caminos_warshall(matriz):
    n = len(matriz)
    caminos = [row[:] for row in matriz]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                caminos[i][j] = caminos[i][j] or (caminos[i][k] and caminos[k][j])
    return caminos

# -----------------------------------------------------------
# Mostrar la matriz como texto legible (MODIFICADO)
# -----------------------------------------------------------
def mostrar_matriz_textual(titulo, matriz, orden=None):
    n = len(matriz)
    
    # Determinar las etiquetas para filas y columnas
    # Si 'orden' se proporciona, usamos esos índices (sumando 1)
    # Si no, usamos la secuencia normal (1, 2, ... n)
    etiquetas_columnas = [f"{(idx+1):2}" for idx in orden] if orden else [f"{(i+1):2}" for i in range(n)]
    etiquetas_filas = [f"{(idx+1):2}" for idx in orden] if orden else [f"{(i+1):2}" for i in range(n)]

    texto = f"{titulo}\n"
    
    # Cabecera de columnas
    texto += "    " + " ".join(etiquetas_columnas) + "\n"
    
    for i, fila in enumerate(matriz):
        # Cabecera de fila
        texto += f"{etiquetas_filas[i]} | " + " ".join([f"{v:2}" for v in fila]) + "\n"
    
    return texto + "\n"


# -----------------------------------------------------------
# Detectar componentes conexas a partir de matriz de caminos
# -----------------------------------------------------------
def componentes_por_caminos(matriz_caminos):
    n = len(matriz_caminos)
    visitado = [False]*n
    componentes = []
    texto = ""
    comp = 1

    for i in range(n):
        if not visitado[i]:
            grupo = [i+1]
            visitado[i] = True
            for j in range(n):
                # Si i puede llegar a j y j puede llegar a i → están en la misma componente
                if matriz_caminos[i][j] == 1 and matriz_caminos[j][i] == 1 and not visitado[j]:
                    visitado[j] = True
                    grupo.append(j+1)
            componentes.append(sorted(grupo))
            texto += f"Componente conexa {comp}: {{ " + ", ".join(map(str, sorted(grupo))) + " }\n"
            comp += 1

    # 🔹 Mostrar número total de componentes al final
    texto += f"\nTotal de componentes conexas: {len(componentes)}\n"

    return componentes, texto

# -----------------------------------------------------------
# Dibujar grafo final con colores por componente (sin bucles)
# -----------------------------------------------------------
def dibujar_grafo_final(matriz, componentes):
    G = nx.DiGraph()
    n = len(matriz)
    for i in range(n):
        G.add_node(i+1)
    # Añadimos solo aristas entre nodos distintos (evitar bucles i->i)
    for i in range(n):
        for j in range(n):
            if i != j and matriz[i][j] == 1:
                G.add_edge(i+1, j+1)

    colores = ["#ff9999", "#99ff99", "#9999ff", "#ffcc99", "#ff99ff", "#99ffff"]
    color_map = {}
    for idx, comp in enumerate(componentes):
        for nodo in comp:
            color_map[nodo] = colores[idx % len(colores)]
    node_colors = [color_map.get(i+1, "#cccccc") for i in range(n)]

    pos = nx.spring_layout(G)
    plt.figure(figsize=(6, 6))
    nx.draw(G, pos, with_labels=True, node_color=node_colors,
            node_size=800, font_size=10, font_weight="bold", arrows=True)
    plt.title("Grafo - Componentes conexas")
    plt.show()

# -----------------------------------------------------------
# Generar y mostrar todo paso a paso (5 pasos solicitados)
# -----------------------------------------------------------
def generar_y_mostrar_grafo(root, n, modo):
    matriz = generar_matriz(n, modo)
    if matriz is None:
        messagebox.showerror("Error", "No se pudo generar la matriz.")
        return

    pasos = []

    # PASO 1: Matriz de adyacencia original
    pasos.append(mostrar_matriz_textual("Matriz de adyacencia original:", matriz))

    # PASO 2: Matriz con diagonal en 1 (no modificamos la matriz original para otros usos; hacemos copia)
    matriz_diagonal = [row[:] for row in matriz]
    for i in range(n):
        matriz_diagonal[i][i] = 1
    pasos.append(mostrar_matriz_textual("Matriz de adyacencia (con diagonal en 1):", matriz_diagonal))

    # PASO 3: Matriz de caminos (usar la matriz con diagonal)
    caminos = matriz_caminos_warshall(matriz_diagonal)
    pasos.append(mostrar_matriz_textual("Matriz de caminos:", caminos))

    # PASO 4: Matriz ordenada por filas y columnas (orden descendente por cantidad de unos)
    cantidad_unos = [sum(caminos[i]) for i in range(n)]
    orden = sorted(range(n), key=lambda x: cantidad_unos[x], reverse=True)
    # construimos matriz ordenada permutando filas y columnas según 'orden'
    matriz_ordenada = [[caminos[i][j] for j in orden] for i in orden]
    
    # (MODIFICADO) - Le pasamos la lista 'orden' a la función de mostrar
    pasos.append(mostrar_matriz_textual("Matriz ordenada por filas y columnas:", matriz_ordenada, orden))

    # PASO 5: Componentes conexas (calculadas a partir de 'caminos')
    componentes, texto_comp = componentes_por_caminos(caminos)
    pasos.append("Componente(s) detectada(s):\n" + texto_comp)

    # Ventana de pasos
    ventana = tk.Toplevel(root)
    ventana.title("Componentes Conexas - Paso a Paso")
    ventana.geometry("700x700")

    txt = scrolledtext.ScrolledText(ventana, width=80, height=35, font=("Consolas", 10))
    txt.pack(padx=10, pady=10)

    paso_actual = 0

    def siguiente():
        nonlocal paso_actual
        if paso_actual < len(pasos):
            txt.insert(tk.END, "\n" + pasos[paso_actual])
            paso_actual += 1
            txt.see(tk.END)
        else:
            boton.config(state="disabled")
            # Para dibujar el grafo final usamos la matriz original con diagonal=1
            # (si prefieres usar otra matriz, cámbialo aquí)
            dibujar_grafo_final(matriz_diagonal, componentes)

    boton = tk.Button(
        ventana, text="Siguiente paso", command=siguiente,
        bg="#2196F3", fg="white", font=("Arial", 10, "bold")
    )
    boton.pack(pady=5)

    siguiente()  # Mostrar el primer paso automáticamente

# -----------------------------------------------------------
# Ventana principal
# -----------------------------------------------------------
def main():
    root = tk.Tk()
    root.title("Generador de Grafos - Componentes Conexas")
    root.geometry("400x300")

    lbl = tk.Label(root, text="Ingrese el número de nodos:", font=("Arial", 12))
    lbl.pack(pady=10)

    entry = tk.Entry(root, font=("Arial", 12))
    entry.pack(pady=5)

    def iniciar(modo):
        try:
            n = int(entry.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido de nodos.")
            return

        # 🔹 Validación del rango permitido
        if n < 6 or n > 12:
            messagebox.showerror("Error", "El número de nodos debe estar entre 6 y 12.")
            return

        generar_y_mostrar_grafo(root, n, modo)


    btn_manual = tk.Button(root, text="Modo Manual", command=lambda: iniciar(1),
                            bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=15)
    btn_manual.pack(pady=10)

    btn_auto = tk.Button(root, text="Modo Aleatorio", command=lambda: iniciar(2),
                            bg="#2196F3", fg="white", font=("Arial", 12, "bold"), width=15)
    btn_auto.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()