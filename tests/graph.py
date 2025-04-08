import networkx as nx
import plotly.graph_objects as go
import numpy as np

# Crear un grafo simple con networkx
G = nx.erdos_renyi_graph(10, 0.3)  # Grafo aleatorio con 10 nodos y probabilidad de 0.3 de tener una arista

# Generar posiciones de los nodos en 3D usando un layout de "spring" (empuje)
pos = nx.spring_layout(G, dim=3, seed=42)  # Layout 3D con un valor de "seed" para reproducibilidad

# Extraer las coordenadas de los nodos
x_nodes = [pos[node][0] for node in G.nodes()]
y_nodes = [pos[node][1] for node in G.nodes()]
z_nodes = [pos[node][2] for node in G.nodes()]

# Extraer las coordenadas de las aristas
x_edges = []
y_edges = []
z_edges = []
for edge in G.edges():
    x_edges.append(pos[edge[0]][0])
    x_edges.append(pos[edge[1]][0])
    y_edges.append(pos[edge[0]][1])
    y_edges.append(pos[edge[1]][1])
    z_edges.append(pos[edge[0]][2])
    z_edges.append(pos[edge[1]][2])

# Crear la figura
fig = go.Figure()

# Agregar las aristas (conexiones entre nodos)
fig.add_trace(go.Scatter3d(x=x_edges, y=y_edges, z=z_edges, mode='lines', line=dict(width=2, color='black')))

# Agregar los nodos
fig.add_trace(go.Scatter3d(x=x_nodes, y=y_nodes, z=z_nodes, mode='markers+text', text=list(G.nodes()), textposition='top center', marker=dict(size=10, color='red')))

# Ajustar el layout para una visualización 3D
fig.update_layout(
    title="Grafo en 3D",
    showlegend=False,
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    )
)

# Mostrar la figura
fig.show()
