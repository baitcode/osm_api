# coding=utf-8

import api_wrapper
import pycountry


# query = u'node["place"="city"];node["is_in:country_code"="{}"];'
# for country in pycountry.countries:
#     print country.alpha2
#     if country.alpha2 == 'KE':
#         continue
#     api_wrapper.get(query.format(country.alpha2))



# query = u'relation["uboundary"="administrative"]["admin_level"=8](55.703322379585,37.50801086425781,55.815172308302344,37.749366760253906);'
#         u'way["admin_level"=9](55.703322379585,37.50801086425781,55.815172308302344,37.749366760253906)'

# query = u'relation["boundary"="administrative"]["admin_level"=8]["addr:city"="Москва"]'
# api_wrapper.get(query)





import mysql.connector


class DB(object):

    def __init__(self):
        super(DB, self).__init__()
        config = {
          'user': 'root',
          'password': '',
          'host': '127.0.0.1',
          'database': 'geotest',
          'raise_on_warnings': True,
          'use_pure': False,
        }
        self.cnx = mysql.connector.connect(**config)

    def execute(self, query):
        cursor = self.cnx.cursor()

        try:
            cursor.execute(query)
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

        # cursor.column_names

        for element in cursor:
            yield dict(zip(cursor.column_names, element))

# for row in DB().execute('SELECT * FROM geo_instance;'):
#     print row

