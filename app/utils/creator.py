import json

from at.io.utils import load_json
from at.web.element import Element, ElementStore
from pprint import pprint

filepath = "D:/.temp/.dev/.aztool/atparser/skroutz.config.json"

all_data = load_json(filepath)

data = all_data.pop('elements')

def element_maker(dict_data:dict):
    children = dict_data.pop('children', None)

    if children is None:
        return Element(**dict_data)
    else:
        if isinstance(children, (list, tuple)):
            _iterable = [element_maker(child_data) for child_data in children]
            return Element(**dict_data, children=_iterable)
        else:
            return Element(**dict_data, children=element_maker(children))

def element_factory(json_config_data:dict):
    if 'interaction' in json_config_data:
        interaction = json_config_data.pop('interaction')
        if 'cookies' in interaction:
            cookies = interaction.pop('cookies')
            print(Element.from_dict(cookies))
        if 'paginator' in interaction:
            paginator = interaction.pop('paginator')
            print(Element.from_dict(paginator))
    if 'data' in json_config_data:
        data_elems = json_config_data.pop('data')
        print(Element.from_dict(data_elems))

es = ElementStore.from_json_config(data)

print(es.cookies)
print(es.paginator)
print(es.data)
    
    
    