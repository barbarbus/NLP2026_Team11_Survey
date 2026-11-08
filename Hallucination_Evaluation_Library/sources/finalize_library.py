from collect_papers import *
from pypdf import PdfReader
import shutil, collections
rows=json.loads((OUT/'metadata/selected.json').read_text(encoding='utf-8'))
removed=[];final=[];keys={};hashes={}
bad={'I049','I098','I099','I038','I039'}
for p in rows:
    reason=''
    if p['id'] in bad:reason='人工复核排除：无关论文或仅为解释忠实性/纠错扩展'
    elif p.get('download_status')!='downloaded':reason='未获得可校验PDF，不计入已打包重要论文数量'
    elif norm(p['title']) in keys:reason='同名论文不同版本，合并至 '+keys[norm(p['title'])]
    elif p.get('sha256') in hashes:reason='相同PDF，合并至 '+hashes[p['sha256']]
    elif 'frank' in p['title'].lower() and any('frank' in q['title'].lower() for q in final):reason='FRANK会议版与预印本重复，保留单篇'
    if reason:
        p['exclusion_reason']=reason;removed.append(p)
        src=OUT/p['local_pdf']
        if src.exists():
            dest=ROOT/'screening_excluded';dest.mkdir(exist_ok=True);shutil.move(str(src),str(dest/src.name))
        continue
    keys[norm(p['title'])]=p['id'];hashes[p['sha256']]=p['id']
    # Correct broad automatic labels for well-known families.
    t=p['title'].lower()
    if any(s in t for s in ['qafacteval','feqa','questeval','qags','asking and answering','q^{2}','q2:']):p.update(area='04_QA_Based_Metrics',related_core='C09;C11',owner='李瑾 / 程子晨',reading_focus='问答式事实核验：比较问题覆盖率、答案匹配误差和人工一致性。')
    elif any(s in t for s in ['summac','factcc','evaluating the factual consistency of abstractive','dependency-level','entity-level','fast and accurate factual','trueteacher']):p.update(area='03_Factuality_Entailment',related_core='C07;C09;C11',owner='李瑾 / 程子晨',reading_focus='蕴含/分类型事实一致性指标：比较粒度、训练信号和跨任务元评估。')
    elif any(s in t for s in ['factual inconsistency evaluator','llm-based nlg','summeval','multi-dimensional evaluation']):p.update(area='07_Judges_Human_Meta',related_core='C11;C14',owner='杨桑多杰 / 张磊 / 程子晨',reading_focus='自动评估与人工判断一致性、评价协议和裁判偏差。')
    p['identity_status']='PDF header and page parsing passed; title words checked on first page'
    p['reading_status']='已核验书目信息和PDF首页；未逐篇完成全文精读'
    final.append(p)
codes=json.loads((OUT/'code/repositories.json').read_text(encoding='utf-8'))
try:
    repo='hkust-nlp/felm';info=json.loads(get('https://api.github.com/repos/'+repo));branch=info['default_branch'];sha=json.loads(get(f'https://api.github.com/repos/{repo}/commits/{branch}'))['sha']
    b=get(f'https://codeload.github.com/{repo}/zip/{sha}',100);zipfile.ZipFile(__import__('io').BytesIO(b)).testzip()
    path=f'code/FELM_{sha[:8]}.zip';(OUT/path).write_bytes(b)
    codes=[c for c in codes if c['name']!='FELM']+[dict(name='FELM',url='https://github.com/'+repo,commit=sha,branch=branch,license=(info.get('license') or {}).get('spdx_id','not declared'),archive=path,status='downloaded',bytes=len(b))]
except Exception as e:print('FELM retry',str(e))
(OUT/'code/repositories.json').write_text(json.dumps(codes,ensure_ascii=False,indent=2),encoding='utf-8')
for n in ['candidate_source.md','eval_source.md','survey_source.md']:shutil.copy2(ROOT/n,OUT/'sources'/n)
(OUT/'metadata/final_manifest.json').write_text(json.dumps(final,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'metadata/packaging_exclusions.json').write_text(json.dumps(removed,ensure_ascii=False,indent=2),encoding='utf-8')
fields=['id','core','title','authors','date','doi','url','area','related_core','owner','reading_focus','local_pdf','pages','bytes','sha256','download_status','verification','title_word_coverage','code_url','reading_status']
with (OUT/'paper_catalog.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(final)
bib=[]
for p in final:
    year=re.search(r'(19|20)\d{2}',p.get('date',''))
    if not year and 'arxiv.org' in p['url']:year=re.search(r'/(\d{2})\d{2}\.',p['url']);yearval='20'+year[1] if year else ''
    else:yearval=year[0] if year else ''
    title=p['title'].replace('&',r'\&').replace('_',r'\_').replace('$','')
    entry=f'@misc{{{p["id"]},\n  title = {{{title}}},\n  url = {{{p["url"]}}}'
    if p.get('authors'):entry+=',\n  author = {'+' and '.join(p['authors'].split('; '))+'}'
    if yearval:entry+=',\n  year = {'+yearval+'}'
    entry+='\n}\n';bib.append(entry)
(OUT/'references.bib').write_text('\n'.join(bib),encoding='utf-8')
core=[p for p in final if p['core']];important=[p for p in final if not p['core']]
names={'01_Definitions_Surveys':'定义、术语与综述框架','02_Benchmarks':'评估数据集与基准','03_Factuality_Entailment':'事实一致性、分类与蕴含指标','04_QA_Based_Metrics':'问答式事实评估','05_Evidence_RAG':'外部证据核验与RAG忠实性','06_Uncertainty_Consistency':'自洽性、不确定性与内部信号','07_Judges_Human_Meta':'LLM裁判、人工评价与元评估','08_Domain_Multilingual':'中文、多语言与领域泛化'}
guide=['# 文献研究地图与阅读安排','',f'整理日期：2026-11-06。核心论文 {len(core)} 篇，核心之外的重要论文 {len(important)} 篇。所有计入数量的论文均已保存可解析PDF。','', '分类与“对应核心”表示本项目的概念组织关系，并非已验证的直接引用或继承关系。重要论文是推荐候选池，不表示已完成全文精读，也不表示每篇都必须写入最终8页报告。预印本与已发表版本须在最终引用前再次统一。','', '## 核心阅读顺序','', '先读 C01–C04 建立全景，结合 C15–C16 明确“事实性、忠实性、无支持信息”的区别；再读 C05–C06 和 C13 了解基准；随后比较 C07–C10 的不同方法；以 C11、C14 检查评价方法自身是否可靠，最后用 C12 连接RAG场景。','']
focus={ 'C01':'历史基础：NLG幻觉定义、任务边界与早期指标。','C02':'LLM全景框架：事实性/忠实性、检测方法和基准分类。','C03':'补充全景视角，交叉核对分类，而非照搬现成综述。','C04':'最贴近本选题的自动评估综述；重点比较我们的分类维度与现有综述的差异。','C05':'真实性基准：常见误解与开放问答；不能等同所有形式的幻觉。','C06':'幻觉识别基准：考察合成错误与自然错误的分布差异。','C07':'原子事实核验：研究事实分解、证据检索和事实精确率的局限。','C08':'黑箱采样一致性：研究无需外部证据时的检测及多次采样成本。','C09':'统一对齐函数：比较蕴含/训练型指标与LLM裁判。','C10':'语义熵：区分语义不确定性与词面变化，讨论自信错误的边界。','C11':'跨任务元评估：关注自动指标和人工标注的对齐，而非单一排行榜。','C12':'RAG细粒度标注：区分证据忠实性、无依据内容和事实错误。','C13':'事实评价器的基准：区分被评价模型与评价器自身的能力。','C14':'人工评价协议：标注指南、标注者信息和一致性报告。','C15':'术语审计：追踪不同论文对幻觉定义的不一致。','C16':'定义反思：为什么不能把无支持、虚假、遗漏等概念混为一谈。'}
for p in core:guide += [f'### {p["id"]} {p["title"]}',focus.get(p['id'],''),f'[原始页面]({p["url"]}) · [本地PDF]({p["local_pdf"]})','']
guide+=['## 重要论文如何围绕核心论文展开','']
for cat,label in names.items():
    group=[p for p in important if p['area']==cat]
    if not group:continue
    guide += [f'### {label}（{len(group)}篇）','']
    for p in group:guide += [f'- **{p["id"]} {p["title"]}** — 对应核心：{p["related_core"]}；负责人：{p["owner"]}。{p["reading_focus"]} [PDF]({p["local_pdf"]}) / [来源]({p["url"]})']
    guide+=['']
guide+=['## 全体成员的交付标准','', '程子晨参与并负责所有研究方面，组织分类讨论、证据核查和总稿整合。每位成员先从其负责方向选择4–6篇精读，再扩展阅读；所有结论必须记录论文页码、实验条件和证据。每篇阅读笔记应包括：定义、任务、粒度、证据来源、方法机制、基准、人工一致性、泛化性、成本、局限及可复现资源。未读出的信息写“未报告/待确认”，不要据标题补造结论。','', '源码用于理解方法和按需复现实验，Track A不要求训练全部模型。源码快照均未运行，不包含额外模型权重和外部数据下载；依赖与许可证以各原仓库为准。']
(OUT/'research_map.md').write_text('\n'.join(guide),encoding='utf-8')
readme=f'''# 大语言模型幻觉评估方法综述 研究资料包

整理日期：2026-11-06

已打包：{len(core)}篇核心论文 + {len(important)}篇独立重要论文，共{len(final)}篇可解析PDF；{sum(c['status']=='downloaded' for c in codes)}个相关官方源码仓库快照。

先打开 research_map.md 查看核心阅读顺序和每篇重要论文对应的研究方面、核心论文及负责人。paper_catalog.csv 可以用Excel打开和筛选；references.bib 是初步引用库；metadata/final_manifest.json 包含下载URL、SHA256、页数和核验状态。

重要：这是经书目信息、原始落地页及PDF首页核验的选题阅读库，不是逐篇全文精读报告。“对应核心”是本项目概念关联，不是论文直接引用关系。方法优劣和实验结果须在精读时填写，不作未验证的性能结论。传统摘要/翻译评估研究用于解释方法源流，多语言、医学、法律论文用于讨论泛化边界；最终8页报告应精选证据，不能罗列全部文献。

核心目录 papers/core；重要目录 papers/important。文件编号有间断，来自筛除错链、重复版本和未获得全文的记录，不代表缺失文件。

code/repositories.json 记录原仓库、下载状态、提交SHA与许可证；每个ZIP保留仓库自身LICENSE。源码未安装或执行。未下载模型权重，不承诺全部实验开箱即跑。

去重以规范化标题、下载文件SHA256和人工识别的会议版/预印本重复为依据。少量论文无机器可提取作者/日期，CSV保留空值，最终引用请以原始PDF核对；不编造字段。references.bib优先使用arXiv版本信息，最终报告应优先替换为正式发表记录。

候选来源：EdinburghNLP/awesome-hallucination-detection、综述作者LuckyyySTA/Awesome-LLM-hallucination及siyaqi/Awesome-Hallu-Eval；这些只是发现入口，PDF来自arXiv、ACL Anthology、Nature等原始来源。sources保留索引快照便于追溯，不代表接受其中全部描述。

metadata/packaging_exclusions.json 和 excluded.json 记录未纳入项。无关或重复已下载文件移到当前文件夹 screening_excluded，不进入正式资料包。源码和论文仅供课程研究，转发时请遵守各来源许可。
'''
(OUT/'README.md').write_text(readme,encoding='utf-8')
for s in ['collect_papers.py','package_library.py','collect_code.py','audit_library.py','finalize_library.py']:shutil.copy2(ROOT/s,OUT/'sources'/s)
assert len(important)>=100
assert all((OUT/p['local_pdf']).exists() for p in final)
summary=dict(core=len(core),important=len(important),total=len(final),code_archives=sum(c['status']=='downloaded' for c in codes),pdf_bytes=sum(p['bytes'] for p in final),areas=dict(collections.Counter(p['area'] for p in important)),excluded=len(removed))
(OUT/'metadata/summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
archive=shutil.make_archive(str(ROOT/'Hallucination_Evaluation_Library'),'zip',ROOT,OUT.name)
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(json.dumps(summary,ensure_ascii=True));print('ZIP',archive,Path(archive).stat().st_size)
