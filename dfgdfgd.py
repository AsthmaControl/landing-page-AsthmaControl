##matematica computacional

import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import random
import networkx as nx
import matplotlib.pyplot as plt

def pedir_numero_nodos_ventana():
    while True:
        n = simpledialog.askinteger("Nodos", "Ingrese la cantidad de nodos (6 a 12):")
        if n is None:
            return None
        if 6 <= n <= 12:
            return n
        else:
            messagebox.showerror("Error", "Debe ingresar un número entre 6 y 12.")

def elegir_modo_generacion_ventana():
    while True:
        modo = simpledialog.askinteger("Modo", "Seleccione modo de generación:\n1. Manual\n2. Aleatorio")
        if modo is None:
            return None
        if modo in (1, 2):
            return modo
        else:
            messagebox.showerror("Error", "Ingrese 1 para Manual o 2 para Aleatorio.")

def generar_matriz_adyacencia_ventana(n, modo):
    matriz = [[0]*n for _ in range(n)]
    if modo == 1:
        for i in range(n):
            for j in range(n):
                while True:
                    valor = simpledialog.askinteger("Arista", f"¿Hay arista de {i+1} a {j+1}?\n(0 = No, 1 = Sí)")
                    if valor is None:
                        return None
                    if valor in (0, 1):
                        matriz[i][j] = valor
                        break
                    else:
                        messagebox.showerror("Error", "Ingrese 0 o 1.")
    else:
        for i in range(n):
            for j in range(n):
                matriz[i][j] = 0 if i == j else random.randint(0, 1)
    return matriz

def poner_diagonal(matriz):
    n = len(matriz)
    for i in range(n):
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
    n = len(matriz)
    cantidad_unos = [sum(matriz[i]) for i in range(n)]
    orden = sorted(range(n), key=lambda x: cantidad_unos[x], reverse=True)
    return orden, cantidad_unos

def intercambiar_columnas(matriz, col1, col2):
    n = len(matriz)
    for i in range(n):
        matriz[i][col1], matriz[i][col2] = matriz[i][col2], matriz[i][col1]

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
        unos = 0
        for j in range(n):
            if matriz[ordenFilas[actual]][ordenColumnas[j]] == 1:
                unos += 1
        grupo = []
        texto += f"\nComponente conexa {comp}: {{ "
        for k in range(actual, actual + unos):
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

def graficar_grafo(matriz, componentes=None, titulo="Grafo"):
    n = len(matriz)
    G = nx.Graph()
    G.add_nodes_from(range(1, n+1))
    for i in range(n):
        for j in range(n):
            if matriz[i][j] == 1 and i < j:
                G.add_edge(i+1, j+1)
    plt.figure(figsize=(7,7))
    pos = nx.spring_layout(G, seed=42)
    if componentes:
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'gold', 'cyan', 'magenta']
        node_colors = []
        for node in G.nodes():
            color_found = False
            for idx, comp in enumerate(componentes):
                if node in comp:
                    node_colors.append(colors[idx % len(colors)])
                    color_found = True
                    break
            if not color_found:
                node_colors.append('gray')
        nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=800, edge_color='gray', font_weight='bold')
    else:
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=800, edge_color='gray', font_weight='bold')
    plt.title(titulo)
    plt.show()

def main_ventana():
    root = tk.Tk()
    root.withdraw()

    n = pedir_numero_nodos_ventana()
    if n is None: return
    modo = elegir_modo_generacion_ventana()
    if modo is None: return
    matriz = generar_matriz_adyacencia_ventana(n, modo)
    if matriz is None: return

    texto = ""
    texto += mostrar_matriz_textual("Matriz de adyacencia original:", matriz)
    graficar_grafo(matriz, titulo="Grafo de adyacencia original")

    poner_diagonal(matriz)
    texto += "\n" + mostrar_matriz_textual("Matriz de adyacencia (con diagonal en 1):", matriz)
    graficar_grafo(matriz, titulo="Grafo de adyacencia con diagonal en 1")

    caminos = matriz_caminos_warshall(matriz)
    texto += "\n" + mostrar_matriz_textual("Matriz de caminos:", caminos)

    ordenFilas, cantidadUnos = ordenar_por_cantidad_unos(caminos)
    ordenColumnas = ordenFilas[:]
    for i in range(n):
        while ordenColumnas[i] != i:
            intercambiar_columnas(caminos, i, ordenColumnas[i])
            ordenColumnas[i], ordenColumnas[ordenColumnas[i]] = ordenColumnas[ordenColumnas[i]], ordenColumnas[i]
    texto += "\n" + mostrar_matriz_textual("Matriz ordenada por filas y columnas:", caminos, ordenFilas)
    componentes, texto_comp = detectar_componentes(caminos, ordenFilas, ordenColumnas)
    texto += texto_comp

    graficar_grafo(matriz, componentes, "Grafo coloreado por componentes conexas")

    ventana = tk.Toplevel()
    ventana.title("Reporte de Componentes Conexas")
    ventana.geometry("700x700")
    txt = scrolledtext.ScrolledText(ventana, width=80, height=40, font=("Consolas", 10))
    txt.pack(padx=10, pady=10)
    txt.insert(tk.END, texto)
    txt.config(state=tk.DISABLED)
    ventana.mainloop()

if __name__ == "__main__":
    main_ventana()