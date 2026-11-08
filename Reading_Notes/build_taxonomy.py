"""Build a reviewed, multi-label taxonomy of the 124-paper reading corpus."""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent

def ids(s: str) -> set[str]:
    return set(s.split())

# H human; E explicit external evidence / QA / claims; T trained semantic or
# representation detector; U sampling, confidence or uncertainty; J LLM judge.
# A dash means the paper's principal contribution is a resource, analysis, or
# synthesis, rather than an evaluator belonging to one of the five methods.
PRIMARY = {
    'H': ids('C14 I037'),
    'E': ids('C07 I005 I006 I015 I029 I032 I041 I042 I043 I046 I047 I048 I050 I054 I057 I058 I059 I062 I072 I086'),
    'T': ids('C09 I016 I017 I019 I023 I026 I027 I031 I036 I044 I051 I063 I067 I069 I073 I074 I076 I078 I090 I092 I093 I094 I095 I106 I109 I118 I119'),
    'U': ids('C08 C10 I002 I020 I022 I045 I052 I055 I060 I061 I064 I066 I068 I070 I071 I075 I079 I080 I081 I082 I083 I084 I085 I087 I088 I091 I096'),
    'J': ids('I010 I018 I034 I065 I097 I100 I101 I104'),
}

SURVEY = ids('C01 C02 C03 C04 C14 C15 C16 I001 I033')
BENCHMARK = ids('C05 C06 C12 C13 I003 I004 I007 I008 I011 I012 I013 I014 I021 I040 I053 I102 I103 I110 I111 I114 I115 I116 I117')
META = ids('C11 I007 I036 I037 I102 I103 I105 I107')
EMPIRICAL = ids('I024 I035 I068 I077 I108 I112 I113')

# Cross-family mechanisms actually evaluated or combined in the paper. These
# are secondary labels, not extra counts in the primary-method totals.
SECONDARY = {
    'C05':'T J H', 'C06':'H J', 'C07':'J', 'C08':'T J', 'C09':'E', 'C11':'E T',
    'C12':'T H', 'C13':'E J H', 'C14':'J',
    'I002':'E', 'I003':'H T', 'I005':'J H', 'I006':'T J', 'I007':'H E T',
    'I008':'T J H', 'I010':'H', 'I011':'E J H', 'I012':'U E', 'I013':'E J H',
    'I014':'J H', 'I015':'E H', 'I016':'U', 'I017':'U', 'I018':'J E',
    'I019':'J', 'I020':'J E', 'I022':'J', 'I023':'J', 'I026':'U',
    'I027':'E', 'I029':'J', 'I031':'E', 'I032':'J', 'I034':'H', 'I035':'H E T',
    'I036':'E H', 'I037':'E T J', 'I040':'H T', 'I041':'J H', 'I043':'T',
    'I044':'E J H', 'I046':'J', 'I047':'T', 'I048':'J', 'I050':'J',
    'I051':'U', 'I052':'E', 'I053':'E J', 'I054':'T', 'I055':'E',
    'I057':'J', 'I058':'J', 'I059':'J', 'I060':'E', 'I061':'E',
    'I063':'T', 'I064':'T', 'I065':'H', 'I066':'E', 'I067':'U',
    'I068':'T U', 'I069':'U', 'I070':'T', 'I071':'T', 'I073':'E',
    'I074':'E', 'I076':'U', 'I077':'U', 'I078':'U', 'I079':'T',
    'I080':'T', 'I082':'T', 'I085':'E', 'I086':'T', 'I087':'J',
    'I088':'J', 'I090':'U', 'I092':'E', 'I093':'U', 'I094':'U',
    'I095':'J', 'I096':'J T', 'I097':'U', 'I100':'H', 'I101':'H',
    'I102':'J H', 'I103':'J E', 'I104':'U', 'I105':'J H',
    'I106':'J E', 'I107':'T J H', 'I108':'H E', 'I109':'E',
    'I110':'J H', 'I111':'H T', 'I112':'H', 'I113':'H E',
    'I114':'H T', 'I115':'J H', 'I116':'J H', 'I117':'E J H',
    'I119':'H',
}

TARGET = {
    'source':'C09 C11 C12 I003 I004 I005 I006 I007 I015 I027 I031 I034 I035 I036 I037 I042 I043 I044 I054 I057 I062 I065 I072 I073 I074 I086 I092 I095 I101 I103 I106 I109 I111 I112 I114 I118 I119',
    'world':'C05 C07 C08 C10 C13 I002 I008 I010 I011 I012 I013 I014 I016 I017 I018 I019 I020 I021 I022 I023 I024 I026 I029 I032 I040 I045 I046 I047 I048 I050 I051 I058 I059 I060 I061 I063 I064 I066 I067 I068 I069 I070 I071 I075 I076 I077 I078 I079 I080 I081 I082 I083 I084 I085 I087 I088 I090 I091 I093 I094 I096 I097 I104 I107 I108 I110 I113 I115 I116 I117',
    'multi':'C01 C02 C03 C04 C06 C14 C15 C16 I001 I033 I041 I052 I053 I055 I100 I102 I105',
}

LABEL = {'H':'人工评价','E':'参考/证据核验','T':'判别器/蕴含/内部表征','U':'自一致性/不确定性','J':'LLM 裁判','—':'无单一方法主类'}
TARGET_LABEL = {'source':'来源忠实性','world':'外部事实性/正确性','multi':'跨目标或概念研究'}

def role(p: str) -> str:
    if p in SURVEY: return '综述/概念'
    if p in META: return '元评估/审计'
    if p in BENCHMARK: return '基准/数据'
    if p in EMPIRICAL: return '领域实证/现象分析'
    return '评价方法'

def main() -> None:
    with (ROOT/'Hallucination_Evaluation_Library/paper_catalog.csv').open(encoding='utf-8-sig',newline='') as f:
        catalog=list(csv.DictReader(f))
    all_ids={p['id'] for p in catalog}
    assert len(catalog)==len(all_ids)==124
    owners={p:family for family,group in PRIMARY.items() for p in group}
    assert sum(map(len,PRIMARY.values()))==len(owners), 'Duplicate primary categories'
    assert not (set(owners)-all_ids)
    assert not (set(SECONDARY)-all_ids)
    targets={p:k for k,group in TARGET.items() for p in ids(group)}
    assert len(targets)==sum(len(ids(group)) for group in TARGET.values()), 'Duplicate target'
    assert len(targets)==124 and set(targets)==all_ids, f'Missing targets: {sorted(all_ids-set(targets))}'
    notes={p.stem.split('_')[0]:p for p in (OUT/'notes').glob('*/*.md')}
    assert set(notes)==all_ids, f'Missing note: {sorted(all_ids-set(notes))}'
    rows=[]
    for p in catalog:
        pid=p['id']; primary=owners.get(pid,'—'); secondary=SECONDARY.get(pid,'').split()
        secondary=[s for s in secondary if s!=primary]
        assert all(s in LABEL and s!='—' for s in secondary)
        rows.append({
            'id':pid, 'level':'core' if p['core'].lower() in ('true','1','yes') else 'important',
            'title':p['title'], 'study_role':role(pid),
            'primary_method_code':primary, 'primary_method':LABEL[primary],
            'secondary_method_codes':';'.join(secondary),
            'secondary_methods':';'.join(LABEL[s] for s in secondary),
            'evaluation_target':TARGET_LABEL[targets[pid]],
            'reading_note':str(notes[pid].relative_to(ROOT)).replace('\\','/'),
            'paper_url':p['url'],
        })
    assert Counter(r['level'] for r in rows)=={'important':108,'core':16}
    path=OUT/'Taxonomy_124.csv'
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)

    count=Counter(r['primary_method_code'] for r in rows)
    secondary_count=Counter(s for r in rows for s in r['secondary_method_codes'].split(';') if s)
    lines=['# 124篇文献的技术分类（16 core + 108 important）','',
           '## 分类原则','',
           '主类沿用计划书的五条评价技术线：H 人工评价、E 参考/证据核验、T 判别器/蕴含/内部表征、U 自一致性/不确定性、J LLM 裁判。T 类包含训练探针、NLI 评价器，以及基于内部表征/注意力的异常判别；它们的监督要求另见逐篇笔记。',
           '每篇最多一个**技术主类**，可以有多个技术次类。`—`表示论文的主要贡献是基准、综述、元评估或现象分析，不能仅凭论文使用了某种基线就说它提出了该方法。',
           '另用“研究角色”和“评价对象”两个正交轴防止概念混淆。特别是来源忠实性不等于世界事实性；论文标题中的“hallucination”也不自动意味着相同的标注构念。',
           '分类依据是逐篇阅读笔记及原文；技术次类只记录重要交叉，不能理解为该论文覆盖该类全部方法。',
           '', '## 总览','',
           f'共 {len(rows)} 篇：core 16 篇、important 108 篇。技术主类：'+ '；'.join(f'{k} {LABEL[k]} {count[k]} 篇' for k in ['H','E','T','U','J','—'])+'。',
           '技术次类（可重叠）：'+'；'.join(f'{k} {secondary_count[k]} 篇' for k in ['H','E','T','U','J'])+'。主类与次类不能直接相加当作互斥论文数。',
           '研究角色：'+'；'.join(f'{k} {v} 篇' for k,v in Counter(r['study_role'] for r in rows).items())+'。','',
           '## 五类技术的判断标准','',
           '- **H 人工评价**：人工定义、标注、评分和人际一致性；人工标签用作基准金标时仅记为次类。',
           '- **E 参考/证据核验**：将输出拆为声明、实体、关系或问答，依据源文、检索证据或知识图谱判断支持性。',
           '- **T 判别器/蕴含/内部表征**：使用训练的事实性判别器、NLI 模型，或隐藏状态与注意力等内部特征建立检测分数。',
           '- **U 自一致性/不确定性**：跨采样语义一致性、置信度、概率、熵、校准以及动态拒答风险。',
           '- **J LLM 裁判**：让通用大模型依据提示、评分规则或交叉询问判定事实性或忠实性。',
           '', '## 16篇核心论文速查','']
    for r in [r for r in rows if r['level']=='core']:
        note=Path(r['reading_note']).relative_to('Reading_Notes')
        lines.append(f"- [{r['id']}]({note.as_posix()}) {r['title']} — {r['study_role']}；技术主类 {r['primary_method_code']}，次类 {r['secondary_method_codes'] or '无'}。")
    lines += ['', '## 分类清单','']
    for fam in ['H','E','T','U','J','—']:
        subset=[r for r in rows if r['primary_method_code']==fam]
        lines += [f'### {fam} · {LABEL[fam]}（{len(subset)}篇）','',
                  '格式：ID〔core/important；研究角色；评价对象；次类〕标题。每条链接通向对应精读笔记。','']
        for r in subset:
            note=Path(r['reading_note']).relative_to('Reading_Notes')
            # Relative Markdown links keep the research package portable.
            sec=r['secondary_method_codes'] or '无'
            lines.append(f"- [{r['id']}]({note.as_posix()})〔{r['level']}；{r['study_role']}；{r['evaluation_target']}；次类 {sec}〕{r['title']}")
        lines.append('')
    lines += ['## 使用与边界','',
              '- 建议论文正文用“研究角色 × 五类技术 × 评价对象”的三层结构组织综述，而不是把所有基准强行算作方法。',
              '- 主类是为了统计和排版作出的主贡献判定；跨类论文须同时查看“次类”，例如 FActScore（E+J）、SelfCheckGPT（U+T/J）、ARES（T+E/J）。',
              '- 类别是研究地图，不代表复现完成或各论文主张已经由本组独立验证。具体数据、局限与待核查点见对应精读笔记。','']
    (OUT/'Taxonomy_124.md').write_text('\n'.join(lines),encoding='utf-8')
    print('Wrote',path,'and',OUT/'Taxonomy_124.md')
    print('Primary:',dict(count))
    print('Roles:',dict(Counter(r['study_role'] for r in rows)))

if __name__=='__main__': main()
