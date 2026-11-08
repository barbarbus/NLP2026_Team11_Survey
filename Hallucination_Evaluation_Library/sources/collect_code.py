from collect_papers import *
repos=[('SelfCheckGPT','potsawee/selfcheckgpt'),('FActScore','shmsw25/FActScore'),('AlignScore','yuh-zha/AlignScore'),('HaluEval','RUCAIBox/HaluEval'),('TruthfulQA','sylinrl/TruthfulQA'),('Semantic_entropy','jlko/semantic_uncertainty'),('RAGTruth','ParticleMedia/RAGTruth'),('FELM','HKUST-KnowComp/FELM'),('SummaC','tingofurro/summac'),('QAFactEval','salesforce/QAFactEval'),('QuestEval','ThomasScialom/QuestEval'),('FRANK','artidoro/frank')]
def fetchrepo(pair):
    name,repo=pair;row=dict(name=name,url='https://github.com/'+repo)
    try:
        info=json.loads(get('https://api.github.com/repos/'+repo));branch=info['default_branch']
        row['license']=(info.get('license') or {}).get('spdx_id','not declared');row['branch']=branch;row['retrieved_at']='2026-11-06'
        commit=json.loads(get(f'https://api.github.com/repos/{repo}/commits/{branch}'))['sha'];row['commit']=commit
        url=f'https://codeload.github.com/{repo}/zip/{commit}'
        b=get(url,100)
        import io
        z=zipfile.ZipFile(io.BytesIO(b));row['files']=len(z.namelist())
        dest=OUT/'code'/f'{name}_{commit[:8]}.zip';dest.write_bytes(b)
        row['archive']=str(dest.relative_to(OUT));row['status']='downloaded';row['bytes']=len(b)
    except Exception as e:row['status']='unavailable: '+str(e)
    print(name,row['status'],flush=True);return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(fetchrepo,repos))
(OUT/'code/repositories.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
