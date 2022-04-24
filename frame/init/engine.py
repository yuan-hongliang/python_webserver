from frame.init.get_mapping import init_mapping
from frame.init.init_filter import init_filter_dict
from frame.init.init_server import init_server

def init(config):
    _post_mapping,_get_mapping=init_mapping(config)
    print("包文件扫描成功")
    init_filter_dict(config,_get_mapping,_post_mapping)
    print("过滤器加载成功")
    init_server(config)
    print("请求队列初始化成功")