import re, json, csv, time, html, hashlib, zipfile, urllib.request, concurrent.futures
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'Hallucination_Evaluation_Library'
for d in ['papers/core','papers/important','metadata','code','sources']:(OUT/d).mkdir(parents=True,exist_ok=True)
def get(url,timeout=45):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (academic literature collection)'})
    with urllib.request.urlopen(req,timeout=timeout) as r:return r.read()
def norm(s):return re.sub('[^a-z0-9]','',s.lower())
items={}
def add(title,url,source,section='',core=False,code=''):
    url=url.strip().replace('http://','https://')
    m=re.search(r'(\d{4}\.\d{4,5})',url)
    if m:url='https://arxiv.org/abs/'+m[1]
    elif 'aclanthology.org' in url:url=url.removesuffix('.pdf').rstrip('/')+'/'
    key=norm(title)
    if key in items:
        if core:items[key]['core']=True
        return
    items[key]=dict(title=html.unescape(title),url=url,discovery_source=source,source_section=section,core=core,code_url=code)
src=ROOT/'candidate_source.md'
text=src.read_text(encoding='utf-8')
for m in re.finditer(r'^### \[(.*?)\]\((https?[^\s]+)\)(.*?)(?=^### |\Z)',text,re.M|re.S):
    title,url,body=m.groups()
    if re.search(r'vision|visual|multimodal|multi-modal|image|video|segmentation|object halluc|code-related',title,re.I):continue
    if not re.search(r'detect|evaluat|benchmark|uncertainty|confidence|factual|faithful|survey|hallucinat|truth|know',title,re.I):continue
    if re.search(r'decoding|mitigat|reducing|reduce|reinforcement|prunecd|parammute|spark|knowledge adapting|editing.*space',title,re.I) and not re.search(r'detect|evaluat|benchmark|uncertainty|survey',title,re.I):continue
    codes=re.findall(r'https://github.com/[\w.-]+/[\w.-]+',body)
    add(title,url,'https://github.com/EdinburghNLP/awesome-hallucination-detection',code=codes[0] if codes else '')
text=(ROOT/'survey_source.md').read_text(encoding='utf-8')
section='';active=False
for block in re.split(r'\n\s*\n',text):
    if block.startswith('#'):
        section=block.strip()
        if 'Hallucination Detection and Benchmarks' in block:active=True
        if 'Hallucination Mitigation' in block:active=False
    if active:
        m=re.search(r'\d+\. \*\*(.*?)\*\*',block)
        if m:pending=m[1]
        p=re.search(r'\[\[paper\]\]\((https?[^)]+)\)',block)
        if p and 'pending' in locals():add(pending,p[1],'https://github.com/LuckyyySTA/Awesome-LLM-hallucination',section)
CORE=[
('Survey of Hallucination in Natural Language Generation','2202.03629',''),
('A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions','2311.05232',''),
("Siren’s Song in the AI Ocean: A Survey on Hallucination in Large Language Models",'2309.01219',''),
('A Survey of Automatic Hallucination Evaluation on Natural Language Generation','2404.12041',''),
('TruthfulQA: Measuring How Models Mimic Human Falsehoods','https://aclanthology.org/2022.acl-long.229/','sylinrl/TruthfulQA'),
('HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models','2305.11747','RUCAIBox/HaluEval'),
('FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation','2305.14251','shmsw25/FActScore'),
('SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models','2303.08896','potsawee/selfcheckgpt'),
('AlignScore: Evaluating Factual Consistency with A Unified Alignment Function','2305.16739','yuh-zha/AlignScore'),
('Detecting hallucinations in large language models using semantic entropy','https://www.nature.com/articles/s41586-024-07421-0','jlko/semantic_uncertainty'),
('TRUE: Re-Evaluating Factual Consistency Evaluation','2204.04991','google-research/true'),
('RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models','2401.00396','ParticleMedia/RAGTruth'),
('FELM: Benchmarking Factuality Evaluation of Large Language Models','2310.00741','HKUST-KnowComp/FELM'),
('Do My Eyes Deceive Me? A Survey of Human Evaluations of Hallucinations in NLG','https://aclanthology.org/2025.inlg-main.4/',''),
('An Audit on the Perspectives and Challenges of Hallucinations in NLP','https://aclanthology.org/2024.emnlp-main.375/',''),
('The Pitfalls of Defining Hallucination','https://aclanthology.org/2024.cl-2.10/','')]
for t,u,c in CORE:
    add(t,u if u.startswith('http') else 'https://arxiv.org/abs/'+u,'core seed verified by primary landing page',core=True,code='https://github.com/'+c if c else '')
    # Merge pre-existing abbreviated variants by canonical URL.
    target=items[norm(t)]
    for k,v in list(items.items()):
        if v is not target and v['url']==target['url']:
            if not target['code_url']:target['code_url']=v['code_url']
            del items[k]
EXTRA=[('SummEval: Re-evaluating Summarization Evaluation','https://aclanthology.org/2021.tacl-1.24/'),('FEQA: A Question Answering Evaluation Framework for Faithfulness Assessment in Abstractive Summarization','https://aclanthology.org/2020.acl-main.454/'),('Asking and Answering Questions to Evaluate the Factual Consistency of Summaries','https://aclanthology.org/2020.acl-main.450/'),('RAGAs: Automated Evaluation of Retrieval Augmented Generation','https://aclanthology.org/2024.eacl-demo.16/'),('ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems','https://aclanthology.org/2024.naacl-long.20/'),('Factuality of Large Language Models: A Survey','https://aclanthology.org/2024.emnlp-main.1088/'),('Language Models Hallucinate, but May Excel at Fact Verification','https://aclanthology.org/2024.naacl-long.62/'),('The Dawn After the Dark: An Empirical Study on Factuality Hallucination in Large Language Models','https://aclanthology.org/2024.acl-long.586/'),('LLM-based NLG Evaluation: Current Status and Challenges','https://aclanthology.org/2025.cl-2.9/'),('FRANK: A Benchmark for Factuality Metrics','https://aclanthology.org/2021.naacl-main.383/')]
for t,u in EXTRA:add(t,u,'ACL Anthology primary search')
def metadata(p):
    try:
        b=get(p['url'],30);s=b.decode('utf-8','replace')
        tags={}
        for tag in re.findall(r'<meta\b[^>]*>',s,re.I):
            attrs=dict((k.lower(),html.unescape(v)) for k,q,v in re.findall(r'([\w:-]+)\s*=\s*([\x22\x27])(.*?)\2',tag,re.S))
            name=attrs.get('name',attrs.get('property','')).lower()
            if name:tags.setdefault(name,[]).append(attrs.get('content',''))
        title=(tags.get('citation_title') or [None])[0]
        if not title:
            m=re.search(r'<h1[^>]*class="[^"]*title[^>]*>(.*?)</h1>',s,re.S)
            if m:title=re.sub('<[^>]+>','',m[1]).replace('Title:','').strip()
        p['verified_title']=title or ''
        p['authors']='; '.join(tags.get('citation_author',[]))
        p['date']=(tags.get('citation_date') or tags.get('citation_publication_date') or [''])[0]
        p['doi']=(tags.get('citation_doi') or [''])[0]
        p['pdf_url']=(tags.get('citation_pdf_url') or [''])[0]
        if 'aclanthology.org' in p['url'] and not p['pdf_url']:p['pdf_url']=p['url'].rstrip('/')+'.pdf'
        if 'arxiv.org/abs/' in p['url'] and not p['pdf_url']:p['pdf_url']=p['url'].replace('/abs/','/pdf/')
        p['verification']='primary metadata' if title else 'landing page reachable; title not extracted'
        codes=re.findall(r'https://github.com/[\w.-]+/[\w.-]+',s)
        if not p['code_url'] and codes:p['code_url']=codes[0].rstrip('.')
        (OUT/'metadata'/f"{hashlib.sha1(p['url'].encode()).hexdigest()[:12]}.json").write_text(json.dumps(tags,ensure_ascii=False,indent=2),encoding='utf-8')
    except Exception as e:p['verification']='failed: '+str(e)
    return p
if __name__=='__main__':
    pool=list(items.values());print('CANDIDATES',len(pool),flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        verified=[]
        for p in ex.map(metadata,pool):
            verified.append(p)
            if len(verified)%15==0:print('VERIFIED',len(verified),flush=True)
    (OUT/'metadata/all_candidates.json').write_text(json.dumps(verified,ensure_ascii=False,indent=2),encoding='utf-8')
    print('DONE',len(verified),sum(bool(p.get('verified_title')) for p in verified),flush=True)
