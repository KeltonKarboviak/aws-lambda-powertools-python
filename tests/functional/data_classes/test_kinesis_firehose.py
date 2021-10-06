import base64
import json

from aws_lambda_powertools.utilities.data_classes import KinesisFirehoseEvent
from tests.functional.utils import load_event


def test_kinesis_firehose_event():
    event = KinesisFirehoseEvent(load_event("kinesisFirehoseEvent.json"))

    assert event.invocation_id == "invoked123"
    assert event.delivery_stream_arn == "aws:lambda:events"
    assert event.region == "us-west-2"

    records = list(event.records)
    assert len(records) == 2
    record = records[0]

    assert record.data == event["records"][0]["data"]
    assert record.record_id == "record1"
    assert record.approximate_arrival_timestamp == 1510772160000

    kinesis_record_metadata = record.kinesis_record_metadata
    assert kinesis_record_metadata._data["kinesisRecordMetadata"] == event["records"][0]["kinesisRecordMetadata"]

    assert kinesis_record_metadata.shard_id == "shardId-000000000000"
    assert kinesis_record_metadata.partition_key == "4d1ad2b9-24f8-4b9d-a088-76e9947c317a"
    assert kinesis_record_metadata.approximate_arrival_timestamp == "2012-04-23T18:25:43.511Z"
    assert kinesis_record_metadata.sequence_number == "49546986683135544286507457936321625675700192471156785154"
    assert kinesis_record_metadata.subsequence_number == ""

    assert record.data_as_bytes() == b"Hello World"
    assert record.data_as_text() == "Hello World"


def test_kinesis_firehose_event_json_data():
    json_value = {"test": "value"}
    data = base64.b64encode(bytes(json.dumps(json_value), "utf-8")).decode("utf-8")
    event = KinesisFirehoseEvent({"records": [{"data": data}]})
    assert next(event.records).data_as_json() == json_value
