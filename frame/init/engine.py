from frame.init.get_mapping import init_mapping
from frame.init.init_filter import init_filter_dict
from frame.init.init_server import init_server

def init(config):
    _post_mapping,_get_mapping=init_mapping(config)
    init_filter_dict(config,_get_mapping,_post_mapping)
    init_server(config)