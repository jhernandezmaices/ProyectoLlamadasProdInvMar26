import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

df = pd.read_csv('ConcentradoProdInv.csv')

edges = defaultdict(lambda: {'calls': 0, 'duration': 0})
for _, row in df.iterrows():
    key = tuple(sorted([row['ColabOrigen'], row['ColabDestino']]))
    edges[key]['calls'] += 1
    edges[key]['duration'] += row['Duracion']

G = nx.Graph()
for (src, dst), data in edges.items():
    weight = data['calls'] + (data['duration'] / 10)
    G.add_edge(src, dst, weight=data['calls'], duration=data['duration'], weighted_weight=weight)

plt.figure(figsize=(16, 12))
pos = nx.spring_layout(G, k=2.5, seed=42)

node_sizes = [G.degree(node) * 400 + 500 for node in G.nodes()]

edge_weights = [G[u][v]['weighted_weight'] * 0.8 for u, v in G.edges()]

max_weight = max(edge_weights) if edge_weights else 1
edge_colors = [plt.cm.Blues(0.3 + 0.7 * w / max_weight) for w in edge_weights]

nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=node_sizes, edgecolors='darkblue', linewidths=2)

nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')

nx.draw_networkx_edges(G, pos, width=edge_weights, edge_color=edge_colors, alpha=0.7)

labels = {(u, v): f"{G[u][v]['weight']} calls\n{G[u][v]['duration']} min" for u, v in G.edges()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=6, alpha=0.8)

plt.title('Red de Comunicación entre Colaboradores\n(Grosor de línea = Intensidad de comunicación)', fontsize=14, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.savefig('GrafoComunicacion.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("Grafo guardado como: GrafoComunicacion.png")
print(f"\nEstadísticas:")
print(f"- Total de colaboradores: {G.number_of_nodes()}")
print(f"- Total de conexiones: {G.number_of_edges()}")
print(f"- Total de llamadas: {len(df)}")

print("\nColaboradores más conectados:")
degree_dict = dict(G.degree())
for name, deg in sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"  {name}: {deg} conexiones")