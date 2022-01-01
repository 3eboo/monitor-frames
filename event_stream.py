import faust
import json
from kafka import KafkaProducer


class Frame(faust.Record, validation=True, serializer='json'):
    uid: str
    ts: int


app = faust.App("log-frames-streamer", broker="kafka://{}".format("localhost"))
frames_topic = app.topic("frames", value_type=str, value_serializer=json, partitions=8)
uid_topic = app.topic("uid", key_type=str, value_type=Frame)
uid_counts = app.Table("uid_counts", default=int, key_type=str, value_type=int)


@app.agent(frames_topic)
async def process(events: str):
    async for event in events:
        for frame in json.loads(event):
            await process_event.send(
                key=frame['uid'],
                value=Frame(frame['uid'], frame['ts']))
        else:
            print(f'event: {event}  events:{events}')
        # frames = json.loads(events)
        # for frame in frames:



@app.agent(uid_topic)
async def process_event(frames: faust.Stream[Frame]) -> None:
    async for frame in frames.group_by(Frame.uid):
        uid_counts[frame.uid] += 1
        print(f'frame {frame.uid} has count{uid_counts[frame.uid]}')


@app.timer(60.0)
async def my_periodic_task():
    print('print counts for each uid')

if __name__ == "__main__":
    app.main()
