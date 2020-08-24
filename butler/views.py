from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timezone

from . import api

import dateutil.parser

@csrf_exempt
def event(request):
    print("An event!")
    update_working()
    return HttpResponse()

def update_working():
    entries = api.get_entries()
    new_wip = [e for e in entries
            if e[f"{api.working_start['uuid']}_date"] is None
            and api.stage_wip['id'] in e[f"{api.stage['uuid']}_categories"]]

    for e in new_wip:
        print("new WIP:", e['displayString'])
        new = {f"{api.working_start['uuid']}_date": datetime.now().isoformat(),
               f"{api.working_start['uuid']}_hasTime": True}
        api.put(f"/api/v1/lists/{api.collection['id']}/entries/{e['id']}/elements/{api.working_start['id']}", new)



    old_wip = [e for e in entries
            if e[f"{api.working_start['uuid']}_date"] is not None
            and api.stage_wip['id'] not in e[f"{api.stage['uuid']}_categories"]]

    for e in old_wip:
        print("old WIP:", e['displayString'])

        old_time = e[f"{api.working_time['uuid']}_number"] or 0
        start = dateutil.parser.parse(e[f"{api.working_start['uuid']}_date"])
        new_time = old_time + (datetime.now(timezone.utc) - start).total_seconds()/60
        new = {f"{api.working_time['uuid']}_number": new_time}
        api.put(f"/api/v1/lists/{api.collection['id']}/entries/{e['id']}/elements/{api.working_time['id']}", new)

        new = {f"{api.working_start['uuid']}_date": None}
        api.put(f"/api/v1/lists/{api.collection['id']}/entries/{e['id']}/elements/{api.working_start['id']}", new)

    