# taxi-demo-cli

This Demo will demonstrate how to use MLRun CLI to create a project, build ML functions (jobs, serving and nuclio) and run workflows piplines.

#### Setting remote envirobale:
* You can find more inforamtion on this [documentation link](https://docs.mlrun.org/en/latest/howto/remote.html?highlight=working%20from%20remote)
* Important - define MLRUN_ARTIFACT_PATH with v3io path:
 * With this setting your artifcats will save in v3io path and can expose and used by athoer functions, if you dont use it you will have to apply auto_mount in your code or when you run a function.
  
 Example:
 ````
 MLRUN_ARTIFACT_PATH=v3io:///projects/{{run.project}}/artifacts
 ````

# Build a project:

#### Using GitHub:
* For working with secrets for privete repositories you need to define two environment variables, Example:
````
 export git_user=User
````
````
 export git_password= GitToken
 
````
* Create a project and sync it to db - You have to have at list one function in your YAML file to create a project from a YAML file, and when the project will create all functions will build automateclly in the project.
  * -n - Define the name of the project , it overwrithe the name that writen in the YAML file.
  * -u = Define the url to your fit repository, can use to direct to a local project YAML file.
  * ./project - The name of the directory that will contain all the clone files.
  * --sync - Use to sync the project.yaml to system db, if you would not write it you would not see the project until you run a function or a workflow.

````
mlrun project -n gitproject -u "git://github.com/GiladShapira94/taxi-demo-cli.git" ./project --sync
````
#### Using Local Yaml file:

* Create a project and sync it to db:
 * -u = Define the url to your fit repository, can use to direct to a local project YAML file.
 * . - specify the context folder 
 * --sync - Use to sync the project.yaml to system db, if you would not write it you would not see the project until you run a function or a workflow.
````
mlrun project -u project.yaml . --sync
````
# Build a ML Function:
*
# Run a ML Function:
#### Run with remote inputs:
````
mlrun run -i taxi_records_csv_path=https://s3.wasabisys.com/iguazio/data/Taxi/yellow_tripdata_2019-01_subset.csv -i zones_csv_path=https://s3.wasabisys.com/iguazio/data/Taxi/taxi_zones.csv  --project gitproject -f db://gitproject/taxi --handler fetch_data --auto-mount
````
#### Run with local inputs:
````
mlrun run -f db://cli-test/taxi-func --name transation --handler transform_dataset --project gitproject -i zones_csv_path=/User/artifacts/gitproject/data/zones-dataset.csv -i taxi_records_csv_path=/User/artifacts/gitproject/data/nyc-taxi-dataset.csv
````
# Deploy serving and nuclio functions:

* For creating serving or nuclio function, you can see examples to yaml files in the git repository
 * Need to convert your code text to Base64 - Tip using this [link](https://md5decrypt.net/en/Conversion-tools) and choose the Text to Base64 options
 * Important you need to add to your code this lines befor you deploy serving functions :
 ````
 from mlrun.runtimes import nuclio_init_hook
 def init_context(context):
     nuclio_init_hook(context, globals(), 'serving_v2')

 def handler(context, event):
     return context.mlrun_handler(context, event)
 ````
 * For deploy nuclio function:
````
mlrun deploy -f nucliofunc.yaml -p gitproject
````
 * For deploy serving function:
````
 mlrun deploy -f serving.yaml -p gitproject
````

# Run a project workflow:
  * -r - The name of the workflow file - For example this file need to be located in project direcory (/project/workflow.py)
  * -w - watch option equal to true, works only on kfp engine

````
mlrun project -n gitproject -r workflow.py -w ./project
````

