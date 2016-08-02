import weakref


class Way(object):
    def __init__(self, data, heap):
        """

        :type data: dict
        :type heap: InstanceHeap
        """
        super(Way, self).__init__()
        self.heap = weakref.ref(heap)
        self.data = data

    @property
    def id(self):
        return int(self.data['id'])

    @property
    def nodes(self):
        result = []

        heap = self.heap()
        if not heap:
            return result

        for nid in self.data['nodes']:
            node = heap.get_node(nid)
            result.append(node)

        return result
