import sys
import os
import csv
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def generate_graph(filename):
    df = pd.read_csv( 'results_little/links_fav_little.csv' )
    Graphtype = nx.Graph()
    G = nx.from_pandas_edgelist( df, source='user1', target='user2', edge_attr='num_interactions', create_using=Graphtype)
    #nx.draw( G )
    nx.draw_random(G)
    plt.show()


if __name__ == '__main__':

    #[ 'user_id', 'user_name', 'num_fav', 'bot_prob' ]

    #cmap=plt.cm.RdBu
    cmap=plt.cm.seismic

    G = nx.DiGraph()
    nodes = pd.read_csv( 'results_little/processed_users_fav_little.csv' )
    nodes_size = []
    nodes_color = []
    for i in range( 0, len( nodes ) ):
        nodes_size += [ nodes['num_fav'][i]*100 ]
        nodes_color += [ cmap( nodes['bot_prob'][i] ) ]
        G.add_node( nodes['user_id'][i], size=nodes['num_fav'][i]*100 )
    

    edges = pd.read_csv( 'results_little/links_fav_little.csv' )
    for i in range( 0, len( edges ) ):
        attributes = edges['num_interactions'][i]
        G.add_edge( edges['user1'][i], edges['user2'][i] )

    nx.draw(G, node_size=nodes_size, node_color=nodes_color, cmap=plt.cm.RdBu )
    plt.show()

    # Wait for 5 seconds
    #time.sleep(5)
    
    exit(0)