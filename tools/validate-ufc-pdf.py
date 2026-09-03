#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, shutil, subprocess, sys, tempfile, unicodedata, xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path

from normative_catalog import get_rule, load_catalog, rule_map, source_label

PASS='PASS'; FAIL='FAIL'; WARN='WARNING'; REVIEW='MANUAL REVIEW'; NA='NOT APPLICABLE'
MM=72/25.4
CATALOG=load_catalog(); RULES=rule_map(CATALOG)
PAGE=RULES['page.a4']['values']; RECTO=RULES['margin.recto']['values']
A4=(PAGE['width_mm']*MM,PAGE['height_mm']*MM); A4_TOLERANCE=PAGE.get('tolerance_pt',1.8)
LEFT=RECTO['left_mm']*MM; RIGHT=RECTO['right_mm']*MM

@dataclass
class Check:
    id:str; category:str; rule:str; source:str; status:str; evidence:str; correction:str=''; mandatory:bool=True; level:str='automatic'; normative_rule:str=''; locator:str=''; normativity:str=''

def run(cmd, check=True): return subprocess.run(cmd,text=True,capture_output=True,check=check)
def tool(name):
    p=shutil.which(name)
    if not p: raise SystemExit(f'Required tool not found: {name}')
    return p

def norm_source(rule_id):
    rule=get_rule(CATALOG,rule_id)
    return f"{source_label(CATALOG,rule)} · {rule['locator']}"

def norm_check(check_id,rule_id,category,label,status,evidence,correction='',mandatory=True,level='automatic'):
    rule=get_rule(CATALOG,rule_id)
    return Check(check_id,category,label,norm_source(rule_id),status,evidence,correction,mandatory,level,rule_id,rule['locator'],rule['normativity'])

def info(pdf):
    out={}
    for line in run([tool('pdfinfo'),str(pdf)]).stdout.splitlines():
        if ':' in line:
            k,v=line.split(':',1); out[k.strip()]=v.strip()
    return out

def fonts(pdf):
    rows=[]
    for line in run([tool('pdffonts'),str(pdf)]).stdout.splitlines()[2:]:
        parts=line.split()
        if len(parts)>=8:
            rows.append({'name':parts[0],'emb':parts[-5],'uni':parts[-3]})
    return rows

def text(pdf):
    with tempfile.NamedTemporaryFile(suffix='.txt',delete=False) as f: p=Path(f.name)
    try:
        run([tool('pdftotext'),'-layout',str(pdf),str(p)])
        return p.read_text(encoding='utf-8',errors='replace')
    finally: p.unlink(missing_ok=True)

def bbox(pdf):
    with tempfile.NamedTemporaryFile(suffix='.html',delete=False) as f: p=Path(f.name)
    try:
        run([tool('pdftotext'),'-bbox-layout',str(pdf),str(p)])
        root=ET.parse(p).getroot()
    finally: p.unlink(missing_ok=True)
    ln=lambda t:t.rsplit('}',1)[-1]
    pages=[]
    for pg in (n for n in root.iter() if ln(n.tag)=='page'):
        words=[]
        for w in (n for n in pg.iter() if ln(n.tag)=='word'):
            words.append((''.join(w.itertext()),float(w.attrib['xMin']),float(w.attrib['yMin']),float(w.attrib['xMax']),float(w.attrib['yMax'])))
        pages.append((float(pg.attrib['width']),float(pg.attrib['height']),words))
    return pages

def norm(s):
    s=unicodedata.normalize('NFKD',s)
    s=''.join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r'\s+',' ',s.upper()).strip()
def compact(s): return re.sub(r'[^a-z0-9]','',norm(s).lower())
def verdict(cs):
    if any(c.mandatory and c.status==FAIL for c in cs): return FAIL
    if any(c.mandatory and c.status==REVIEW for c in cs): return 'REVIEW REQUIRED'
    if any(c.status in (WARN,REVIEW) for c in cs): return 'AUTOMATED CHECKS PASSED WITH WARNINGS'
    return 'AUTOMATED CHECKS PASSED'

def check_layout(pages):
    bad=[i for i,(w,h,_) in enumerate(pages,1) if abs(w-A4[0])>A4_TOLERANCE or abs(h-A4[1])>A4_TOLERANCE]
    cs=[norm_check('layout.a4','page.a4','Layout','Papel A4',PASS if not bad else FAIL,'All pages are A4.' if not bad else f'Pages outside A4: {bad}','Configure A4 paper size for all pages.' if bad else '')]
    out=[]
    for i,(w,h,ws) in enumerate(pages,1):
        for s,x0,y0,x1,y1 in ws:
            s=s.strip()
            if not s: continue
            if re.fullmatch(r'\d+',s) and y0<70: continue
            if x0<LEFT-A4_TOLERANCE or x1>w-RIGHT+3: out.append((i,s[:24],round(x0,1),round(x1,1)))
    cs.append(norm_check('layout.margins','margin.recto','Layout','Margens horizontais do anverso: 3 cm / 2 cm',PASS if not out else FAIL,'No text exceeds the margins.' if not out else f'Examples: {out[:8]}','Move the element inside the text block.' if out else '',level='geometric'))
    return cs

def is_text_fallback(name):
    x=re.sub(r'[^a-z0-9]','',name.lower())
    return ('texgyretermesx' in x or ('texgyretermes' in x and 'math' not in x) or 'texgyreheros' in x)

def check_fonts(fs,profile):
    cs=[]; unemb=[f['name'] for f in fs if f['emb']!='yes']
    cs.append(Check('font.embedded','Typography','All fonts embedded','PDF/A / preservation',PASS if fs and not unemb else FAIL,'All fonts embedded.' if fs and not unemb else f'Not embedded/undetermined: {unemb or "no analyzable font"}','Recompile with all fonts embedded.' if unemb or not fs else ''))
    names=[re.sub(r'^[A-Z]{6}\+','',f['name']) for f in fs]; nn=[re.sub(r'[^a-z0-9]','',n.lower()) for n in names]
    allowed=RULES['font.family.body']['values']['allowed']; allowed_compact=[compact(name) for name in allowed]
    literal=[n for n,x in zip(names,nn) if any(key in x for key in allowed_compact)]
    fallback=[n for n in names if is_text_fallback(n)]
    ok=bool(literal) and not fallback
    st=PASS if ok else (WARN if profile=='portable' else FAIL)
    allowed_label=' or '.join(allowed)
    cs.append(norm_check('font.literal','font.family.body','Typography',f'{allowed_label} literal',st,f'Literal fonts: {literal or "none"}; text fallback: {fallback or "none"}',f'Use strict-font = true with literal {allowed_label}.' if not ok else '',mandatory=profile!='portable',level='typographic'))
    return cs

def check_structure(t):
    u=norm(t); cs=[]
    req=[('cover','Capa','UNIVERSIDADE FEDERAL DO CEARA'),('approval','Folha de aprovação','BANCA EXAMINADORA'),('resumo','Resumo','RESUMO'),('abstract','Abstract','ABSTRACT'),('toc','Sumário','SUMARIO'),('refs','Referências','REFERENCIAS')]
    for k,label,token in req:
        ok=token in u; cs.append(Check('structure.'+k,'Structure',label,'ABNT/UFC',PASS if ok else FAIL,'Element found.' if ok else 'Element not found.',f'Include {label.lower()}.' if not ok else ''))
    summary_source=norm_source('summary.paragraph')
    for k,token in [('keywords','PALAVRAS-CHAVE'),('keywords-en','KEYWORDS')]:
        ok=token in u; cs.append(Check('structure.'+k,'Resumo',token.title(),summary_source,PASS if ok else FAIL,'Field found.' if ok else 'Field missing.',f'Include {token.lower()}.' if not ok else '',normative_rule='summary.paragraph',locator=RULES['summary.paragraph']['locator'],normativity=RULES['summary.paragraph']['normativity']))
    cs.append(norm_check('catalog.optional','deposit.catalog-card','UFC Deposit','Ficha catalográfica visual',NA,'The visual representation is optional.',mandatory=False))
    cs.append(norm_check('approval.signatures','deposit.approval-signatures','UFC Deposit','Folha de aprovação sem assinaturas digitalizadas',REVIEW,'Requires visual inspection.','For repository submission, use the Folha de aprovação without signatures.',mandatory=False,level='manual'))
    cs.append(norm_check('capes','deposit.capes','UFC Deposit','Agradecimento CAPES quando aplicável',REVIEW,'Depends on funding.','Include the required wording when CAPES funding applies.',mandatory=False,level='conditional'))
    return cs

def check_meta(pdf,inf,profile):
    raw=pdf.read_bytes().decode('latin-1',errors='ignore')
    lang=re.search(r'/Lang\s*(?:\(([^)]*)\)|/([^\s/>]+))',raw); lang=(lang.group(1) or lang.group(2)) if lang else ''
    cs=[Check('meta.lang','Metadata','Primary language','WCAG PDF16 / preservation',PASS if lang else WARN,lang or 'missing','Set pt-BR.' if not lang else '',mandatory=False),Check('meta.title','Metadata','PDF title','Repository best practice',PASS if inf.get('Title') else WARN,inf.get('Title') or 'missing','Set the PDF/XMP title.' if not inf.get('Title') else '',mandatory=False),Check('meta.author','Metadata','PDF author','Repository best practice',PASS if inf.get('Author') else WARN,inf.get('Author') or 'missing','Set the PDF/XMP author.' if not inf.get('Author') else '',mandatory=False)]
    tagged=inf.get('Tagged','').lower()=='yes'; acc=profile=='accessibility'
    cs.append(Check('access.tagged','Accessibility','Tagged/structured PDF','PDF/UA / WCAG',PASS if tagged else (FAIL if acc else WARN),f"Tagged: {inf.get('Tagged','unknown')}",'Generate a tagged PDF.' if not tagged else '',mandatory=acc))
    outlines='/Outlines' in raw; cs.append(Check('access.bookmarks','Accessibility','Bookmarks','WCAG PDF2',PASS if outlines else WARN,'Detected.' if outlines else 'Not detected.','Add hierarchical bookmarks.' if not outlines else '',mandatory=False))
    enc=inf.get('Encrypted','').lower(); cs.append(Check('security.encrypted','Integrity','No encryption','Repository submission',PASS if enc.startswith('no') else FAIL,inf.get('Encrypted','unknown'),'Remove password/encryption.' if not enc.startswith('no') else ''))
    meta=run([tool('pdfinfo'),'-meta',str(pdf)],check=False).stdout
    profile_name=RULES['deposit.pdfa']['values']['project_profile']; claim=bool(re.search(r'pdfaid:part[^>]*>\s*2\s*<',meta,re.I) and re.search(r'pdfaid:conformance[^>]*>\s*B\s*<',meta,re.I))
    cs.append(norm_check('pdfa.claim','deposit.pdfa','PDF/A',f'{profile_name} declaration',PASS if claim else WARN,f'XMP declares {profile_name}.' if claim else 'Declaration not detected.',f'Generate {profile_name} metadata.' if not claim else '',mandatory=False))
    return cs

def check_verapdf(pdf,profile):
    exe=shutil.which('verapdf'); required=profile!='portable'; profile_name=RULES['deposit.pdfa']['values']['project_profile']
    if not exe:
        cs=[norm_check('pdfa.deep','deposit.pdfa','PDF/A',f'veraPDF validation {profile_name}',REVIEW,'veraPDF is not installed.','Run Deep mode with veraPDF.',mandatory=required,level='deep')]
        if profile=='accessibility': cs.append(Check('access.pdfua','Accessibility','PDF/UA-1 with veraPDF','PDF/UA-1',REVIEW,'veraPDF is not installed.','Run veraPDF -f ua1.',mandatory=True,level='deep'))
        return cs
    def valid(flavour): return 'isCompliant="true"' in run([exe,'-f',flavour,str(pdf)],check=False).stdout
    ok=valid('2b'); cs=[norm_check('pdfa.deep','deposit.pdfa','PDF/A',f'veraPDF validation {profile_name}',PASS if ok else FAIL,'Compliant.' if ok else 'Failed by veraPDF.','Fix the veraPDF violations.' if not ok else '',mandatory=required,level='deep')]
    if profile=='accessibility':
        ua=valid('ua1'); cs.append(Check('access.pdfua','Accessibility','PDF/UA-1 with veraPDF','PDF/UA-1',PASS if ua else FAIL,'Compliant in automated checks.' if ua else 'Failed.','Fix tagging/structure.',mandatory=True,level='deep'))
    return cs

def render_table(cs): return '\n'.join(f'{c.status:18} | {c.category:16} | {c.rule[:48]:48} | {c.evidence[:70]}' for c in cs)
def main():
    ap=argparse.ArgumentParser(description='Validate an academic UFC/ABNT PDF.'); ap.add_argument('pdf',type=Path); ap.add_argument('--profile',choices=('strict','portable','accessibility'),default='strict'); ap.add_argument('--format',choices=('table','json','markdown'),default='table'); ap.add_argument('--output',type=Path); a=ap.parse_args(); pdf=a.pdf.resolve()
    if not pdf.is_file(): raise SystemExit(f'File not found: {pdf}')
    inf=info(pdf); fs=fonts(pdf); t=text(pdf); pages=bbox(pdf); cs=[Check('pdf.open','Integrity','Readable PDF','Technical prerequisite',PASS,f"{inf.get('Pages','?')} pages; PDF {inf.get('PDF version','?')}.")]; cs+=check_layout(pages)+check_fonts(fs,a.profile)+check_structure(t)+check_meta(pdf,inf,a.profile)+check_verapdf(pdf,a.profile)
    if a.profile=='accessibility': cs += [Check('access.alt','Accessibility','Adequate alternative text','PDF/UA / WCAG',REVIEW,'Quality requires human review.','Review /Alt and decorative artifacts.',mandatory=True,level='manual'),Check('access.order','Accessibility','Logical reading order','PDF/UA / WCAG',REVIEW,'Requires testing with assistive technology.','Review the reading order.',mandatory=True,level='manual')]
    v=verdict(cs); base={'schema_version':CATALOG['schema_version'],'reviewed_at':CATALOG['reviewed_at']}
    if a.format=='json': out=json.dumps({'file':pdf.name,'profile':a.profile,'verdict':v,'normative_catalog':base,'checks':[asdict(c) for c in cs],'mode':'cli-deep-local'},ensure_ascii=False,indent=2)+'\n'
    elif a.format=='markdown':
        esc=lambda x:str(x).replace('|','\\|').replace('\n',' '); lines=['# UFC validation report','',f'File: `{pdf.name}`',f'Profile: `{a.profile}`',f'Verdict: **{v}**',f'Normative base reviewed on: `{CATALOG["reviewed_at"]}`','','| Status | Category | Rule | Source | Evidence | Correction |','|---|---|---|---|---|---|']; lines += [f'| {esc(c.status)} | {esc(c.category)} | {esc(c.rule)} | {esc(c.source)} | {esc(c.evidence)} | {esc(c.correction)} |' for c in cs]; out='\n'.join(lines)+'\n'
    else: out=f'File: {pdf.name}\nProfile: {a.profile}\nVerdict: {v}\nNormative base: {CATALOG["reviewed_at"]}\n\n{render_table(cs)}\n'
    (a.output.write_text(out,encoding='utf-8') if a.output else print(out,end='')); raise SystemExit(1 if v==FAIL else 0)
if __name__=='__main__': main()
