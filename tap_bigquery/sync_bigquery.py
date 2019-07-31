import json
import datetime
import dateutil.parser

from google.cloud import bigquery


APPLICATION_NAME = 'Singer BigQuery Target'

# export GOOGLE_APPLICATION_CREDENTIALS=''


def do_discover(stream, limit=100):
    client = bigquery.Client()
    keys = {"table": stream["table"],
            "columns": ".".join(stream["columns"]),
            "limit": limit}
    query = """SELECT {columns} FROM {table} limit {limit}""".format(**keys)
    query_job = client.query(query)
    results = query_job.result()  # Waits for job to complete.

    properties = {}
    for row in results:
        for key in row.keys():
            if key not in properties.keys():
                properties[key] = {}
                properties[key]["type"] = ["null", "string"]
                properties[key]["inclusion"] = "automatic"
            if properties[key]["type"][1] == "float" or "properties" in properties[key].keys():
                continue
            if type(row[key]) == datetime.date:
                properties[key]["format"] = "date-time"
                continue
            if properties[key]["type"][1] == "string":
                try:
                    int(row)
                    properties[key]["type"][1] = "integer"
                except TypeError as e:
                    pass
                except ValueError as e:
                    pass
            if properties[key]["type"][1] in ("integer", "string"):
                try:
                    v = float(row[key])
                    properties[key]["type"][1] = "integer"
                    if v != int(v):
                        properties[key]["type"][1] = "number"
                except TypeError as e:
                    pass
                except ValueError as e:
                    pass

    stream_metadata = [{
        "metadata": {
            "selected": True,
            "table": stream["table"],
            "columns": stream["columns"],
            "datetime_key": stream["datetime_key"]
            # "inclusion": "available",
            # "table-key-properties": ["id"],
            # "valid-replication-keys": ["date_modified"],
            # "schema-name": "users"
            },
        "breadcrumb": []
        }]
    stream_key_properties = []
    schema = {"type": "SCHEMA",
              "stream": stream["name"],
              "key_properties":[],
              "properties": properties
              }
    return stream_metadata, stream_key_properties, schema

def do_sync(config, stream):
    client = bigquery.Client()
    metadata = stream.metadata[0]["metadata"]
    if config.get("start_datetime"):
        start_datetime = dateutil.parser.parse(config.get("start_datetime")).strftime("%Y-%m-%d %H:%M:%S")
    if config.get("end_datetime"):
        end_datetime = dateutil.parser.parse(config.get("end_datetime")).strftime("%Y-%m-%d %H:%M:%S")

    stream_dict = stream.to_dict()
    stream_dict["type"] = "SCHEMA"
    stream_dict["schema"]["type"] = "object"
    print(json.dumps(stream_dict))
    properties = stream.schema.properties

    keys = {"table": metadata["table"],
            "columns": ".".join(metadata["columns"]),
            "datetime_key": metadata.get("datetime_key"),
            "start_datetime": start_datetime,
            "end_datetime": end_datetime
            }
    query = """SELECT {columns} FROM {table} WHERE 1=1""".format(**keys)
    if keys.get("datetime_key") and keys.get("start_datetime"):
        query = query + " AND datetime '{start_datetime}' <= {datetime_key}".format(**keys)
    if keys.get("datetime_key") and keys.get("end_datetime"):
        query = query + " AND {datetime_key} < datetime '{end_datetime}'".format(**keys)
    query_job = client.query(query)

    # results = query_job.result()  # Waits for job to complete.

    for row in query_job:
    # for row in results:
        record = {}
        for key in properties.keys():
            prop = properties[key]
            if prop.format == "date-time":
                record[key] = row[key].strftime("%Y-%m-%d %H:%M:%S")
            else:
                record[key] = row[key]
        out_row = {"type": "RECORD",
                   "stream": stream.stream,
                   "schema": stream.stream,
                   "record": record}
        print(json.dumps(out_row))