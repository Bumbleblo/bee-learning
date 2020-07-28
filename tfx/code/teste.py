import datetime

from tfx.components import CsvExampleGen, StatisticsGen, SchemaGen, ExampleValidator, Transform, Trainer
from tfx.components.base import executor_spec
from tfx.components.trainer.executor import GenericExecutor
from tfx.orchestration import pipeline, metadata
from tfx.orchestration.airflow.airflow_dag_runner import AirflowDagRunner, AirflowPipelineConfig
from tfx.proto import trainer_pb2
from tfx.types import channel_utils
from tfx.types.standard_artifacts import ExternalArtifact


CSV_PATH='/home/data'

def create_pipe():


    instance = ExternalArtifact()
    instance.uri = str(CSV_PATH)

    channels = channel_utils.as_channel([instance])

    example_gen = CsvExampleGen(input=channels)

    statistics_gen = StatisticsGen(examples=example_gen.outputs['examples'])

    infer_schema = SchemaGen(
        statistics=statistics_gen.outputs['statistics']
    )

    example_val = ExampleValidator(
        statistics=statistics_gen.outputs['statistics'], 
        schema=infer_schema.outputs['schema']
    )

    transform = Transform(
        examples=example_gen.outputs['examples'],
        schema=infer_schema.outputs['schema'],
        module_file='/root/airflow/dags/infer.py'
    )

    trainer = Trainer(
        module_file='/root/airflow/dags/infer.py',
        custom_executor_spec=executor_spec.ExecutorClassSpec(GenericExecutor),
        transformed_examples=transform.outputs['transformed_examples'],
        schema=infer_schema.outputs['schema'],
        transform_graph=transform.outputs['transform_graph'],
        train_args=trainer_pb2.TrainArgs(num_steps=200),
        eval_args=trainer_pb2.EvalArgs(num_steps=100)
    )

    # Database config
    metadata_config = metadata.sqlite_metadata_connection_config('teste_1.db')

    pipe = pipeline.Pipeline(
            pipeline_name='teste_1',
            pipeline_root='/root/',
            components=[
                example_gen,
                statistics_gen,
                infer_schema,
                example_val,
                transform,
                trainer
            ],
            metadata_connection_config=metadata_config,
        )
 
    return pipe

_airflow_config = {
    'schedule_interval': None,
    'start_date': datetime.datetime(2020, 2, 11),
}

runner = AirflowDagRunner(AirflowPipelineConfig(_airflow_config))

DAG = runner.run(create_pipe())
