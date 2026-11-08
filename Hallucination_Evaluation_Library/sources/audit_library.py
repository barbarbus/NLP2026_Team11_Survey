from collect_papers import *
from pypdf import PdfReader
import difflib, shutil
p=json.loads((OUT/'metadata/selected.json').read_text(encoding='utf-8'))
for x in p:
    path=OUT/x['local_pdf']
    if path.exists():
        try:
            reader=PdfReader(path);x['pages']=len(reader.pages)
            txt=reader.pages[0].extract_text() or '';x['first_page_text']=txt[:9000]
            (OUT/'metadata'/f"{x['id']}_first_page.txt").write_text(txt,encoding='utf-8')
            titlewords=set(re.findall('[a-z]{4,}',x['title'].lower()))
            textwords=set(re.findall('[a-z]{4,}',txt[:4500].lower()))
            x['title_word_coverage']=round(len(titlewords&textwords)/max(1,len(titlewords)),2)
        except Exception as e:x['pdf_parse_error']=str(e)
(OUT/'metadata/selected.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
for x in p:
    if x.get('title_word_coverage',0)<.6:print(x['id'],x['title'],x.get('title_word_coverage'),x.get('first_page_text','')[:200].replace('\n',' '),flush=True)
