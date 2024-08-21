from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.exceptions import InfluxDBError


# TODO: implement logging
def build_influx_data(metric_api_data: list) -> list[Point]:
    """Concvert the CDO API json resulkts into influxdb line objects"""
    metrics = list()
    for metric_name, metric_value in metric_api_data.items():
        if isinstance(metric_value, dict):
            metric_dict = {
                "measurement": metric_name,
                "tags": {"deviceName": metric_api_data["deviceName"], "deviceUid": metric_api_data["deviceUid"]},
                "fields": metric_value,
            }
            metrics.append(Point.from_dict(metric_dict))
    return metrics


def write_influx_metrics(
    influx_url: str, influx_token: str, influx_org: str, bucket: str, metrics: list[Point]
) -> None:
    """Given a list of influxdb line point objects, write them to the given influx instance and bucket"""
    with InfluxDBClient(url=influx_url, token=influx_token, org=influx_org) as client:
        with client.write_api(write_options=SYNCHRONOUS) as writer:
            for point in metrics:
                try:
                    writer.write(bucket=bucket, record=[point])
                except InfluxDBError as e:
                    print(e)
