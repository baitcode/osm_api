from .relation import Relations, Relation
from .node import Node, Nodes
from .way import Way


class InstanceHeap(object):
    def __init__(self, elements):
        super(InstanceHeap, self).__init__()
        self.__nodes = {}
        self.__ways = {}
        self.__relations = {}

        for element in elements:
            if element['type'] == 'relation':
                relation = Relation(element, self)
                self.__relations[relation.id] = relation

            if element['type'] == 'way':
                way = Way(element, self)
                self.__ways[way.id] = way

            if element['type'] == 'node':
                node = Node(element, self)
                self.__nodes[node.id] = node

    def get_node(self, nid):
        return self.__nodes[int(nid)]

    def get_way(self, wid):
        return self.__ways[int(wid)]

    def get_relation(self, rid):
        return self.__relations[int(rid)]

    @property
    def all_relations(self):
        return Relations(self.__relations.values())

    @property
    def all_nodes(self):
        return Nodes(self.__nodes.values())
