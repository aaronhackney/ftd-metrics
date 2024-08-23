from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.exceptions import InfluxDBError


# TODO: implement logging
def build_influx_data(metric_api_data: list) -> list[Point]:
    """Convert the CDO API json resulkts into influxdb line objects"""
    metrics = list()
    for metric_name, metric_value in metric_api_data.items():
        if isinstance(metric_value, dict) and metric_name != "interfaceHealthMetrics":
            metric_dict = {
                "measurement": metric_name,
                "tags": {"deviceName": metric_api_data["deviceName"], "deviceUid": metric_api_data["deviceUid"]},
                "fields": metric_value,
            }
            metrics.append(Point.from_dict(metric_dict))
        elif metric_name == "interfaceHealthMetrics":
            if_metrics = build_interface_data(metric_value, metric_api_data["deviceName"], metric_api_data["deviceUid"])
    return metrics + if_metrics


def build_interface_data(if_api_data: list, device_name: str, device_id: str):
    metrics = list()
    for if_data in if_api_data:
        metric_dict = {
            "measurement": "interfaceHealthMetrics",
            "tags": {"deviceName": device_name, "deviceUid": device_id, "ifname": if_data["interface"]},
            "fields": {
                "status": if_data.get("status"),
                "bufferUnderrunsAvg": if_data.get("bufferUnderrunsAvg"),
                "bufferOverrunsAvg": if_data.get("bufferOverrunsAvg"),
                "interface": if_data.get(""),
                "interfaceName": if_data.get("interfaceName"),
            },
        }
        metrics.append(Point.from_dict(metric_dict))
    return metrics


def write_influx_metrics(
    influx_url: str, influx_token: str, influx_org: str, bucket: str, metrics: list[Point]
) -> None:
    """Given a list of influxdb line point objects, write them to the given influx instance and bucket"""
    with InfluxDBClient(url=influx_url, token=influx_token, org=influx_org) as client:
        with client.write_api(write_options=SYNCHRONOUS) as writer:
            try:
                writer.write(bucket=bucket, record=metrics)
            except InfluxDBError as e:
                print(e)
