import faust
import json
from datetime import datetime, timedelta
from kafka import KafkaProducer


# model for the counter, we dont care abot the rest of the message
class Frame(faust.Record, validation=True, serializer='json'):
    uid: str
    ts: datetime


# application
app = faust.App("log-frames-streamer", broker="kafka://{}".format("localhost"))

# topic definition of initial messages
frames_topic = app.topic("frames", value_type=str, value_serializer=json, partitions=None)

# topic definition that we send after consuming the first json
uid_topic = app.topic("uid", key_type=str, value_type=Frame)
# table definition with windowed aggregation
uid_counts = app.Table(
    "uid_counts", default=int, key_type=str, value_type=int
).hopping(
    step=timedelta(seconds=60), size=timedelta(seconds=60), expires=timedelta(minutes=60), key_index=True
).relative_to_field(Frame.ts)


@app.agent(frames_topic)
async def process(events: str):
    async for event in events:
        await process_event.send(
            key=event['uid'],
            value=Frame(event['uid'], datetime.fromtimestamp(event['ts']))
        )


@app.agent(uid_topic)
async def process_event(frames: faust.Stream[Frame]) -> None:
    async for frame in frames.group_by(Frame.uid):
        uid_counts[frame.uid] += 1


if __name__ == "__main__":
    app.main()
