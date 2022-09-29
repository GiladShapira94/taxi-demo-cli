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
    name="Testing Conditions",
    description="Testing Conditions"
)

def kfpipeline():
    
    serving = funcs['add-2'].as_step()
