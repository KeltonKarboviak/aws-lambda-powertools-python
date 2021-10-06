import base64
import json
from typing import Iterator

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper


class KinesisFirehoseRecordMetadata(DictWrapper):
    @property
    def shard_id(self) -> str:
        """Identifies which shard in the stream the data record is assigned to"""
        return self["kinesisRecordMetadata"]["shardId"]

    @property
    def partition_key(self) -> str:
        """Underlying Kinesis record partition key associated with the event"""
        return self["kinesisRecordMetadata"]["partitionKey"]

    @property
    def approximate_arrival_timestamp(self) -> str:
        """The approximate time that the record was inserted into the stream"""
        return self["kinesisRecordMetadata"]["approximateArrivalTimestamp"]

    @property
    def sequence_number(self) -> str:
        """The unique identifier of the record within its shard"""
        return self["kinesisRecordMetadata"]["sequenceNumber"]

    @property
    def subsequence_number(self) -> str:
        """The unique identifier of the subrecord in an aggregated record"""
        return self["kinesisRecordMetadata"]["subsequenceNumber"]


class KinesisFirehoseRecord(DictWrapper):
    @property
    def data(self) -> str:
        """The data blob"""
        return self["data"]

    @property
    def record_id(self) -> str:
        """A globally unique identifier for the event that was recorded in this record"""
        return self["recordId"]

    @property
    def approximate_arrival_timestamp(self) -> float:
        """The approximate time that the record was inserted into the stream"""
        return float(self["approximateArrivalTimestamp"])

    @property
    def kinesis_record_metadata(self) -> KinesisFirehoseRecordMetadata:
        """Underlying Kinesis record metadata associated with the event"""
        return KinesisFirehoseRecordMetadata(self._data)

    def data_as_bytes(self) -> bytes:
        """Decode binary encoded data as bytes"""
        return base64.b64decode(self.data)

    def data_as_text(self) -> str:
        """Decode binary encoded data as text"""
        return self.data_as_bytes().decode("utf-8")

    def data_as_json(self) -> dict:
        """Decode binary encoded data as json"""
        return json.loads(self.data_as_text())


class KinesisFirehoseEvent(DictWrapper):
    """Kinesis firehose event

    Documentation:
    --------------
    - https://docs.aws.amazon.com/lambda/latest/dg/services-kinesisfirehose.html
    """

    @property
    def invocation_id(self) -> str:
        """A globally unique identifier for the invocation of the Lambda Function"""
        return self["invocationId"]

    @property
    def delivery_stream_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the firehose delivery stream event source"""
        return self["deliveryStreamArn"]

    @property
    def region(self) -> str:
        """AWS region where the event originated eg: us-east-1"""
        return self["region"]

    @property
    def records(self) -> Iterator[KinesisFirehoseRecord]:
        for record in self["records"]:
            yield KinesisFirehoseRecord(record)
