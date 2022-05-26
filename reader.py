import hazelcast
import time
def reader():
    print('reading...')

    client = hazelcast.HazelcastClient(cluster_name="hw2",
                                           cluster_members=[
                                               "127.0.0.1:5701",
                                               "127.0.0.1:5701",
                                               "127.0.0.1:5701",
                                           ])
    queue = client.get_queue('bounded_queue').blocking()

    while True:
        el = queue.take()
        print(f"taken {el}")
        if el == 'poison_pill':
            queue.put('poison_pill')
            break
        # time.sleep(0.1)


    client.shutdown()

if __name__ == '__main__':
    time.sleep(5)
    reader()