from cartoframes.viz import Layer, Legend, Popup, Source, Style
from cartoframes.lib.context.api_context import APIContext
from cartoframes.auth import Credentials


def setup_mocks(mocker):
    mocker.patch.object(Source, 'get_geom_type', return_value='point')
    mocker.patch.object(Source, '_compute_query_bounds')
    mocker.patch.object(APIContext, 'get_schema', return_value='public')


class TestLayer(object):
    def test_is_layer_defined(self):
        """Layer"""
        assert Layer is not None

    def test_initialization_objects(self, mocker):
        """Layer should initialize layer attributes"""
        setup_mocks(mocker)
        layer = Layer(Source('layer_source', credentials=Credentials('fakeuser')))

        assert layer.is_basemap is False
        assert layer.source_data == 'SELECT * FROM "public"."layer_source"'
        assert isinstance(layer.source, Source)
        assert isinstance(layer.style, Style)
        assert isinstance(layer.popup, Popup)
        assert isinstance(layer.legend, Legend)
        assert layer.interactivity == []

    def test_initialization_simple(self, mocker):
        """Layer should initialize layer attributes"""
        setup_mocks(mocker)
        layer = Layer('layer_source', '', credentials=Credentials('fakeuser'))

        assert layer.is_basemap is False
        assert layer.source_data == 'SELECT * FROM "public"."layer_source"'
        assert isinstance(layer.source, Source)
        assert isinstance(layer.style, Style)
        assert isinstance(layer.popup, Popup)
        assert isinstance(layer.legend, Legend)
        assert layer.interactivity == []


class TestLayerStyle(object):

    def test_style_dict(self, mocker):
        """Layer style should set the style when it is a dict"""
        setup_mocks(mocker)
        layer = Layer(
            'layer_source',
            {
                'vars': {
                    'grad': '[red, green, blue]'
                },
                'color': 'blue',
                'width': 10,
                'strokeColor': 'black',
                'strokeWidth': 1
            },
            credentials=Credentials('fakeuser')
        )

        assert isinstance(layer.style, Style)
        assert '@grad: [red, green, blue]' in layer.viz
        assert 'color: blue' in layer.viz
        assert 'width: 10' in layer.viz
        assert 'strokeColor: black' in layer.viz
        assert 'strokeWidth: 1' in layer.viz

    def test_style_str(self, mocker):
        """Layer style should set the style when it is a dict"""
        setup_mocks(mocker)
        layer = Layer(
            'layer_source',
            """
                @grad: [red, green, blue]
                color: blue
                width: 10
                strokeColor: black
                strokeWidth: 1
            """,
            credentials=Credentials('fakeuser')
        )

        assert isinstance(layer.style, Style)
        assert '@grad: [red, green, blue]' in layer.viz
        assert 'color: blue' in layer.viz
        assert 'width: 10' in layer.viz
        assert 'strokeColor: black' in layer.viz
        assert 'strokeWidth: 1' in layer.viz
