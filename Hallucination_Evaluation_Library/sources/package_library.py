from collect_papers import *
import shutil, subprocess, difflib
allp=json.loads((OUT/'metadata/all_candidates.json').read_text(encoding='utf-8'))
exclude=['cognometry','refute:','cross-modal','vlms','multimodal','detox','elastic weight','steering knowledge','financial decision','prompted for graphs','knowledge alignment problem','check your facts and try again','zero-resource hallucination prevention','teaching language models to hallucinate less','pruned large','question decomposition improves','truth-o-meter','improving factual consistency of text summarization by adversarially','towards faithful neural table','looking beyond sentence','knowledge-constrained tree','sources of hallucination','origin of hallucinations','entity-based knowledge conflicts','knowledge-augmented language model verification','llm lies:']
selected=[];rejected=[];seen=set()
for p in allp:
    why=''
    if not p['core'] and any(x in p['title'].lower() for x in exclude):why='outside focused evaluation scope or source mismatch'
    if p.get('verified_title') and difflib.SequenceMatcher(None,norm(p['title']),norm(p['verified_title'])).ratio()<.65:why='primary title mismatch'
    if p['url'] in seen:why='duplicate canonical URL'
    if why:p['exclusion_reason']=why;rejected.append(p);continue
    seen.add(p['url']);selected.append(p)
extra=[('2303.16634','LLM-as-a-Judge'),('2306.05685','LLM-as-a-Judge'),('2304.01379','LLM-as-a-Judge'),('2305.17926','LLM-as-a-Judge'),('2207.05221','uncertainty'),('2302.09664','uncertainty'),('2109.07958','uncertainty'),('2406.15927','uncertainty'),('2404.12060','meta-evaluation'),('2403.00724','RAG')]
for aid,area in extra:
    p=metadata(dict(title='',url='https://arxiv.org/abs/'+aid,discovery_source='primary arXiv seed; title verified automatically',source_section=area,core=False,code_url=''))
    if p.get('verified_title') and p['url'] not in seen:p['title']=p['verified_title'];selected.append(p);seen.add(p['url'])
def category(p):
    t=(p['title']+' '+p.get('source_section','')).lower()
    if re.search('survey|audit|pitfalls|definitions',t):return '01_Definitions_Surveys','C01;C02;C03;C04;C15;C16','范一鸣 / 程子晨','梳理术语、边界和综述分类；不把综述替代原始实验论文。'
    if re.search('chinese|multilingual|translation|medical|med-halt|medhallu|legal|psiloqa',t):return '08_Domain_Multilingual','C05;C06;C13','李瑾 / 张磊 / 程子晨','检验评估在中文、多语言或专业领域的适用边界。'
    if re.search('rag|retrieval|ground|attribut|citation|supporting evidence|graph|claim verification|fact-check',t):return '05_Evidence_RAG','C07;C09;C12','李瑾 / 程子晨','比较外部证据、检索质量与事实验证；关注忠实性和事实性是否分开。'
    if re.search('uncertainty|confidence|entropy|internal|hidden|attention|inside|belief|selfcheck|consistency|cross.check|snowball|lying|android|ignorance|drift|know when|answerability',t):return '06_Uncertainty_Consistency','C08;C10','杨桑多杰 / 程子晨','围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。'
    if re.search('human|judge|chatgpt|g-eval|gptscore|gpt-4|reasoners|cross examination|chainpoll|lynx|teacher|meta-evaluation|mirage|illusion of progress',t):return '07_Judges_Human_Meta','C11;C14','杨桑多杰 / 张磊 / 程子晨','考察裁判偏差、人工一致性和跨模型元评估；不直接比较异构数据集分数。'
    if re.search('benchmark|dataset|truthfulqa|halueval|hades|factor|felm|hallu|realtime|fresh|bamboo|factchd',t):return '02_Benchmarks','C05;C06;C12;C13','李瑾 / 程子晨','比较标注粒度、错误覆盖、数据构造与污染风险。'
    if re.search('question|qa|feqa|qags|questeval|qafact|q²|q2',t):return '04_QA_Based_Metrics','C09;C11','李瑾 / 程子晨','比较问答式核验和基准；分析问题生成及答案匹配误差。'
    return '03_Factuality_Entailment','C07;C09;C11','李瑾 / 张磊 / 程子晨','比较细粒度事实性、蕴含/分类指标及摘要评价的历史基础。'
# Stable core numbers follow the explicit seed order, not discovery order.
core_order={norm(t):i+1 for i,(t,_,_) in enumerate(CORE)}
selected.sort(key=lambda p:(not p['core'],core_order.get(norm(p['title']),99) if p['core'] else category(p)[0],p['title']))
ci=ii=0
for p in selected:
    if p['core']:ci+=1;p['id']=f'C{ci:02d}'
    else:ii+=1;p['id']=f'I{ii:03d}'
    p['area'],p['related_core'],p['owner'],p['reading_focus']=category(p)
    p['title']=p.get('verified_title') or p['title']
    slug=re.sub(r'[^A-Za-z0-9]+','_',p['title']).strip('_')[:100]
    p['local_pdf']=f"papers/{'core' if p['core'] else 'important'}/{p['id']}_{slug}.pdf"
def download(p):
    dest=OUT/p['local_pdf'];urls=[]
    if p.get('pdf_url'):urls.append(p['pdf_url'])
    if 'arxiv.org/abs/' in p['url']:urls += [p['url'].replace('/abs/','/pdf/'),p['url'].replace('arxiv.org/abs/','export.arxiv.org/pdf/')]
    if 'aclanthology.org' in p['url']:urls += [p['url'].rstrip('/')+'.pdf']
    for u in dict.fromkeys(urls):
        try:
            b=get(u,55)
            if not b.startswith(b'%PDF'):raise ValueError('not PDF')
            dest.write_bytes(b);p['download_status']='downloaded';p['bytes']=len(b);p['sha256']=hashlib.sha256(b).hexdigest();p['download_url']=u
            # Save only the first page text for identity checking, not full-text redistribution as text.
            exe=Path(r'C:\Users\23136\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftotext.exe')
            if exe.exists():
                q=subprocess.run([str(exe),'-f','1','-l','1',str(dest),'-'],capture_output=True)
                p['first_page_text']=q.stdout.decode('utf-8','replace')[:6000]
                (OUT/'metadata'/f"{p['id']}_first_page.txt").write_text(p['first_page_text'],encoding='utf-8')
            return p
        except Exception as e:p['download_status']=str(e)
    p['download_status']='unavailable: '+p.get('download_status','no open PDF link')
    return p
print('SELECTED',ci,'CORE',ii,'IMPORTANT',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
    done=[]
    for p in ex.map(download,selected):
        done.append(p)
        if len(done)%10==0:print('PDF',len(done),'OK',sum(x.get('download_status')=='downloaded' for x in done),flush=True)
(OUT/'metadata/selected.json').write_text(json.dumps(done,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'metadata/excluded.json').write_text(json.dumps(rejected,ensure_ascii=False,indent=2),encoding='utf-8')
print('FINISHED PDFs',sum(p.get('download_status')=='downloaded' for p in done),flush=True)
