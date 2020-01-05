import datetime
import uuid
import time
import json
import msgpack
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError

topic = 'my-topic2'

def get_consumer(topic=topic):
    return KafkaConsumer(
            topic,
            # group_id='my-group',
            # client_id=str(uuid.uuid1()),
            # fetch_max_wait_ms=1,
            # metadata_max_age_ms=10,
            auto_offset_reset='earliest',
            consumer_timeout_ms=10000,
            bootstrap_servers=['localhost:9092'],
            value_deserializer=msgpack.loads)

producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        value_serializer=msgpack.dumps)

consumer = get_consumer()


def _produce_n(n=100):
    for i in range(n):
        yield (i, time.time())

def on_send_error(excp):
    log.error("ERROR", exc_info=excp)

def on_send_success(record_metadata):
    print(f'SUCCESS: {record_metadata.topic}, {record_metadata.partition}, {record_metadata.offset}')

def produce_n(n=100):
    for value in _produce_n(n=n):
        producer.send(topic, value=value).add_callback(on_send_success).add_errback(on_send_error)
        time.sleep(0.100)

def consume(consumer=None):
    if consumer is None:
        consumer = get_consumer()
    for x in consumer:
        # print(x)
        T = time.time()
        t = x.value[1]
        dt = T - t
        x = x.value[0]
        print(f'x={x}, t={t} T={T} dt={dt} ms')
