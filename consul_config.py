import consul

c = consul.Consul()

c.kv.put('hz_cluster', 'HW3')

c.kv.put('hz_node_1', '5701')
c.kv.put('hz_node_2', '5702')
c.kv.put('hz_node_3', '5703')

c.kv.put('map', 'logging_map')
c.kv.put('queue', 'msg_queue')

# c.kv.put('msg_port_1', '9085')
# c.kv.put('msg_port_1', '9086')
#
# c.kv.put('log_port_1', '9082')
# c.kv.put('log_port_2', '9083')
# c.kv.put('log_port_3', '9084')

