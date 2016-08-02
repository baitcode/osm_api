import pytils


class City(object):

    def __init__(self, names, node, relation):
        super(City, self).__init__()
        self.relation = relation
        self.node = node
        self.polygons = relation.outer_polygons
        self.center = node
        self.names = names
        self.population = node.population

    def __str__(self):
        return '{} - pop. {} n_id: {} r_id: {}'.format(
            self.names['en'].encode('utf-8'),
            self.population / 1000,
            self.node.id,
            self.relation.id
        )

    def serialize(self):
        template = '{}{}'


class Geo(object):

    def __init__(self, names):
        super(Geo, self).__init__()
        try:
            self.name_ru = names['ru']
        except:
            self.name_ru = ''
        self.name_en = names['en']
        self.name_translit = pytils.translit.translify(self.name_ru)


class Continent(Geo):
    def __init__(self, names):
        super(Continent, self).__init__(names)


class Country(Geo):
    def __init__(self, names, continent):
        super(Country, self).__init__(names)


class City(Geo):
    def __init__(self, names):
        super(City, self).__init__(names)


class District(Geo):
    def __init__(self, names):
        super(District, self).__init__(names)


class Polygon(object):
    def __init__(self, edges):
        self.edges = edges

