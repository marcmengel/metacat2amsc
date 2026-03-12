from metacat.webapi import MetaCatClient
from conversion_dicts import meta2amsc_dict
from version import __version
import os
import json
import requests
import urllib

class AmSCClient:
    def __init__(self, cf):
        self.amsc_url = cf.get("general","amsc_url") 
        self.sess = requests.Session()
        self.sess.headers.update( {"Authorization": cf.get("openmetadata","jwt_token")})
        self.fqnmap = {}

    def lookup_fqn(self, namespace, name):
        did = f"{namespace}:{name}"
        if not(did in self.fqnmap):
            res = self.query(f"type=scientificWork and name={name} and extra['MetaCat.namespace']={namespace}")
            if res:
                self.fqnmap[did] = res[0]["fqn"]
            else:
                return "unknown"
        return self.fqnmap[did]:

    def query(self, querystring, limit=0, offset=0):
        url = f"{self.amsc_url}/search/catalog?q={urllib.quote_plust(querystring)}"
        if limit:
            url += f"&{limit=}"
        if offset:
            url += f"&{offset=}"
        resp = self.sess.get(url)
        return resp.json()

    def post_create(self, entity_dict):
        url = f"{self.amsc_url}/catalog/{entity_dict['type']}"
        print(f"posting {json.dumps(entity_dict, indent=4)} to {url}")
        resp = self.sess.post(url , entity_dict)
        if resp.status != 200:
             raise RuntimeError(f"got status {resp.status} for POST catalog entry")
        return resp.json()

    def put_update(self, entity_dict):
        url = f"{self.amsc_url}/catalog/{entity_dict['fqn']}"
        print(f"posting {json.dumps(entity_dict, indent=4)} to {url}")
        resp = self.sess.put(url, entity_dict)
        if resp.status != 200:
             raise RuntimeError(f"got status {resp.status} for POST catalog entry")
        return resp.json()


def field_convert(entry):
    res = {}
    extra = {
       "converter": "meta_cat2amsc",
       "converter_version": __version,
    }
    for k in entry:
        if k in meta2amsc_dict:
             if entry[k]:
                 res[meta2amsc_dict[k]] = entry[k]
        else:
             if k not in ("metadata",) and entry[k]:
                 extra[f"MetaCat.{k}"] = entry[k]

    for k in entry["metadata"]:
        if k in meta2amsc_dict:
             if entry["metadata"][k]:
                 res[meta2amsc_dict[k]] = entry["metadata"][k]
        else:
             if k not in ("metadata",) and entry["metadata"][k]:
                 extra[k] = entry["metadata"][k]

    # special conversion cases:
    if "ParentFQN" in res:
        res["ParentFQN"] = [ x["name"] for x in res["ParentFQN"] ]
    res["extra"] = extra
    return res

def convert(cf):
    print("entering convert")
    fq = cf.get("general", "file_query")
    dq = cf.get("general", "dataset_query")
    mcsu = cf.get("metacat", "server_url")
    mcasu = cf.get("metacat", "auth_server_url")
    #mcuser = cf.get("metacat", "user")

    # in development, we need an ssh tunnel to get to the AMSC API..."
    tunnel = cf.get("general", "tunnel_command")
    if tunnel:
        print(f"running: {tunnel}") 
        os.system(tunnel)

    mcc = MetaCatClient(server_url=mcsu, auth_server_url=mcasu)
    amscc = AmSCClient(cf)

    #mcc.login_token(cf.get("general", mcuser))
    
    dataset_list = mcc.query(dq, with_metadata=True, with_provenance=True)

    for d_entry in dataset_list:
        amsc_data = field_convert(d_entry)

        if not amsc_data.get("fqn",None):
            # not previously migrated
            res_data = amscc.post_create(amsc_data)

            # remember fqn, and update in metacat
            amsc_cc.fqnmap[f"{d_entry['namespace']}:{d_entry['name']}"] = res_data.get("fqn",None)

            mcc.update_dataset(
                namespace=d_entry["namespace"],
                name=d_entry["name"],
                metadata={"AmSC.common.fqn",res_data.get("fqn", "")}
            )
        else:
            # previously migrated: update
            res_data = amscc.put_update(amsc_data)

            # remember fqn
            amsc_cc.fqnmap[f"{d_entry['namespace']}:{d_entry['name']}"] = res_data.get("fqn",None)
        

    file_list = mcc.query(fq)
    for file_info in file_list:

        file_entry = mcc.get_file(name = file_info["name"], namespace = file_info["namespace"], with_datasets=True)
        amsc_data = field_convert(file_entry)

        if not amsc_data.get("fqn",None):
            # not previously migrated
            print(f"I would post {json.dumps(amsc_data,indent=4)}")
            #res_data = amscc.post_create(amsc_data)
            #mcc.update_file(
            #    namespace=d_entry["namespace"],
            #    name=d_entry["name"],
            #    metadata={"AmSC.common.fqn",res_data["fqn"]}
            #)
        else:
            # previously migrated
            res_data = amscc.put_update(amsc_data)

