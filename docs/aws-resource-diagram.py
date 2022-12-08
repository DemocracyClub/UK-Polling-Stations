from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS
from diagrams.aws.network import ALB, Route53
from diagrams.aws.storage import S3
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.framework import Django

with Diagram("AWS Resources", filename="docs/aws-resources", show=False):
    rds = RDS("RDS Primary/Write")
    lamda_trigger = Lambda("WDIVTrigger")

    with Cluster("S3"):
        pollingstations_data = S3("pollingstations_data")
        file_uploads = S3("file_uploads")
        address_data = S3("address_data")
        file_uploads >> lamda_trigger
        pollingstations_data << lamda_trigger
        rds << pollingstations_data
        rds << address_data

    alb = ALB("Application Load Balancer")

    with Cluster("Instances", direction="TB"):
        for i in range(1, 4):
            with Cluster(
                f"Instance {i}",
            ):
                alb << Django("WDIV App") >> rds
                PostgreSQL(f"Replica/Read db {i}") << rds

    dns = Route53("DNS")

    dns >> alb
