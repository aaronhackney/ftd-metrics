#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from influx_helpers import build_influx_data, write_influx_metrics
from cdo_helpers import create_session, get, TIME_INTERVALS
import json


def get_ftd_metrics(cdo_endpoint: str, cdo_token: str, fmc_uid: str, interval: str):
    """Call the CDO API and get the metrics for all of the FTDs managed by this cdFMC"""
    cdo_session = create_session(cdo_token)
    return get(
        cdo_session,
        cdo_endpoint,
        path=f"api/rest/v1/inventory/managers/{fmc_uid}/health/metrics",
        query={"timeRange": "5m"},
    )


def main():
    load_dotenv()
    org = os.environ.get("ORG")
    url = os.environ.get("URL")
    bucket = os.environ.get("BUCKET")
    fmc_uid = os.environ.get("FMC_UID")
    cdo_token = os.environ.get("CDO_TOKEN")
    cdo_endpoint = os.environ.get("CDO_ENDPOINT")
    influx_token = os.environ.get("INFLUXDB_TOKEN")
    time_interval = os.environ.get("TIME_INTERVAL")

    if time_interval not in TIME_INTERVALS:
        raise ValueError("Valid metric time intervals are 5m, 15m, 30m, 1h")

    # Get the API data from the cdFMC
    metric_api_data = get_ftd_metrics(cdo_endpoint, cdo_token, fmc_uid, time_interval)
    # with open("test.json") as json_data:
    #     metric_api_data = json.load(json_data)

    # Write the data to influxDB (And we will visualize with Grafana)
    for device_data in metric_api_data:
        metrics = build_influx_data(device_data)
        write_influx_metrics(url, influx_token, org, bucket, metrics)


if __name__ == "__main__":
    main()
