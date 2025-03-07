from airflow.decorators import dag, task
from datetime import datetime

from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from astro import sql as aql
from astro.files import File
from astro.sql.table import Table, Metadata
from astro.constants import FileType
from include.dbt.cosmos_config import DBT_PROJECT_CONFIG, DBT_CONFIG
from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.constants import LoadMode
from cosmos.config import ProjectConfig, RenderConfig

@dag(
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=['steam_reviews'],
)
def steam_reviews():

    upload_steamreviews_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_steamreviews_to_gcs',
        src='include/dataset/steam_reviews.csv',
        dst='raw/steam_reviews.csv',
        bucket='amirhamzah_bucket',
        gcp_conn_id='gcp',
        mime_type='text/csv',
    )

    upload_steamappdetails_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_steamappdetails_to_gcs',
        src='include/dataset/steamappdetails.csv',
        dst='raw/steamappdetails.csv',
        bucket='amirhamzah_bucket',
        gcp_conn_id='gcp',
        mime_type='text/csv',
    )

    create_steam_reviews_dataset = BigQueryCreateEmptyDatasetOperator(
            task_id='create_steam_reviews_dataset',
            dataset_id='steam_reviews',
            gcp_conn_id='gcp',
        )

    gcs_steamreviews_to_raw = aql.load_file(
            task_id='gcs_steamreviews_to_raw',
            input_file=File(
                'gs://amirhamzah_bucket/raw/steam_reviews.csv',
                conn_id='gcp',
                filetype=FileType.CSV,
            ),
            output_table=Table(
                name='raw_steam_reviews',
                conn_id='gcp',
                metadata=Metadata(schema='steam_reviews')
            ),
            use_native_support=False,
        )
    
    gcs_steamappdetails_to_raw = aql.load_file(
            task_id='gcs_steamappdetails_to_raw',
            input_file=File(
                'gs://amirhamzah_bucket/raw/steamappdetails.csv',
                conn_id='gcp',
                filetype=FileType.CSV,
            ),
            output_table=Table(
                name='raw_steamappdetails',
                conn_id='gcp',
                metadata=Metadata(schema='steamappdetails')
            ),
            use_native_support=False,
        )
    
    transform = DbtTaskGroup(
            group_id='transform',
            project_config=DBT_PROJECT_CONFIG,
            profile_config=DBT_CONFIG,
            render_config=RenderConfig(
                load_method=LoadMode.DBT_LS,
                select=['path:models/transform']
            )
        )
    
    @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_transform(scan_name='check_transform', checks_subpath='transform'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)

    check_transform()

steam_reviews()