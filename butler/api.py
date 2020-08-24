import requests
import json
import os

parameters = {}
headers = {
    "Zenkit-API-Key": os.getenv("ZENKIT_API_KEY"),
    "Content-Type": "application/json"
}
def get(req, parameters=None):
    p = None if parameters is None else json.dumps(parameters)
    response = requests.get(f"http://zenkit.com{req}", p, headers=headers)
    return json.loads(response.content)

def post(req, parameters=None):
    p = None if parameters is None else json.dumps(parameters)
    response = requests.post(f"http://zenkit.com{req}", p, headers=headers)
    return json.loads(response.content)

def put(req, parameters=None):
    p = None if parameters is None else json.dumps(parameters)
    response = requests.put(f"http://zenkit.com{req}", p, headers=headers)
    return json.loads(response.content)

def delete(req):
    p = None if parameters is None else json.dumps(parameters)
    response = requests.delete(f"http://zenkit.com{req}", headers=headers)
    return json.loads(response.content)

def get_collection(name):
    return next(collection
        for workspace in get("/api/v1/users/me/workspacesWithLists")
        for collection in workspace['lists']
        if collection['name'] == name)

print("Getting main collection")
collection = get_collection("Luke")
elements = get(f"/api/v1/lists/{collection['id']}/elements")
stage = next(e for e in elements if e['name'] == "Stage")
working = next(e for e in elements if e['name'] == "Working")
working_start = next(e for e in elements if e['name'] == "Working-start")
working_time = next(e for e in elements if e['name'] == "Working-time")

stage_wip = next(x for x in stage['elementData']['predefinedCategories'] if x['name'] == 'WIP')
working_wip = next(x for x in working['elementData']['predefinedCategories'] if x['name'] == 'WIP')


def get_entries():
    return post(f"/api/v1/lists/{collection['shortId']}/entries/filter/list", {'limit':999})['listEntries']

def get_stage(stage_name):
    return next(x for x in stage['elementData']['predefinedCategories'] if x['name']==stage_name)

def copy_all(from_stage, to_stage):
    entries = get_entries()
    from_entries =  [e for e in entries if any(x['id'] == from_stage['id'] for x in e[f"{stage['uuid']}_categories_sort"])]
    print(f"copying {len(from_entries)} entries")
    for i,e in enumerate(from_entries):
        print(f"  copying {e['displayString']}")
        new = {k:v for k,v in e.items() if "-" in k or k == "checklists"}
        new[f"{stage['uuid']}_categories"] = [to_stage['id']]
        del new[f"{stage['uuid']}_categories_sort"]

        new['sortOrder'] = max(float(e['sortOrder']) for e in entries) + i
        post(f"/api/v1/lists/{collection['id']}/entries", new)

def move_all(from_stage, to_stage):
    entries = get_entries()
    from_entries = [e for e in entries if any(x['id'] == from_stage['id'] for x in e[f"{stage['uuid']}_categories_sort"])]
    print(f"moving {len(from_entries)} entries")
    for e in from_entries:
        print(f"  moving {e['displayString']}")
        new = {f"{stage['uuid']}_categories": [to_stage['id']]}
        put(f"/api/v1/lists/{collection['id']}/entries/{e['id']}/elements/{stage['id']}", new)
