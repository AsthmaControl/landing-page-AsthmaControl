import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import random
import networkx as nx
import matplotlib.pyplot as plt

# === Funciones ===
def pedir_numero_nodos():
    while True:
        n = simpledialog.askinteger("Cantidad de nodos", "Ingrese un número entre 6 y 12:")
        if n is None: return None
        if 6 <= n <= 12: return n
        messagebox.showerror("Error", "Debe ingresar un número entre 6 y 12.")

def elegir_modo():
    while True:
        modo = simpledialog.askinteger("Modo", "Seleccione modo de generación:\n1. Manual\n2. Aleatorio")
        if modo is None: return None
        if modo in (1,2): return modo
        messagebox.showerror("Error", "Ingrese 1 (Manual) o 2 (Aleatorio).")

def generar_matriz(n, modo):
    matriz = [[0]*n for _ in range(n)]
    if modo == 1:
        for i in range(n):
            for j in range(n):
                if i == j:
                    matriz[i][j] = 1  # diagonal en 1
                    continue
                while True:
                    val = simpledialog.askinteger("Arista", f"¿Existe arista de {i+1} → {j+1}? (0=No, 1=Sí)")
                    if val is None:
                        # Si cierra el diálogo, asumimos 0 para no bloquear
                        val = 0
                    if val in (0,1):
                        matriz[i][j] = val
                        break
                    messagebox.showerror("Error", "Debe ingresar 0 o 1.")
    else:
        for i in range(n):
            for j in range(n):
                if i != j: matriz[i][j] = random.randint(0,1)
    return matriz

def poner_diagonal(matriz):
    for i in range(len(matriz)):
        matriz[i][i] = 1

def matriz_caminos_warshall(matriz):
    n = len(matriz)
    caminos = [row[:] for row in matriz]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                caminos[i][j] = caminos[i][j] or (caminos[i][k] and caminos[k][j])
    return caminos

def ordenar_por_cantidad_unos(matriz):
    cantidad_unos = [sum(row) for row in matriz]
    orden = sorted(range(len(matriz)), key=lambda x: cantidad_unos[x], reverse=True)
    return orden, cantidad_unos

def intercambiar_columnas(matriz, c1, c2):
    for fila in matriz:
        fila[c1], fila[c2] = fila[c2], fila[c1]

def detectar_componentes(matriz, ordenFilas, ordenColumnas):
    n = len(matriz)
    visitado = [False]*n
    actual = 0
    comp = 1
    componentes = []
    texto = ""
    while actual < n:
        if visitado[actual]:
            actual += 1
            continue
        unos = sum(matriz[ordenFilas[actual]][ordenColumnas[j]] for j in range(n))
        # Asegurarse que siempre haya al menos 1 nodo
        unos = max(1, unos)
        grupo = []
        texto += f"\nComponente conexa {comp}: "
        for k in range(actual, min(actual + unos, n)):
            texto += f"{ordenFilas[k]+1}"
            grupo.append(ordenFilas[k]+1)
            visitado[k] = True
            if k < actual + unos - 1:
                texto += ", "
        texto += " }\n"
        componentes.append(grupo)
        actual += unos
        comp += 1
    return componentes, texto

def mostrar_matriz_textual(titulo, matriz, indices=None):
    n = len(matriz)
    texto = titulo + "\n    "
    for i in range(n):
        texto += f"{(indices[i]+1 if indices else i+1):2} "
    texto += "\n"
    for i in range(n):
        texto += f"{(indices[i]+1 if indices else i+1):2} | "
        for j in range(n):
            row = indices[i] if indices else i
            col = indices[j] if indices else j
            texto += f"{matriz[row][col]:2} "
        texto += "\n"
    return texto

def dibujar_grafo_final(matriz_original, componentes):
    n = len(matriz_original)
    G = nx.DiGraph()
    for i in range(n):
        for j in range(n):
            if i != j and matriz_original[i][j] == 1:
                G.add_edge(i+1, j+1)

    pos = nx.spring_layout(G, seed=42, k=2.0)

    colores = ['red','blue','green','orange','purple','gold','cyan','magenta']
    node_colors = []
    for nodo in G.nodes():
        color_asignado = False
        for idx, comp in enumerate(componentes):
            if nodo in comp:
                node_colors.append(colores[idx%len(colores)])
                color_asignado = True
                break
        if not color_asignado:
            node_colors.append('gray')

    plt.figure(figsize=(10,10))
    nx.draw(
        G, pos, with_labels=True, node_color=node_colors, node_size=1000,
        edge_color='gray', arrows=True, arrowsize=20, font_weight='bold',
        connectionstyle='arc3,rad=0.2'
    )
    plt.title("Grafo final de componentes conexas")
    plt.show()

# === Función para generar matriz y mostrar pasos ===
def generar_y_mostrar_grafo(root, n, modo):
    matriz = generar_matriz(n, modo)
    if matriz is None: return

    pasos = []
    pasos.append(mostrar_matriz_textual("Matriz de adyacencia original:", matriz))
    poner_diagonal(matriz)
    pasos.append(mostrar_matriz_textual("Matriz de adyacencia (con diagonal en 1):", matriz))
    caminos = matriz_caminos_warshall(matriz)
    pasos.append(mostrar_matriz_textual("Matriz de caminos:", caminos))
    ordenFilas, _ = ordenar_por_cantidad_unos(caminos)
    ordenColumnas = ordenFilas[:]
    for i in range(len(caminos)):
        while ordenColumnas[i] != i:
            intercambiar_columnas(caminos, i, ordenColumnas[i])
            ordenColumnas[i], ordenColumnas[ordenColumnas[i]] = ordenColumnas[ordenColumnas[i]], ordenColumnas[i]
    pasos.append(mostrar_matriz_textual("Matriz ordenada por filas y columnas:", caminos, ordenFilas))
    componentes, texto_comp = detectar_componentes(caminos, ordenFilas, ordenColumnas)
    pasos.append(texto_comp)

    ventana = tk.Toplevel(root)
    ventana.title("Componentes Conexas - Paso a Paso")
    ventana.geometry("700x700")
    txt = scrolledtext.ScrolledText(ventana, width=80, height=35, font=("Consolas",10))
    txt.pack(padx=10,pady=10)

    paso_actual = 0
    def siguiente():
        nonlocal paso_actual
        if paso_actual < len(pasos):
            txt.insert(tk.END,"\n"+pasos[paso_actual])
            paso_actual += 1
            txt.see(tk.END)
        else:
            boton.config(state="disabled")
            dibujar_grafo_final(matriz, componentes)

    boton = tk.Button(ventana, text="Siguiente paso", command=siguiente,
                      bg="#2196F3", fg="white", font=("Arial",10,"bold"))
    boton.pack(pady=5)

    # Mostrar automáticamente el primer paso
    siguiente()

# === Programa principal ===
def main():
    root = tk.Tk()
    root.withdraw()  # Ocultamos la ventana Tk vacía

    # Ventana inicial
    ventana_inicial = tk.Toplevel(root)
    ventana_inicial.title("Detección de Componentes Conexas")
    ventana_inicial.geometry("600x300")
    ventana_inicial.resizable(False, False)

    titulo = tk.Label(ventana_inicial, text="🔹 Componentes Conexas 🔹", 
                      font=("Bebas Neue", 24), fg="#2196F3")
    titulo.pack(pady=(30,10))

    subtitulo = tk.Label(ventana_inicial, text="Visualiza paso a paso la conexión de los nodos de un grafo",
                         font=("Montserrat", 12), fg="gray")
    subtitulo.pack(pady=(0,20))

    def iniciar():
        n = pedir_numero_nodos()
        if n is None: return
        modo = elegir_modo()
        if modo is None: return
        ventana_inicial.destroy()
        generar_y_mostrar_grafo(root, n, modo)

    boton = tk.Button(ventana_inicial, text="Iniciar", command=iniciar,
                      font=("Montserrat", 12, "bold"), bg="#2196F3", fg="white")
    boton.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
