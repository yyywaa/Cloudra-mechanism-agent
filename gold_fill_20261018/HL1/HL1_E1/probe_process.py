import json
d=json.load(open('/home/ly/Cloudra-mechanism-agent/ts/ts_0022/process.json'))
print("top keys:", list(d.keys()))
for k in ('input','verification','steps','stages','nodes','dag','plan','progress','status','state'):
    if k in d:
        v=d[k]
        print("--",k,"type",type(v).__name__)
        s=json.dumps(v)[:1500]
        print(s)
