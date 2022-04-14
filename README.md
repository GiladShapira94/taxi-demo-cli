# taxi-demo-cli

This Demo will demonstrate how to use MLRun CLI to create a project, build ML functions (jobs, serving and nuclio) and run workflows piplines.

# 1. Build a project using GitHub:

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
* 
* Run a project workflow - 
  * -r - The name of the workflow file
  * -w - watch option equal to true, works only on kfp engine

````
mlrun project -n gitproject -r workflow.py -w ./project
````
