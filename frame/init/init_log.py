from frame.application.log import init_log_list

def init_log(config):
    '''
        初始化log
        :param config: 配置列表
        :return:
        '''
    if "log" in config:
        if "storage_address" in config["log"]:
            _storage_address = config["log"]["storage_address"]
        if "log_max_len" in config["log"]:
            _log_max_len = int(config["log"]["log_max_len"])

    init_log_list(_storage_address,_log_max_len)
