import weakref


class Node(object):
    def __init__(self, data, heap=None):
        super(Node, self).__init__()
        if heap:
            self.heap = weakref.ref(heap)
        self.data = data

    @property
    def id(self):
        return int(self.data['id'])

    @property
    def name(self, language='en'):
        return self.data.get('tags', {}).get('name', u'')

    @property
    def x(self):
        return self.data['lat']

    @property
    def y(self):
        return self.data['lon']

    @property
    def population(self):
        result = self.data['tags'].get('population', 0)
        if isinstance(result, basestring):
            result = result.replace('.', '').replace(',', '').replace(' ', '')
        return int(result)

    def __hash__(self):
        return (self.x, self.y).__hash__()

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __str__(self):
        return '( {} x:{: >5.10}, y:{: >5.10} )'.format(
            self.name.encode('utf-8'),
            self.x,
            self.y
        )


class Vector(object):
    def __init__(self, start, end):
        """

        :type start: Point
        :type end: Point
        :return:
        """
        super(Vector, self).__init__()
        self.end = end
        self.start = start

    @classmethod
    def from_point(cls, node):
        return Vector(
            Node({'lat': 0.0, 'lon': 0.0}),
            node
        )

    def intersects(self, v2):
        """

        :type v1: Vector
        :type v2: Vector
        :return:
        """
        v1 = self

        p1 = v1.start
        p2 = v1.end

        p3 = v2.start
        p4 = v2.end

        a1 = p1.x - p3.x
        b1 = p2.x - p1.x
        c1 = p4.x - p3.x

        a2 = p1.y - p3.y
        b2 = p2.y - p1.y
        c2 = p4.y - p3.y

        denominator = (b1 * c2 - b2 * c1)

        if denominator == 0:
            return None

        s = float(b1 * a2 - b2 * a1) / denominator
        t = float(a2 * c1 - a1 * c2) / denominator

        if not (1 >= s >= 0 and 1 >= t >= 0):
            return None

        return s, t

    def __str__(self):
        return "[{}, {}]".format(self.start, self.end)


class Nodes(object):
    def __init__(self, nodes):
        super(Nodes, self).__init__()
        self.nodes = nodes

    def __iter__(self):
        for node in self.nodes:
            yield node

    def __len__(self):
        return len(self.nodes)


class Polygon(Nodes):
    def has_node(self, node):
        if len(self.nodes) <= 2:
            return

        vector = Vector.from_point(node)

        intersections = 0
        for i in range(0, len(self.nodes) - 1):
            vec = Vector(self.nodes[i], self.nodes[i + 1])
            intersections += bool(vector.intersects(vec))

        vec = Vector(self.nodes[-1], self.nodes[0])
        intersections += bool(vector.intersects(vec))

        return intersections % 2 != 0
