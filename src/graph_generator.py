import sys
import os
import csv
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib


def generate_graph(filename):
    df = pd.read_csv( 'results_little/links_fav_little.csv' )
    Graphtype = nx.Graph()
    G = nx.from_pandas_edgelist( df, source='user1', target='user2', edge_attr='num_interactions', create_using=Graphtype)
    #nx.draw( G )
    nx.draw_random(G)
    plt.show()


if __name__ == '__main__':

    #[ 'user_id', 'user_name', 'num_interactions', 'bot_prob' ]

    if len(sys.argv) < 3:
        print( "ERROR: Few Arguments: [Nodes File] [Links File]." )
        exit( 1 )

    try:
        nodes = pd.read_csv( sys.argv[1] )
    except:
        print("ERROR: Nodes file doesn't exists.")
        exit(1)

    try:
        edges = pd.read_csv( sys.argv[2] )
    except:
        print("ERROR: Links file doesn't exists.")
        exit(1)

    #cmap=plt.cm.RdBu
    cmap=plt.cm.seismic

    G = nx.DiGraph()
    nodes_size = []
    nodes_color = []
    try:
        for i in range( 0, len( nodes ) ):
            nodes_size += [ nodes['num_interactions'][i]*1 ]
            nodes_color += [ cmap( nodes['bot_prob'][i] ) ]
            G.add_node( nodes['user_id'][i], size=nodes['num_interactions'][i]*1 )
    except:
        print("ERROR: Wrong format in the nodes file, line ", i)
        exit(1)

    try:
        for i in range( 0, len( edges ) ):
            attributes = edges['num_interactions'][i]
            G.add_edge( edges['user1'][i], edges['user2'][i] )
    except:
        print("ERROR: Wrong format in the links file, line ", i)
        exit(1)

    #some users re not analyzed due to their accounts have been removed or they are private so I will print these accounts as green points
    for i in range( len(nodes), G.number_of_nodes() ):
        nodes_size += [ 1 ]
        nodes_color += [ (0.0, 1.0, 0.0, 1.0 ) ]
    

    fig, ax = plt.subplots()
    nx.draw(G, node_size=nodes_size, node_color=nodes_color, cmap=plt.cm.seismic )
    
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=1))
    sm.set_array([])
    cbar = plt.colorbar(sm, fraction=0.046, pad=0.01)
    cbar.ax.set_ylabel('Probability of being a Bot',labelpad=15,rotation=270)
    plt.subplots_adjust(left=0)
    plt.show()

    # Wait for 5 seconds
    #time.sleep(5)
    exit(0)