from kfp import dsl
from mlrun.platforms import auto_mount
import os
import sys
import mlrun

funcs = {}

# init functions is used to configure function resources and local settings
def init_functions(functions: dict, project=None, secrets=None):
    for f in functions.values():
        f.apply(auto_mount())

@dsl.pipeline(
    name="NYC Taxi Demo",
    description="Convert ML script to MLRun"
)

def kfpipeline():

    taxi_records_csv_path = mlrun.get_sample_path('data/Taxi/yellow_tripdata_2019-01_subset.csv')
    zones_csv_path = mlrun.get_sample_path('data/Taxi/taxi_zones.csv')
    
    # build our ingestion function (container image)
    builder = funcs['taxi'].deploy_step(skip_deployed=True)
    
    # run the ingestion function with the new image and params
    ingest = funcs['taxi'].as_step(
        name="fetch_data",
        handler='fetch_data',
        image=builder.outputs['image'],
        inputs={'taxi_records_csv_path': taxi_records_csv_path,
                'zones_csv_path': zones_csv_path},
        outputs=['nyc-taxi-dataset', 'zones-dataset'])

    # Join and transform the data sets 
    transform = funcs["taxi"].as_step(
        name="transform_dataset",
        handler='transform_dataset',
        inputs={"taxi_records_csv_path": ingest.outputs['nyc-taxi-dataset'],
                "zones_csv_path" : ingest.outputs['zones-dataset']},
        outputs=['nyc-taxi-dataset-transformed'])

    # Train the model
    train = funcs["taxi"].as_step(
        name="train",
        handler="train_model",
        inputs={"input_ds" : transform.outputs['nyc-taxi-dataset-transformed']},
        outputs=['FareModel'])
  #Build serving function
    serving = mlrun.code_to_function(filename=path.abspath('model-serving.ipynb'),kind = 'serving',image='mlrun/mlrun').apply(auto_mount())
    serving.spec.default_class = 'LGBMModel'
    serving.spec.build.commands = ['pip install lightgbm']
    serving.add_model('taxi-serving', train_model_run.outputs['FareModel'])
    serving_address = serving.deploy()
    deploy = funcs["model-serving"].deploy_step(models={"taxi-serving_v1": train.outputs['FareModel']}, tag='v2')
