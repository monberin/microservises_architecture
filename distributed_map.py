import hazelcast
import logging

logging.basicConfig(level=logging.INFO)


def main():
    client = hazelcast.HazelcastClient(cluster_name="hw2",
                                       cluster_members=[
                                           "127.0.0.1:5701",
                                           "127.0.0.1:5701",
                                           "127.0.0.1:5701",
                                       ])

    hz_map = client.get_map("distributed_map").blocking()

    for id in range(1000):
        hz_map.set(id, f"{id}_value")
    client.shutdown()


if __name__ == '__main__':
    main()
