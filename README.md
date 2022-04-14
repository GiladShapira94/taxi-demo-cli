# taxi-demo-cli

This Demo will demonstrate how to use MLRun CLI to create a project, build ML functions (jobs, serving and nuclio) and run workflows piplines.

# Build a project using GitHub:

* For working with secrets for privete repositories you need to define two environment variables, Example:
````
 export git_user=User
````
````
 export git_password= GitToken
 
````
* Create a project and sync it to db - 
  * -n - Define the name of the project , it overwrithe the name that writen in the YAML file.
  * -u = Define the url to your fit repository, can use to direct to a local project YAML file.
  * ./project - The name of the directory that will contain all the clone files.
  * --sync - Use to sync the project.yaml to system db, if you would not write it you would not see the project until you run a function or a workflow.

````
mlrun project -n gitproject -u "git://github.com/GiladShapira94/taxi-demo-cli.git" ./project --sync
````
* Create serving or nuclio function, you can see examples to yaml files in the git repository
 * Need to convert your code text to Base64 - Tip using this [link](https://md5decrypt.net/en/Conversion-tools) and choose the Text to Base64 options
````
mlrun deploy -s model-serving.py -f nucliofunc.yaml -p taxi-cli
````
````
 mlrun deploy -f serving.yaml -p taxi-cli 
````
* Run a ML Function:
````
mlrun run -i taxi_records_csv_path=https://s3.wasabisys.com/iguazio/data/Taxi/yellow_tripdata_2019-01_subset.csv -i zones_csv_path=https://s3.wasabisys.com/iguazio/data/Taxi/taxi_zones.csv  --project cli-test -f db://cli-test/taxi --handler fetch_data --auto-mount
````
````
mlrun run -f db://cli-test/taxi-func --name transation --handler transform_dataset --project cli-test -i zones_csv_path=/User/artifacts/cli-test/data/zones-dataset.csv -i taxi_records_csv_path=/User/artifacts/cli-test/data/nyc-taxi-dataset.csv
````
* Run a project workflow - 
  * -r - The name of the workflow file
  * -w - watch option equal to true, works only on kfp engine

````
mlrun project -n gitproject -r workflow.py -w ./project
````

# Build a project from local YAML files:
