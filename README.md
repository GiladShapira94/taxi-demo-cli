# taxi-demo-cli

This demo will show you how to create a project, build ML functions (jobs, serving, and nuclio), and run workflow pipelines using the MLRun CLI.

#### Setting remote envirobale:
* More information is available at [documentation link](https://docs.mlrun.org/en/latest/howto/remote.html?highlight=working%20from%20remote)
* Important: MLRUN ARTIFACT PATH should be set to the v3io location:
 * With this setting your artifacts will be saved in the v3io path and exposed and used by other functions; if you don't, you'll have to use auto mount in your code (an example can be found in the workflow.py file) or run a function with the —auto-mount option.
  
 Example:
 ````
 MLRUN_ARTIFACT_PATH=v3io:///projects/{{run.project}}/artifacts
 ````

# Build a project:

#### Using GitHub:
* You must define two environment variables to work with secrets for clone private repositories, for example:
````
 export git_user=User
````
````
 export git_password= GitToken
 
````
* Create a project and sync it to the db - To create a project from a YAML file, you must have at least one function, and when the project is created, all functions will be built automatically.
  * -n - Define the name of the project, it overwrites the name that was written in the YAML file.
  * -u = Define the URL to your file repository, which can be use to direct to a local project YAML file.
  * ./project - The directory’s name will contain all the GitHub repository files.
  * --sync - Use to sync the project.yaml to the system DB; if you don't write it, the project won't appear in the UI until you run at least one function or workflow.

````
mlrun project -n gitproject -u "git://github.com/GiladShapira94/taxi-demo-cli.git" ./project --sync
````
#### Using Local Yaml file:

* Create a project and sync it to DB:
 * -u = Define the URL to your fit repository, which can use to direct to a local project YAML file.
 * . - specify the context folder 
 * --sync - Use to sync the project.yaml to the system DB; if you don't write it, the project won't appear in the UI until you run at least one function or workflow.
````
mlrun project -u project.yaml . --sync
````
# Build an ML Functions:
  * Build option can use only for ML function with job type.
  * -s - source file, your function code.
  * --name - define function name, overwrite the YAML file value.
  * --project - project name, if the project does not exist it will create it.
  * myfunc.yaml - you have to define a YAML file.
````
mlrun build -s test.py --name func  --project gitproject myfunc.yaml
````

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
* Deploy option can use only for ML function with nuclio or serving type.
* Examples of YAML files for creating serving or nuclio functions can be found in the git repository.
 * Before you deploy serving functions, you must add these lines to your code. :
 ````
 from mlrun.runtimes import nuclio_init_hook
 def init_context(context):
     nuclio_init_hook(context, globals(), 'serving_v2')

 def handler(context, event):
     return context.mlrun_handler(context, event)
 ````
 * Your code text must be converted to Base64 - you can use this [link](https://md5decrypt.net/en/Conversion-tools) and choose the Text to Base64 options, or you can use linux base64 command - `base64 model-serving.py`

 * For deploy nuclio function:
````
mlrun deploy -f nucliofunc.yaml -p gitproject
````
 * For deploy serving function:
````
 mlrun deploy -f serving.yaml -p gitproject
````

# Run a project workflow:
  * -r - The name of the workflow file - For example, this file needs to be located in the project directory (/project/workflow.py)
  * -w - watch option equal to true, works only on kfp engine

````
mlrun project -n gitproject -r workflow.py -w ./project
````



