from time import sleep
from unittest import TestCase

from topology_manager import TopologyManager


class TestTopologyManager(TestCase):
    tm = TopologyManager()
    def test_create_topology(self):
        self.tm.create_n_node(10,'Alpine')
        self.tm.create_router()
        sleep(3)
        self.tm.clean()
