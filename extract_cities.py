import datetime

import osm


assembler = osm.Assembler(
    osm_client=osm.osm_client.OverpassAPI(
        cache=osm.caches.PersistentFileCache(
            path='cache/osm/'
        )
    ),
    names_client=osm.names_client.GeonamesAPI(
        cache=osm.caches.PersistentFileCache(
            path='cache/names/'
        )
    )
)


def extract_cities():
    dao = assembler.get_city_dao()

    heap = dao.get_all_nodes()
    all = len(heap.all_nodes)

    for index, node in enumerate(heap.all_nodes):
        if index < 5386:
            continue

        done = False
        while not done:
            done = True
            try:
                yield '{:%Y-%m-%d %H:%M:%S} {} of {}. {} DONE.'.format(
                    datetime.datetime.now(),
                    index, all, float(index) / all * 100
                )
                names = dao.get_names(node.name)
                heap = dao.get_relations_by_node_id(node)

                got_by_node = True

                relations = heap.all_relations

                if relations.are_empty():
                    got_by_node = False
                    heap = dao.get_relations_by_city_name(node.name)
                    relations = heap.all_relations

                if relations.are_empty():
                    yield '{:%Y-%m-%d %H:%M:%S} Unable to find boundaries for {}'.format(
                        datetime.datetime.now(),
                        node.id
                    )
                    continue

                if not got_by_node:
                    relations = relations.filter_containing_node(node)

                    if relations.are_empty():
                        yield '{:%Y-%m-%d %H:%M:%S} No relations containing {}'.format(
                            datetime.datetime.now(),
                            node.id
                        )
                        continue

                if len(relations) == 1:
                    relation = relations.first()
                else:
                    relation = relations.get_smallest()

                if not relation:
                    yield '{:%Y-%m-%d %H:%M:%S} Relations for node {} are corrupt'.format(
                        datetime.datetime.now(),
                        node.id
                    )
                    continue

                city = osm.classes.City(
                    names,
                    node,
                    relation
                )
                yield '{:%Y-%m-%d %H:%M:%S} {}'.format(
                    datetime.datetime.now(),
                    city
                )
            except:
                done = False



for z in extract_cities():
    print z
