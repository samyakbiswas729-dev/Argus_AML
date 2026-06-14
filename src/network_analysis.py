import networkx as nx


def build_network(df):

    graph = nx.Graph()

    for _, row in df.iterrows():

        graph.add_edge(
            row["client_country"],
            row["counterparty_country"]
        )

    return graph
