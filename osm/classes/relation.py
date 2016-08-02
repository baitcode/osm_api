import weakref
from copy import copy

from .node import Polygon


class Relation(object):
    def __init__(self, data, heap):
        super(Relation, self).__init__()
        self.heap = weakref.ref(heap)
        self.data = data

    def serialize(self):
        return '[{id}]'

    @property
    def id(self):
        return int(self.data['id'])

    @property
    def level(self):
        level = self.data.get('tags', {}).get('admin_level', None)
        return int(level) if level else None

    @property
    def outer_polygons(self):
        """

        :rtype: list<Polygon>
        :return:
        """
        result = []

        current_polygon = []

        heap = self.heap()

        if not heap:
            return result

        def get_nodes(member):
            mtype = member['type']
            mid = member['ref']

            if mtype == 'node':
                node = heap.get_node(mid)
                return [node]
            elif mtype == 'way':
                return heap.get_way(mid).nodes

            return []

        def find_position_of(node, members):
            for index, member in enumerate(members):
                mtype = member['type']

                if mtype != 'way':
                    continue

                nodes = get_nodes(member)

                if node.id == nodes[0].id:
                    return index, 1

                if node.id == nodes[-1].id:
                    return index, -1

            return -1, 1

        temp_members = [m for m in self.data.get('members', []) if m['type'] == 'way']
        while temp_members:
            if not current_polygon:
                current_polygon.extend(get_nodes(temp_members.pop(0)))
                continue

            index, order = find_position_of(current_polygon[-1], temp_members)

            if index >= 0:
                nodes = get_nodes(temp_members.pop(index))[::order]
                current_polygon.extend(nodes[1:])
            else:
                result.append(Polygon(current_polygon))
                current_polygon = []

        if current_polygon:
            result.append(Polygon(current_polygon))

        return result

    def has_node(self, node):
        for polygon in self.outer_polygons:
            if polygon.has_node(node):
                return True

        return False


class Relations(object):
    def __init__(self, relations):
        """

        :type relations: list<Relation>
        """
        super(Relations, self).__init__()
        self.relations = relations

    def get_smallest(self):

        smallest_relation = None
        for relation in self.relations:
            if relation.level is None:
                continue

            if smallest_relation is None:
                smallest_relation = relation
            elif relation.level > smallest_relation.level:
                smallest_relation = relation

        return smallest_relation

    def filter_containing_node(self, node):
        result = []

        for relation in self.relations:
            if relation.has_node(node):
                result.append(relation)

        return Relations(result)

    def __iter__(self):
        for r in self.relations:
            yield r

    def __len__(self):
        return len(self.relations)

    def are_empty(self):
        return (self.relations == [])

    def first(self):
        return self.relations[0]
