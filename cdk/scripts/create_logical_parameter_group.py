import os
import time

import boto3


class DBIdentifierMissing(Exception):
    """base class for new exception"""

    pass


if not (DB_IDENTIFIER := os.environ.get("DB_IDENTIFIER", None)):
    raise DBIdentifierMissing("Missing DB Identifier")

rds_client = boto3.client("rds")

db_instance = rds_client.describe_db_instances(DBInstanceIdentifier=DB_IDENTIFIER)
if len(db_instance["DBInstances"]) != 1:
    raise Exception("DB Instance not found")


db_pg_response = rds_client.create_db_parameter_group(
    DBParameterGroupFamily="postgres14",
    DBParameterGroupName="LogicalParameterGroup",
    Description="Parameter Group for RDS instance that is carrying out logical replication",
)

db_parameter_group_name = db_pg_response["DBParameterGroup"]["DBParameterGroupName"]

modify_response = rds_client.modify_db_parameter_group(
    DBParameterGroupName=db_parameter_group_name,
    Parameters=[
        {
            "ParameterName": "max_replication_slots",
            "ParameterValue": "100",
            "ApplyMethod": "pending-reboot",
        },
        {
            "ParameterName": "max_slot_wal_keep_size",
            "ParameterValue": "5000",
            "ApplyMethod": "immediate",
        },
        {
            "ParameterName": "max_wal_size",
            "ParameterValue": "1028",
            "ApplyMethod": "immediate",
        },
        {
            "ParameterName": "rds.logical_replication",
            "ParameterValue": "1",
            "ApplyMethod": "pending-reboot",
        },
        {
            "ParameterName": "shared_preload_libraries",
            "ParameterValue": "pglogical",
            "ApplyMethod": "pending-reboot",
        },
    ],
)

# 5 mins sleep becasue the docs say so
time.sleep(300)

rds_client.modify_db_instance(
    DBInstanceIdentifier=DB_IDENTIFIER, DBParameterGroupName=db_parameter_group_name
)

time.sleep(300)


rds_client.reboot_db_instance(DBInstanceIdentifier=DB_IDENTIFIER)
