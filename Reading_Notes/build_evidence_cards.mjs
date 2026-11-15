import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const base = path.dirname(fileURLToPath(import.meta.url));
const root = path.dirname(base);
const csv = fs.readFileSync(path.join(base, 'Taxonomy_124.csv'), 'utf8').replace(/^\uFEFF/, '');
function parseCsv(s) {
  const records = []; let row = [], field = '', quoted = false;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (c === '"') { if (quoted && s[i + 1] === '"') { field += '"'; i++; } else quoted = !quoted; }
    else if (c === ',' && !quoted) { row.push(field); field = ''; }
    else if ((c === '\n' || c === '\r') && !quoted) { if (c === '\r' && s[i + 1] === '\n') i++; row.push(field); field = ''; if (row.some(Boolean)) records.push(row); row = []; }
    else field += c;
  }
  if (field || row.length) { row.push(field); records.push(row); }
  const [headers, ...data] = records;
  return data.map(values => Object.fromEntries(headers.map((h, i) => [h, values[i] ?? ''])));
}
const rows = parseCsv(csv);
const maplines = new Map();
for (const line of fs.readFileSync(path.join(base, 'Research_Map_Reviewed.md'), 'utf8').split(/\r?\n/)) {
  const m = line.match(/^-\s+([CI]\d{2,3})\s+[^：:]+[：:]\s*主类(.+?)；次类(.+)/);
  if (m) maplines.set(m[1], [m[2].trim().replace(/。$/, ''), m[3].trim()]);
}
function clean(s, limit) {
  s = s.replace(/\[([^\]]+)\]\([^)]*\)/g, '$1').replace(/[`*_>#]/g, '').replace(/\s+/g, ' ').trim();
  return s.length > limit ? s.slice(0, limit) + '…' : s;
}
function sections(s) {
  return s.split(/^##\s+/m).slice(1).map(p => {
    const [head, ...body] = p.split(/\r?\n/); return [head.trim(), body.join('\n').trim()];
  });
}
const out = ['# 124篇文献的证据卡片', '',
  '本文件把分类和逐篇阅读笔记中的原有判断放在同一处，供五位组员核查与摘录。每条的“研究定位”和“限制”来自现有笔记或已审阅研究地图；它们是本组阅读记录，不能代替论文原文。正式报告引用具体数值时，仍须逐项核对原文页码、表格和实验设置。', '',
  '字段说明：技术主类与评价对象来自 `Taxonomy_124.csv`；研究定位优先取 `Research_Map_Reviewed.md` 的“主类”，否则取该笔记第一个实质小节；限制优先取研究地图“次类”，否则取笔记中明确的局限或待办小节。', ''];
for (const r of rows) {
  const note = path.join(root, r.reading_note.replaceAll('/', path.sep));
  if (!fs.existsSync(note)) throw new Error(`Missing note ${note}`);
  const ss = sections(fs.readFileSync(note, 'utf8'));
  const substantive = ss.find(([h]) => /^1[.、 ]|^1\b/.test(h)) ?? ss.find(([h]) => !/来源|版本|范围|文献|核查/.test(h)) ?? ['', ''];
  const evidence = clean(substantive[1].split(/\n\s*\n/).find(Boolean) ?? '见原笔记；本卡未自动抽出定位段落。', 420);
  const caveatSection = ss.find(([h]) => /局限|边界|待办|不能写|研究问题/.test(h));
  const caveat = caveatSection ? clean(caveatSection[1].split(/\n\s*\n/).find(Boolean) ?? '见原笔记。', 380) : '见原笔记；本卡未自动抽出限制段落。';
  const [measure, concerns] = maplines.get(r.id) ?? [evidence, caveat];
  const rel = r.reading_note.replace(/^Reading_Notes\//, '');
  out.push(`## ${r.id} · ${r.title}`, '',
    `- **层级／研究角色：** ${r.level}／${r.study_role}`,
    `- **评价对象：** ${r.evaluation_target}`,
    `- **技术：** 主类 ${r.primary_method_code}；次类 ${r.secondary_method_codes || '无'}`,
    `- **研究定位：** ${measure}`,
    `- **需核查的条件或限制：** ${concerns}`,
    `- **阅读笔记中的证据片段：** ${evidence}`,
    `- **来源：** [精读笔记](${rel})；[论文页面](${r.paper_url})`, '');
}
fs.writeFileSync(path.join(base, 'Evidence_Cards_124.md'), out.join('\n'), 'utf8');
console.log(`${rows.length} cards; ${maplines.size} map entries`);
