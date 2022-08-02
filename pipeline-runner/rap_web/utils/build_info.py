import json


# Load build info from JSON file
def get_build_info():
    f = open('build-info.json')
    build_info_string = f.read()
    f.close()
    return json.loads(build_info_string)
