import unittest
import networkx as nx
from src.models.bfs_community_graph import BfsCommunityGraph

class TestBfsCommunityGraph(unittest.TestCase):

  def setUp(self) -> None:
    self.graph = BfsCommunityGraph()

  def test_load_graph(self):
    num_nodes = 10
    edge_prob = 0.2
    valid_g_seed = 9
    invalid_g_seed = 7

    # Should return True if the graph is valid
    G = nx.erdos_renyi_graph(num_nodes, edge_prob, valid_g_seed)
    self.assertTrue(self.graph.load_graph(G))

    # Should return False if the graph is not valid
    G = nx.erdos_renyi_graph(num_nodes, edge_prob, invalid_g_seed)
    self.assertFalse(self.graph.load_graph(G))

  def test_make_graph_from_edges(self):
    # Test graph creation from a list of edges
    edges = [("Person_1", "Person_2"), ("Person_2", "Person_3"), ("Person_3", "Person_4")]
    self.assertTrue(self.graph.make_graph_from(edges))
    self.assertEqual(len(self.graph.graph.nodes), 4)  # There should be 4 unique nodes
    self.assertEqual(len(self.graph.graph.edges), 3)  # There should be 3 edges

    # Test invalid graph (empty edge list)
    self.assertFalse(self.graph.make_graph_from([]))

  def test_graph_string_representation(self):
    # Check if the string representation includes correct information
    edges = [("Person_1", "Person_2"), ("Person_2", "Person_3")]
    self.graph.make_graph_from(edges)
    self.graph.set_start_node("Person_1")
        
    graph_str = str(self.graph)
    self.assertIn("Graph Nodes", graph_str)
    self.assertIn("Graph Edges", graph_str)
    self.assertIn("Levels", graph_str)
    self.assertIn("Spread order", graph_str)
    self.assertIn("Start node", graph_str)

  def test_random_community(self):
    # Generate a random community graph and check if it has the correct number of nodes
    num_nodes = 5
    edge_prob = 0.4
    self.assertTrue(self.graph.random_community(num_nodes, edge_prob))

    # Check if the generated graph has the specified number of nodes
    self.assertEqual(len(self.graph.graph.nodes), num_nodes)
        
    # Check if all nodes are labeled as strings (e.g., "Person_0", "Person_1", ...)
    all_labels_are_strings = all(isinstance(node, str) and node.startswith("Person_") for node in self.graph.graph.nodes)
    self.assertTrue(all_labels_are_strings)