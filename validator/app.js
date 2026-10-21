import * as pdfjsLib from "./vendor/pdfjs/pdf.mjs";
import {normativeCatalog,normativeRules,normativeSources} from "./normative-catalog.js";
import {documentApplicability} from "./document-applicability.js";
import {assertLocaleCoverage, setLocale, getLocale, uiText} from "./ui-locales.js";
import {csvRows} from "./csv-export.js";
pdfjsLib.GlobalWorkerOptions.workerSrc="./vendor/pdfjs/pdf.worker.mjs";

const PASS="PASS",FAIL="FAIL",WARN="WARNING",REVIEW="MANUAL REVIEW",NA="NOT APPLICABLE";
const MM=72/25.4,pageRule=normativeRules["page.a4"],rectoRule=normativeRules["margin.recto"],versoRule=normativeRules["margin.verso"];
const A4=[pageRule.values.width_mm*MM,pageRule.values.height_mm*MM],TOL=pageRule.values.tolerance_pt??1.8;
const $=s=>document.querySelector(s); let report=null;
// Presentation-only translations never modify canonical report data.
const displayStatus=s=>uiText("status"+s);
const displayVerdict=s=>uiText("verdict"+s);

function structureObservation(modality,found){
 if(modality==="required")return {status:found?PASS:FAIL,mandatory:true,level:"automatic-partial",evidence:found?"Token detected in PDF text; placement and semantics unverified.":"Required token not detected in PDF text."};
 if(modality==="optional")return {status:found?REVIEW:NA,mandatory:false,level:"conditional",evidence:found?"Optional token detected; review applicability and placement.":"Optional element absent; no failure."};
 if(modality==="not-applicable")return {status:NA,mandatory:false,level:"conditional",evidence:"Not required for this document type; presence is not prohibited."};
 throw new Error("Unsupported document applicability: "+modality);
}
const ck=(id,category,rule,source,status,evidence,correction="",mandatory=true,level="automatic",normativeRule="",locator="",normativity="")=>({id,category,rule,source,status,evidence,correction,mandatory,level,normativeRule,locator,normativity});
const norm=s=>String(s||"").normalize("NFKD").replace(/[\u0300-\u036f]/g,"").replace(/\s+/g," ").trim().toUpperCase();
const compact=s=>norm(s).replace(/[^A-Z0-9]/g,"");
const sourceLabel=ruleId=>normativeRules[ruleId].sources.map(id=>normativeSources[id].title).join(" / ");
const normSource=ruleId=>`${sourceLabel(ruleId)} · ${normativeRules[ruleId].locator}`;
const nck=(id,ruleId,category,label,status,evidence,correction="",mandatory=true,level="automatic")=>{const r=normativeRules[ruleId];return ck(id,category,label,normSource(ruleId),status,evidence,correction,mandatory,level,ruleId,r.locator,r.normativity)};
const isTextFallback=s=>{const x=compact(s);return x.includes("TEXGYRETERMESX")||(x.includes("TEXGYRETERMES")&&!x.includes("MATH"))||x.includes("TEXGYREHEROS")};
const verdict=cs=>cs.some(c=>c.mandatory&&c.status===FAIL)?FAIL:cs.some(c=>c.mandatory&&c.status===REVIEW)?"REVIEW REQUIRED":cs.some(c=>[WARN,REVIEW].includes(c.status))?"AUTOMATED CHECKS PASSED WITH WARNINGS":"AUTOMATED CHECKS PASSED";
const CHECK_ID_ALIASES={"font.family":"font.literal","font.embedding":"font.embedded"};
const reportCheck=c=>({id:CHECK_ID_ALIASES[c.id]??c.id,category:c.category,rule:c.rule,source:c.source,status:c.status,evidence:c.evidence,correction:c.correction,mandatory:c.mandatory,level:c.level,normative_rule:c.normativeRule,locator:c.locator,normativity:c.normativity});

function save(name,data,type){const b=new Blob([data],{type}),u=URL.createObjectURL(b),a=document.createElement("a");a.href=u;a.download=name;a.click();URL.revokeObjectURL(u)}
function renderNormativeBase(){
 $("#norm-reviewed").textContent=normativeCatalog.reviewed_at;
 $("#norm-stats").textContent=uiText("rulesStats",normativeCatalog.rules.length,normativeCatalog.sources.length);
 const list=$("#norm-sources");list.replaceChildren();
 for(const source of normativeCatalog.sources){const li=document.createElement("li"),a=document.createElement(source.url?"a":"span");a.textContent=`${source.title} — ${source.status}`;if(source.url){a.href=source.url;a.target="_blank";a.rel="noopener"}li.append(a);list.append(li)}
}
// Presentation-only filtering. Canonical verdicts, full exports and the
// complete immutable report.checks array always retain all evaluated rules.
function checkVisible(c,mode){
 if(mode==="all")return true;
 if(mode==="attention")return [FAIL,WARN,REVIEW].includes(c.status);
 if(mode==="failures")return c.status===FAIL;
 if(mode==="manual")return c.status===REVIEW;
 throw new Error("Unknown Web/Lite report filter: "+mode);
}
function filterReport(){
 if(!report)return;
 const mode=$("#report-filter").value,rows=[...$("#report-body").children];
 if(rows.length!==report.checks.length)throw new Error("Visible rows differ from canonical report");
 let shown=0;
 rows.forEach((row,i)=>{const visible=checkVisible(report.checks[i],mode);row.hidden=!visible;if(visible)shown++});
 $("#filter-count").textContent=uiText("showing",shown,report.checks.length);
}
function render(r){
 $("#summary").classList.remove("hidden");$("#report-section").classList.remove("hidden");$("#verdict").textContent=displayVerdict(r.verdict);$("#file-name").textContent=r.file;$("#page-count").textContent=r.pages;
 const body=$("#report-body");body.replaceChildren();for(const c of r.checks){const tr=document.createElement("tr");for(const [i,v] of [displayStatus(c.status),c.category,c.rule,c.source,c.evidence,c.correction].entries()){const td=document.createElement("td");td.textContent=v;if(i===0)td.className=c.status===PASS?"status-pass":c.status===FAIL?"status-fail":c.status===WARN?"status-warn":"status-review";tr.append(td)}body.append(tr)}
 $("#counts").textContent=[PASS,FAIL,WARN,REVIEW,NA].map(s=>`${displayStatus(s)}: ${r.checks.filter(c=>c.status===s).length}`).join(" · ");["#export-json","#export-csv","#print-report"].forEach(s=>$(s).disabled=false);
  $("#report-filter").disabled=false;$("#report-filter").value="all";filterReport();
}

export async function analyze(file,profile,documentType="undergraduate-capstone",printMode="single-sided"){
 if(!["single-sided","double-sided"].includes(printMode))throw new Error("Unsupported print mode: "+printMode);
 const documentContract=documentApplicability.document_types[documentType];
 if(!documentContract)throw new Error("Unsupported document type: "+documentType);
 const data=new Uint8Array(await file.arrayBuffer()),pdf=await pdfjsLib.getDocument({data}).promise,meta=await pdf.getMetadata(),outline=await pdf.getOutline(),js=await pdf.getJSActions().catch(()=>null);
 const pages=[],families=new Set();let tagged=false;
 for(let n=1;n<=pdf.numPages;n++){const p=await pdf.getPage(n),vp=p.getViewport({scale:1}),tc=await p.getTextContent(),st=await p.getStructTree().catch(()=>null);if(st)tagged=true;for(const it of tc.items){const f=tc.styles?.[it.fontName]?.fontFamily;if(f)families.add(f)}pages.push({n,w:vp.width,h:vp.height,items:tc.items,text:tc.items.map(i=>i.str).join(" ").replace(/\s+/g," ")})}
 const cs=[ck("pdf.open","Integrity","Readable PDF","Technical prerequisite",PASS,`${pdf.numPages} pages processed locally.`)];
 const bad=pages.filter(p=>Math.abs(p.w-A4[0])>TOL||Math.abs(p.h-A4[1])>TOL).map(p=>p.n);cs.push(nck("layout.a4","page.a4","Layout","Papel A4",bad.length?FAIL:PASS,bad.length?`Pages outside A4: ${bad.join(", ")}`:"All pages are A4.",bad.length?"Configure A4 paper size for all pages.":""));
 const out=[];for(const p of pages){
  const verso=printMode==="double-sided"&&p.n%2===0,values=verso?versoRule.values:rectoRule.values;
  const left=values.left_mm*MM,right=values.right_mm*MM;
  for(const item of p.items){
   const word=item.str?.trim();if(!word)continue;
   const x=item.transform[4],x1=x+(item.width||0),y=item.transform[5];
   if(/^\d+$/.test(word)&&y>p.h-75)continue;
   if(x<left-TOL||x1>p.w-right+3)out.push([p.n,verso?"verso":"recto",word.slice(0,20),x.toFixed(1),x1.toFixed(1)]);
  }
 }
 const marginLabel=printMode==="double-sided"?"Margens horizontais: anverso 3 cm / 2 cm; verso 2 cm / 3 cm":"Margens horizontais: anverso 3 cm / 2 cm";
 const marginSource=printMode==="double-sided"?normSource("margin.recto")+" / "+normSource("margin.verso"):normSource("margin.recto");
 cs.push(ck("layout.margins","Layout",marginLabel,marginSource,out.length?FAIL:PASS,out.length?`Mode ${printMode}; examples: ${JSON.stringify(out.slice(0,8))}`:`Mode ${printMode}; no text exceeds the page-specific horizontal margins.`,out.length?"Move the element inside the page-specific text block.":"",true,"geometric","margin.recto",rectoRule.locator,rectoRule.normativity));
 const fam=[...families],fn=fam.map(compact),allowed=normativeRules["font.family.body"].values.allowed,keys=allowed.map(compact),lit=fam.filter((_,i)=>keys.some(k=>fn[i].includes(k))),fb=fam.filter(isTextFallback);let fs=lit.length&&!fb.length?PASS:fb.length&&!lit.length?(profile==="portable"?WARN:FAIL):REVIEW;const fontLabel=allowed.join(" or ");cs.push(nck("font.family","font.family.body","Typography",`${fontLabel} literal`,fs,`Literal fonts: ${lit.join(", ")||"none"}; text fallback: ${fb.join(", ")||"none"}.`,fs===PASS?"":`Use strict-font = true with ${fontLabel} and confirm in Deep/CLI mode.`,profile!=="portable","heuristic"));cs.push(ck("font.embedding","Typography","All fonts embedded","PDF/A / preservation",REVIEW,"Web/Lite does not certify that all fonts are embedded.","Run Deep/CLI mode.",profile!=="portable","deep"));
 const u=norm(pages.map(p=>p.text).join("\n")),req=[["cover","Capa","UNIVERSIDADE FEDERAL DO CEARA"],["approval","Folha de aprovação","BANCA EXAMINADORA"],["resumo","Resumo","RESUMO"],["abstract","Abstract","ABSTRACT"],["toc","Sumário","SUMARIO"],["refs","Referências","REFERENCIAS"],["keywords","Palavras-chave","PALAVRAS-CHAVE"],["keywords-en","Keywords","KEYWORDS"]];
 for(const [id,label,token] of req){
  const found=u.includes(token),mode=documentContract.checks[id],observation=structureObservation(mode,found);
  const isSummary=id==="keywords"||id==="keywords-en",r=isSummary?normativeRules["summary.paragraph"]:null;
  cs.push(ck(`structure.${id}`,isSummary?"Resumo":"Structure",label,isSummary?normSource("summary.paragraph"):documentContract.authority,observation.status,observation.evidence,observation.status===FAIL?`Include ${label.toLowerCase()}.`:"",observation.mandatory,observation.level,isSummary?"summary.paragraph":"",r?.locator??"",r?.normativity??""));
 }
 const inf=meta.info||{},title=inf.Title||meta.metadata?.get?.("dc:title")||"",author=inf.Author||meta.metadata?.get?.("dc:creator")||"",lang=inf.Language||meta.metadata?.get?.("dc:language")||"";cs.push(ck("meta.lang","Metadata","Primary language","WCAG / preservation",lang?PASS:WARN,lang||"Not exposed by PDF.js.",lang?"":"Set pt-BR.",false));cs.push(ck("meta.title","Metadata","PDF title","Repository best practice",title?PASS:WARN,title||"Missing.",title?"":"Set the PDF/XMP title.",false));cs.push(ck("meta.author","Metadata","PDF author","Repository best practice",author?PASS:WARN,author||"Missing.",author?"":"Set the PDF/XMP author.",false));
 const acc=profile==="accessibility";cs.push(ck("access.tagged","Accessibility","Tagged/structured PDF","PDF/UA / WCAG",tagged?PASS:(acc?FAIL:WARN),tagged?"Structure tree detected.":"Structure tree not detected.",tagged?"":"Generate a tagged PDF.",acc));cs.push(ck("access.bookmarks","Accessibility","Bookmarks","WCAG PDF2",outline?.length?PASS:WARN,outline?.length?`${outline.length} top-level entries.`:"Not detected.",outline?.length?"":"Add bookmarks.",false));cs.push(ck("security.javascript","Integrity","No embedded JavaScript","Preservation",js&&Object.keys(js).length?WARN:PASS,js&&Object.keys(js).length?"JavaScript actions detected.":"No JavaScript actions detected.","",false));
 const pdfa=normativeRules["deposit.pdfa"].values.project_profile;cs.push(nck("pdfa.deep","deposit.pdfa","PDF/A",`Structural validation ${pdfa}`,REVIEW,"Web/Lite does not replace full ISO validation.",`Run CLI/Deep with veraPDF -f 2b.`,profile!=="portable","deep"));cs.push(nck("catalog.optional","deposit.catalog-card","UFC Deposit","Ficha catalográfica visual",NA,"Visual representation is optional.","",false));cs.push(nck("approval.signatures","deposit.approval-signatures","UFC Deposit","Folha de aprovação sem assinaturas digitalizadas",REVIEW,"Requires visual inspection.","For repository submission, use the Folha de aprovação without signatures.",false,"manual"));cs.push(nck("capes","deposit.capes","UFC Deposit","Agradecimento CAPES quando aplicável",REVIEW,"Depends on funding.","Include the required wording when applicable.",false,"conditional"));
 if(acc){cs.push(ck("access.alt","Accessibility","Adequate alternative text","PDF/UA / WCAG",REVIEW,"Quality requires human review.","Review /Alt and decorative artifacts.",true,"manual"));cs.push(ck("access.order","Accessibility","Logical reading order","PDF/UA / WCAG",REVIEW,"Requires testing with assistive technology.","Review the reading order.",true,"manual"))}
 const reportChecks=cs.map(reportCheck);return {file:file.name,pages:pdf.numPages,profile,document_type:documentType,print_mode:printMode,verdict:verdict(cs),normative_catalog:{schema_version:normativeCatalog.schema_version,reviewed_at:normativeCatalog.reviewed_at},checks:reportChecks,mode:"web-lite-local",generated_at:new Date().toISOString()};
}

export function getLastReport(){return report}
export {setLocale, getLocale, assertLocaleCoverage};

assertLocaleCoverage();
setLocale("pt-BR");
$("#ui-locale").addEventListener("change",event=>{setLocale(event.target.value);renderNormativeBase();if(report)render(report)});
renderNormativeBase();
$("#report-filter").addEventListener("change",filterReport);
$("#analyze").addEventListener("click",async()=>{const f=$("#pdf-file").files?.[0];if(!f)return alert(uiText("selectFile"));const b=$("#analyze");b.disabled=true;b.textContent=uiText("validating");try{report=await analyze(f,$("#profile").value,$("#document-type").value,$("#print-mode").value);render(report)}catch(e){console.error(e);alert(uiText("validationFailed",e.message||e))}finally{b.disabled=false;b.textContent=uiText("analyze")}});
$("#export-json").addEventListener("click",()=>report&&save("ufc-validation-report.json",JSON.stringify(report,null,2),"application/json;charset=utf-8"));
$("#export-csv").addEventListener("click",()=>{if(!report)return;const h=["Status","Category","Rule","Source","Evidence","Correction","Level","Mandatory","Normative rule","Locator","Normativity"],rows=report.checks.map(c=>[c.status,c.category,c.rule,c.source,c.evidence,c.correction,c.level,c.mandatory?"yes":"no",c.normative_rule,c.locator,c.normativity]),data=csvRows([h,...rows]);save("ufc-validation-report.csv",`\ufeff${data}`,"text/csv;charset=utf-8")});
$("#print-report").addEventListener("click",()=>window.print());
