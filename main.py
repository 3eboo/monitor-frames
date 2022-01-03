# This is a sample Python script.

import json
import jsonlines
import sys
from kafka import KafkaProducer


def produce_stream_in_file(file_name: str = path_to_file, limit: int = None):
    '''
    :param file_name: path to jsonlines file containing the streaming data
    :param limit:(for the sake to run quick tests) number of events/messages to stream, if None all the data in file will be used.
    :return:
    '''
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    with jsonlines.open(file_name) as reader:
        counter = 0
        for object in reader:
            if counter == limit:
                break
            else:
                producer.send('frames', object)
                counter += 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    produce_stream_in_file(*sys.argv[1:])
