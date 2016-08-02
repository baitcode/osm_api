from . import osm_client
from . import names_client
from . import classes
from . import caches


class Assembler(object):
    defaults = {
        'osm_client': osm_client.OverpassAPI(),
        'names_client': names_client.GeonamesAPI(),
    }

    def __init__(self, **settings):
        super(Assembler, self).__init__()
        self.settings = self.defaults
        self.settings.update(settings)

    def get_city_dao(self):
        return CityDAO(
            settings=self.settings
        )


class CityDAO(object):

    def __init__(self, settings):
        super(CityDAO, self).__init__()
        self.settings = settings

    def get_relations_by_node_id(self, node):
        """

        :type node: Node
        :rtype: InstanceHeap
        """
        client = self.settings.get('osm_client')
        data = client.as_json(
            u'node({node_id});'
            u'relation(bn);'
            u'(._;>;);'
            u''.format(node_id=node.id),
            prefix='node_id_'
        )
        return classes.InstanceHeap(data['elements'])

    def get_relations_by_city_name(self, name):
        client = self.settings.get('osm_client')
        data = client.as_json(
            u'relation["place"="city"]["name"="{name}"];'
            u'(._;>;);'
            u''.format(name=name),
            prefix='node_name_'
        )
        return classes.InstanceHeap(data['elements'])

    def get_all_nodes(self):
        client = self.settings.get('osm_client')
        data = client.as_json(
            u'node["place"="city"];',
            prefix='all_city_'
        )
        return classes.InstanceHeap(data['elements'])

    def get_names(self, name):
        client = self.settings.get('names_client')
        return client.as_json(name)
