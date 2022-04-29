# Module Imports
import os 
import sys
# load_var

DB_USERNAME = ""
DB_PASSWORD = ""

def load_var(env_var):
   env_data = ""
   try:
       env_data=os.environ[env_var]
       
   except:
       print("error:  env not set")
       exit(8)
   return env_data
