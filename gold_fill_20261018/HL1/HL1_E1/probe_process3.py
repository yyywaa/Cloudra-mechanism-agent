import json
d=json.load(open('/home/ly/Cloudra-mechanism-agent/ts/ts_0022/process.json'))
for i,rec in enumerate(d.get('stage_records') or []):
    if isinstance(rec,dict):
        keep={k:rec[k] for k in ('stage','stage_key','purpose','job_id','state','status','done','job_input_path','input_path','endpoint_side','side') if k in rec}
        print(i, json.dumps(keep)[:400])
    else:
        print(i, str(rec)[:200])
print("--- evidence_candidates")
ec=d.get('evidence_candidates')
print(json.dumps(ec)[:1200])
