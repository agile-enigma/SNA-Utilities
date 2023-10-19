import unittest
from src.sna_utils import *

class Test(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.read_csv('./tests/fixtures/TG_forwards_edges_list.csv')
        self.graph = create_nxgraph(self.test_data, directed=True)

    def test_mutualNeighors(self):
        neighborCount_out = len(mutual_neighbors(self.graph, 'Agdchan', 
                                                             'novaresistenciabrasil')
                               )
        neighborCount_in = len(mutual_neighbors(self.graph, 'Agdchan',
                                                            'novaresistenciabrasil',
                                                            incoming=True)
                               )
        self.assertNotEqual(neighborCount_out, neighborCount_in)

if __name__ == '__main__':
    unittest.main()
