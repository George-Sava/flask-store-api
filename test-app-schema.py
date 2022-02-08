from flask import json
from run import api


print(json.dumps(api.__schema__))
