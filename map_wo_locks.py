import hazelcast
import time

def racy_update_member():
    client = hazelcast.HazelcastClient(cluster_name="hw2",
                                       cluster_members=[
                                           "127.0.0.1:5701",
                                           "127.0.0.1:5701",
                                           "127.0.0.1:5701",
                                       ])
    hz_map = client.get_map("distributed_map").blocking()
    key = '1'
    value = 0
    hz_map.put(key, value)
    print('starting...')
    start = time.time()
    for id in range(1000):
        if id % 100 == 0:
            print(f'at {id}')
        value = hz_map.get(key)
        time.sleep(0.01)
        value += 1
        hz_map.set(key, value)
    print(f'time taken: {time.time() - start}')
    print(f'result: {hz_map.get(key)}')
    client.shutdown()

if __name__ == '__main__':
    racy_update_member()