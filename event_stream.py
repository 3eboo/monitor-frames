import faust


# model for the frames
class Frame(faust.Record, serializer='json'):
    uuid: str
    ts: int


# application definition
app = faust.App('my-app', broker='kafka://localhost:9092')
# input stream
frames_kafka_topic = app.topic('frames', value_type=Frame)
# counts table definition
user_count_by_uuid = app.Table('frame_count', default=int)


@app.agent(frames_kafka_topic)
async def process(frames: faust.Stream[Frame]) -> None:
    async for frame in frames.group_by(Frame.uuid):
        user_count_by_uuid[frame.uuid] += 1


if __name__ == "__main__":
    app.main()
