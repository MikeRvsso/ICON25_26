import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns
import pandas as pd
import numpy as np

# Set style for academic/thesis look
sns.set_theme(style="whitegrid") # Clean background with grid
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 12,
    'figure.titlesize': 14,
    'figure.dpi': 300,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11
})

def generate_dag():
    """
    1. "bn_dag.png": Un grafo orientato (DAG) che mostri la topologia della rete.
    """
    print("Generating bn_dag.png...")
    G = nx.DiGraph()
    
    nodes = ["Meteo", "Traffico", "Esperienza Autista", "Status Consegna"]
    edges = [
        ("Meteo", "Traffico"),
        ("Meteo", "Status Consegna"),
        ("Traffico", "Status Consegna"),
        ("Esperienza Autista", "Status Consegna")
    ]
    
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    
    plt.figure(figsize=(10, 7))
    
    # Custom layout to look nice and hierarchical
    # Top level: Meteo, Esperienza Autista
    # Middle: Traffico
    # Bottom: Status Consegna
    pos = {
        "Meteo": (-1, 2),
        "Esperienza Autista": (1, 2),
        "Traffico": (-0.5, 1),
        "Status Consegna": (0.5, 0)
    }
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, 
                           node_color='skyblue', 
                           node_size=4000, 
                           edgecolors='#2c3e50', # Dark blue/gray border
                           linewidths=2, 
                           alpha=0.95)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, 
                           edge_color='gray', 
                           width=2.5, 
                           arrowsize=25, 
                           arrowstyle='-|>', 
                           connectionstyle="arc3,rad=0.1")
    
    # Draw labels
    # Break long labels for better fit
    labels = {n: n.replace(" ", "\n") for n in nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=11, font_weight='bold', font_color='#2c3e50')
    
    plt.title("Struttura Rete Bayesiana (DAG)", pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('bn_dag.png', bbox_inches='tight', dpi=300)
    plt.close()

def generate_scenarios():
    """
    2. "bn_scenarios.png": Un grafico a barre verticale per confrontare due scenari.
    """
    print("Generating bn_scenarios.png...")
    scenarios = ['Scenario A\n(Pessimistico)', 'Scenario B\n(Ottimistico)']
    probs = [82.7, 52.9]
    
    # Custom colors: Red for bad scenario, Green for good scenario
    colors = ['#e74c3c', '#27ae60'] 
    
    plt.figure(figsize=(8, 6))
    bars = plt.bar(scenarios, probs, color=colors, width=0.5, edgecolor='black', linewidth=1, alpha=0.9)
    
    plt.ylabel('Probabilità di Ritardo (%)', fontweight='bold')
    plt.title('Confronto Scenari: Rischio Predittivo (Ritardo)', fontweight='bold', pad=15)
    plt.ylim(0, 100)
    
    # Add labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 2,
                 f'{height}%',
                 ha='center', va='bottom', fontsize=13, fontweight='bold', color='#333333')
                 
    # Add a horizontal grid for readability
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    
    # Remove top and right spines for a cleaner academic look
    sns.despine(left=True, bottom=False)
    
    plt.tight_layout()
    plt.savefig('bn_scenarios.png', bbox_inches='tight', dpi=300)
    plt.close()

def generate_diagnosis():
    """
    3. "bn_diagnosis.png": Un grafico a barre orizzontali per la diagnosi delle cause.
    """
    print("Generating bn_diagnosis.png...")
    data = {
        'Causa': ['Traffic Jam', 'Traffic Low', 'Traffic Medium', 'Traffic High'],
        'Probabilità': [35.9, 27.1, 26.3, 10.7] # Data from user
    }
    
    df = pd.DataFrame(data)
    # Sort for the bar chart (usually best largest on top for horizontal bars)
    df = df.sort_values('Probabilità', ascending=False)
    
    plt.figure(figsize=(10, 5))
    
    # Horizontal bar plot with seaborn palette
    ax = sns.barplot(x='Probabilità', y='Causa', data=df, 
                     palette="Blues_r", # Reverse Blues so darkest is highest prob
                     hue='Causa', legend=False,
                     edgecolor='black', linewidth=1)
    
    plt.title("Probabilità Cause Ritardo (Dato: Ritardo + Autista Esperto)", fontweight='bold', pad=15)
    plt.xlabel('Probabilità A Posteriori (%)', fontweight='bold')
    plt.ylabel('Stato Traffico (Variabile Latente)', fontweight='bold')
    
    # Add percentage labels at the end of the bars
    for i, p in enumerate(ax.patches):
        width = p.get_width()
        plt.text(width + 0.5, p.get_y() + p.get_height()/2,
                 f'{width:.1f}%', 
                 ha='left', va='center', fontsize=12, fontweight='bold', color='#2c3e50')
                 
    plt.xlim(0, 45) # Extend x-axis to fit labels
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    sns.despine(left=True, bottom=True)
    
    plt.tight_layout()
    plt.savefig('bn_diagnosis.png', bbox_inches='tight', dpi=300)
    plt.close()

if __name__ == "__main__":
    generate_dag()
    generate_scenarios()
    generate_diagnosis()
    print("Tutti i grafici sono stati generati con successo.")
