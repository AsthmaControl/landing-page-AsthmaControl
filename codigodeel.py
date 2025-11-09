import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import random
import networkx as nx
import matplotlib.pyplot as plt
import copy

class GraphComponentsApp:
    def __init__(self):
        # Ocultar la ventana raíz principal de tkinter
        self.root = tk.Tk()
        self.root.withdraw()
        
        # Atributos para almacenar el estado del grafo
        self.n_nodes = 0
        self.adj_matrix = []
        self.graph = None
        self.labels = [] # Lista para guardar las etiquetas (A, B, C...)

    def on_close_results(self):
        """Manejador para cerrar la ventana de resultados y terminar el mainloop."""
        try:
            plt.close('all') # Cerrar cualquier figura de matplotlib
        except Exception:
            pass # Ignorar errores al cerrar plt
        self.root.quit()
        self.root.destroy()

    def run(self):
        """Inicia el flujo principal de la aplicación."""
        
        # 1. Obtener el número de nodos (n)
        self.n_nodes = self.get_node_count()
        if self.n_nodes is None:
            messagebox.showinfo("Cancelado", "La operación fue cancelada.")
            return
            
        # Crear las etiquetas de letras (A, B, C...)
        self.labels = [chr(ord('A') + i) for i in range(self.n_nodes)]

        # 2. Elegir el modo de generación
        is_random = self.get_generation_choice()
        if is_random is None:
            messagebox.showinfo("Cancelado", "La operación fue cancelada.")
            return

        # 3. Construir el grafo
        if is_random:
            self.graph, self.adj_matrix = self.build_graph_random(self.n_nodes)
        else:
            self.graph, self.adj_matrix = self.build_graph_manual(self.n_nodes)
        
        if self.graph is None:
            messagebox.showinfo("Cancelado", "La operación fue cancelada.")
            return

        # 4. --- ALGORITMO ---
        try:
            (components, 
             steps_log, 
             sorted_matrix, 
             sorted_labels) = self.calculate_path_matrix_sequential(self.adj_matrix)
        except Exception as e:
            messagebox.showerror("Error en el Algoritmo", f"Ocurrió un error durante el cálculo: {e}")
            return

        # 5. Mostrar los resultados
        self.show_results(self.adj_matrix, sorted_matrix, sorted_labels, steps_log, components)
        
        # 6. Iniciar el bucle de eventos de tkinter
        self.root.mainloop()

    def get_node_count(self):
        """Solicita al usuario un entero n en el rango [6, 12]."""
        n = None
        while n is None:
            n = simpledialog.askinteger("Número de Nodos",
                                        "Ingresa el número de nodos (n):\n(Máximo 12, de A a Z)",
                                        initialvalue=7, minvalue=6, maxvalue=12,
                                        parent=self.root)
            if n is None:
                return None 
            if not (6 <= n <= 12):
                messagebox.showerror("Error", "El número 'n' debe estar en el rango [6, 12].")
                n = None 
        return n

    def get_generation_choice(self):
        """Pregunta al usuario si desea generación aleatoria o manual."""
        choice = messagebox.askyesno("Modo de Generación",
                                     "¿Deseas generar el grafo de forma aleatoria?\n\n(Presiona 'No' para crearlo manualmente)")
        return choice

    def build_graph_random(self, n):
        """Construye un grafo DIRIGIDO y su matriz aleatoriamente."""
        g = nx.DiGraph() # Grafo Dirigido
        g.add_nodes_from(range(n))
        matrix = [[0] * n for _ in range(n)]
        edge_probability = 0.3
        
        for i in range(n):
            for j in range(n): # Bucle completo
                if random.random() < edge_probability:
                    g.add_edge(i, j)
                    matrix[i][j] = 1
                    
        return g, matrix

    def build_graph_manual(self, n):
        """Construye un grafo DIRIGIDO y su matriz manualmente."""
        g = nx.DiGraph() # Grafo Dirigido
        g.add_nodes_from(range(n))
        matrix = [[0] * n for _ in range(n)]

        for i in range(n):
            for j in range(n):
                add_edge = messagebox.askyesno("Creación Manual",
                                               f"¿Existe una arista DESDE {self.labels[i]} HACIA {self.labels[j]}?")
                if add_edge is None:
                     return None, None # El usuario canceló
                if add_edge:
                    g.add_edge(i, j)
                    matrix[i][j] = 1
        
        return g, matrix

    def calculate_path_matrix_sequential(self, adj_matrix):
        """
        Algoritmo de 5 pasos:
        1. Diagonal de 1s
        2. Cálculo secuencial fila por fila (y lo registra)
        3. Ordena filas
        4. Ordena columnas
        5. Extrae componentes de la matriz ordenada
        """
        n = len(adj_matrix)
        labels = self.labels
        steps_log = [] 

        # --- Paso 1: Inicialización ---
        path_matrix = copy.deepcopy(adj_matrix)
        for i in range(n):
            path_matrix[i][i] = 1
        
        steps_log.append("=== INICIO DEL CÁLCULO SECUENCIAL ===")
        steps_log.append("P0: Matriz de Adyacencia (con diagonal de 1s)")
        steps_log.append(self.format_matrix_string(path_matrix, labels, labels))
        steps_log.append("\n" + "-"*40 + "\n")

        # --- Paso 2: Cálculo Secuencial Fila por Fila ---
        
        # Iteramos fila por fila. 'k' es la fila que estamos calculando
        for k in range(n):
            k_label = labels[k]
            steps_log.append(f"Paso {k+1}: Procesando Fila {k_label}")
            
            # Encontrar las filas que necesitamos combinar
            rows_to_combine_indices = []
            for j in range(n): # Mirar los 1s en la fila k
                if path_matrix[k][j] == 1:
                    rows_to_combine_indices.append(j)
            
            rows_to_combine_labels = [labels[i] for i in rows_to_combine_indices]
            steps_log.append(f"  -> La Fila {k_label} (actual) tiene 1s en columnas: {rows_to_combine_labels}")
            steps_log.append(f"  -> La Nueva Fila {k_label} será un OR de las filas: {rows_to_combine_labels}")

            # Calcular la nueva fila
            new_row = [0] * n
            for row_index in rows_to_combine_indices:
                for col in range(n):
                    # Aplicamos el OR con la fila 'row_index' de la matriz actual
                    new_row[col] = new_row[col] or path_matrix[row_index][col]
            
            # Actualizar la matriz
            path_matrix[k] = new_row
            
            # Registrar el estado de la matriz DESPUÉS de la actualización
            steps_log.append(f"\nMatriz P{k+1} (Fila {k_label} actualizada y bloqueada):")
            steps_log.append(self.format_matrix_string(path_matrix, labels, labels))
            steps_log.append("\n" + "-"*40 + "\n")

        steps_log.append("=== CÁLCULO SECUENCIAL TERMINADO ===")
        final_matrix = path_matrix
        
        # --- Paso 3: Ordenar Filas ---
        steps_log.append("\n=== PASO 3: ORDENANDO FILAS (por 1s, luego alfabético) ===")
        
        # Guardamos la info de cada fila
        row_data = []
        for i in range(n):
            num_ones = sum(final_matrix[i])
            row_data.append({'label': labels[i], 'row': final_matrix[i], 'ones': num_ones})
            
        # Creamos la función de ordenamiento
        def sort_key(item):
            # Criterio 1: Número de 1s (descendente)
            # Criterio 2: Etiqueta (alfabético ascendente)
            return (-item['ones'], item['label'])
            
        row_data.sort(key=sort_key)
        
        # Extraer el nuevo orden de etiquetas y la matriz solo con filas ordenadas
        sorted_row_labels = [item['label'] for item in row_data]
        row_sorted_matrix = [item['row'] for item in row_data]
        
        steps_log.append(f"Nuevo orden de filas: {sorted_row_labels}")
        
        # --- Paso 4: Ordenar Columnas ---
        steps_log.append("\n=== PASO 4: ORDENANDO COLUMNAS (para coincidir con filas) ===")
        
        # Mapeo de la etiqueta original a su índice (A:0, B:1...)
        old_label_to_index = {label: i for i, label in enumerate(labels)}
        # Lista de los índices originales, pero en el nuevo orden (E:4, F:5, G:6...)
        new_index_order = [old_label_to_index[label] for label in sorted_row_labels]
        
        fully_sorted_matrix = []
        for i in range(n):
            new_row_for_sorted_matrix = [0] * n
            for j in range(n):
                # La nueva columna 'j' corresponde a un índice antiguo
                old_col_index = new_index_order[j]
                new_row_for_sorted_matrix[j] = row_sorted_matrix[i][old_col_index]
            fully_sorted_matrix.append(new_row_for_sorted_matrix)
            
        steps_log.append("Matriz Final (Filas y Columnas Ordenadas):")
        steps_log.append(self.format_matrix_string(fully_sorted_matrix, sorted_row_labels, sorted_row_labels))
        steps_log.append("\n" + "-"*40 + "\n")
        
        # --- Paso 5: Extracción de Componentes ---
        steps_log.append("=== PASO 5: EXTRACCIÓN DE COMPONENTES (de la matriz ordenada) ===")
        components = []
        visited = set()
        
        for i in range(n):
            label_i = sorted_row_labels[i]
            if label_i in visited:
                continue
                
            current_component = [label_i]
            visited.add(label_i)
            steps_log.append(f"Analizando nodo {label_i} (no visitado)...")
            
            # Buscar conexiones mutuas (M[i][j] == 1 Y M[j][i] == 1)
            for j in range(i + 1, n):
                label_j = sorted_row_labels[j]
                if label_j in visited:
                    continue
                
                # fully_sorted_matrix[i][j] es M[label_i][label_j]
                # fully_sorted_matrix[j][i] es M[label_j][label_i]
                if fully_sorted_matrix[i][j] == 1 and fully_sorted_matrix[j][i] == 1:
                    steps_log.append(f"  -> {label_i} y {label_j} son mutuamente conexos. Agregando a componente.")
                    current_component.append(label_j)
                    visited.add(label_j)
                else:
                    # Si no hay conexión mutua, el bloque se rompe
                    steps_log.append(f"  -> {label_i} y {label_j} NO son mutuamente conexos. El bloque termina.")
                    break 
            
            components.append(current_component)
            steps_log.append(f"  -> Componente encontrado: {current_component}")

        steps_log.append("\nExtracción de componentes completada.")
        
        return components, "\n".join(steps_log), fully_sorted_matrix, sorted_row_labels
        

    def format_matrix_string(self, matrix, row_labels, col_labels):
        n = len(matrix)
        # Encabezado (Etiquetas de Columna)
        header = "    " + " ".join([f"{label:>2}" for label in col_labels])
        lines = [header, "   " + "-" * (n * 3)]
        
        for i, row in enumerate(matrix):
            row_str = " ".join([f"{int(cell):2}" for cell in row])
            # Etiqueta de Fila
            lines.append(f"{row_labels[i]:>2} | {row_str}")
            
        return "\n".join(lines)

    def show_results(self, adj_matrix, sorted_path_matrix, sorted_labels, steps, components):
        """Muestra todos los resultados en una ventana de ScrolledText."""
        
        result_window = tk.Toplevel(self.root)
        result_window.title("Resultados - Componentes Conexas")
        result_window.geometry("700x600")

        txt_area = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, width=80, height=30, font=("Courier New", 9))
        txt_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        output = []
        
        # 1. Matriz de Adyacencia
        output.append("=== MATRIZ DE ADYACENCIA ===")
        output.append(self.format_matrix_string(adj_matrix, self.labels, self.labels))
        output.append("\n" + "=" * 40 + "\n")
        
        # 2. Proceso Paso a Paso
        output.append("=== PROCESO PASO A PASO (Cálculo Secuencial Fila por Fila) ===")
        output.append(steps)
        # El 'steps' ya incluye la matriz final ordenada,
        # pero la pondremos de nuevo por claridad.
        
        # 3. Matriz de Caminos (Ordenada)
        output.append("=== MATRIZ DE CAMINOS (FILAS Y COLUMNAS ORDENADAS) ===")
        output.append(self.format_matrix_string(sorted_path_matrix, sorted_labels, sorted_labels))
        output.append("\n" + "=" * 40 + "\n")

        # 4. Resultados Finales (Componentes)
        output.append("=== RESULTADOS FINALES ===")
        output.append(f"Número total de componentes conexas: {len(components)}")
        output.append("\nLista de nodos por componente:")
        
        if not components:
            output.append("  (No se encontraron componentes)")
        else:
            for i, component in enumerate(components):
                output.append(f"  Componente {i+1}: {component}")

        final_text = "\n".join(output)
        txt_area.insert(tk.INSERT, final_text)
        txt_area.config(state=tk.DISABLED)

        draw_button = tk.Button(result_window, 
                                text="Mostrar Visualización del Grafo", 
                                command=lambda: self.draw_graph_safe(self.graph))
        draw_button.pack(padx=10, pady=(5, 10))
        
        result_window.protocol("WM_DELETE_WINDOW", self.on_close_results)
        result_window.lift()
        result_window.attributes('-topmost', True)
        result_window.after(100, lambda: result_window.attributes('-topmost', False))


    def draw_graph_safe(self, g):
        """Dibuja el grafo DIRIGIDO usando letras y flechas."""
        if g.number_of_nodes() == 0:
            messagebox.showwarning("Grafo Vacío", "No se puede dibujar un grafo sin nodos.")
            return

        plt.figure("Visualización del Grafo")
        
        pos = None
        try:
            pos = nx.kamada_kawai_layout(g)
        except Exception:
            pos = nx.spring_layout(g, k=0.5, iterations=50)

        # Crear el diccionario de etiquetas (0: 'A', 1: 'B', ...)
        label_mapping = {i: self.labels[i] for i in range(self.n_nodes)}

        # nx.draw detecta que 'g' es un DiGraph y dibuja flechas
        nx.draw(g, pos, labels=label_mapping, with_labels=True, node_color='lightblue', 
                edge_color='gray', node_size=700, font_weight='bold', 
                arrows=True, arrowstyle='->', arrowsize=15)
                
        plt.title("Grafo Generado")
        plt.show()

# --- Ejecución Principal ---

if __name__ == "__main__":
    app = GraphComponentsApp()
    app.run()
    print("Programa finalizado.")