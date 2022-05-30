import hazelcast
import time
def writer():
    print('writing...')
    client = hazelcast.HazelcastClient(cluster_name="hw2",
                                           cluster_members=[
                                               "127.0.0.1:5701",
                                           ])
    queue = client.get_queue('bounded_queue').blocking()

    for id in range(1000):
        queue.put(f"{id}_value")
        if queue.remaining_capacity() == 0:
            print('no place left')
            time.sleep(3)
    queue.put('poison_pill')
    print('ended writing')

    client.shutdown()

if __name__ == '__main__':

    print('running')
    writer()
