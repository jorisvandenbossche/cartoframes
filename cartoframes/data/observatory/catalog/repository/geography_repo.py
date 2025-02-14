from __future__ import absolute_import

import geopandas as gpd

from cartoframes.data import Dataset
from cartoframes.auth import Credentials

from .constants import COUNTRY_FILTER, CATEGORY_FILTER
from .entity_repo import EntityRepository


_GEOGRAPHY_ID_FIELD = 'id'
_GEOGRAPHY_SLUG_FIELD = 'slug'
_ALLOWED_FILTERS = [COUNTRY_FILTER, CATEGORY_FILTER]

_DO_CREDENTIALS = Credentials('do-metadata', 'default_public')


def get_geography_repo():
    return _REPO


class GeographyRepository(EntityRepository):

    def __init__(self):
        super(GeographyRepository, self).__init__(_GEOGRAPHY_ID_FIELD, _ALLOWED_FILTERS, _GEOGRAPHY_SLUG_FIELD)

    def get_all(self, filters=None, credentials=None):
        self.client.set_user_credentials(credentials)
        response = self._get_filtered_entities(filters)
        self.client.set_user_credentials(None)
        return response

    @classmethod
    def _get_entity_class(cls):
        from cartoframes.data.observatory.catalog.geography import Geography
        return Geography

    def _get_rows(self, filters=None):
        if filters is not None and (COUNTRY_FILTER in filters.keys() or CATEGORY_FILTER in filters.keys()):
            return self.client.get_geographies_joined_datasets(filters)

        return self.client.get_geographies(filters)

    def _map_row(self, row):
        return {
            'id': self._normalize_field(row, self.id_field),
            'slug': self._normalize_field(row, 'slug'),
            'name': self._normalize_field(row, 'name'),
            'description': self._normalize_field(row, 'description'),
            'provider_id': self._normalize_field(row, 'provider_id'),
            'country_id': self._normalize_field(row, 'country_id'),
            'lang': self._normalize_field(row, 'lang'),
            'geom_coverage': self._normalize_field(row, 'geom_coverage'),
            'update_frequency': self._normalize_field(row, 'update_frequency'),
            'version': self._normalize_field(row, 'version'),
            'is_public_data': self._normalize_field(row, 'is_public_data'),
            'summary_json': self._normalize_field(row, 'summary_json')
        }

    def get_geographies_gdf(self):
        query = 'select id, geom_coverage as the_geom from geographies_public where geom_coverage is not null'
        df = Dataset(query, credentials=_DO_CREDENTIALS).download(decode_geom=True)

        return gpd.GeoDataFrame(df, geometry='geometry')


_REPO = GeographyRepository()
