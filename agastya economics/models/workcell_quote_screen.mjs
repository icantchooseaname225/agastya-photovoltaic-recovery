import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const ARCHITECTURES = [
  {id:"ARM_PLUS_TOOLING",label:"Arm plus task tooling",categories:["robot_and_controller","process_tooling","panel_support_fixture","safety_guarding","electrical_power_controls","extraction_and_output_handling","installation_commissioning","training","initial_spares"]},
  {id:"ARM_ON_RAIL",label:"Short-reach arm with rail or panel indexer",categories:["arm_and_controller","rail_or_panel_indexer","process_tooling","panel_support_fixture","safety_guarding","electrical_power_controls","extraction_and_output_handling","installation_commissioning","training","initial_spares"]},
  {id:"DEDICATED_FIXTURES",label:"Dedicated mechanisms and fixtures",categories:["dedicated_mechanisms","process_tooling","panel_support_fixture","safety_guarding","electrical_power_controls","extraction_and_output_handling","installation_commissioning","training","initial_spares"]},
];

export function createBlankQuoteTemplate() {
  return {currency:"INR",evidence:"No process-cell quotations have been supplied. All numeric and source fields are intentionally null.",
    scopeRule:"Enter vendor-confirmed line totals and a traceable written quote reference. Explicitly record whether tax and delivery/installation/commissioning are included. Do not enter catalogue guesses as quotes.",
    architectures:ARCHITECTURES.map(a=>({id:a.id,label:a.label,capitalItems:a.categories.map(category=>({category,lineTotalInr:null,supplier:null,quoteReference:null,quoteDate:null,taxIncluded:null,deliveryInstallationCommissioningIncluded:null,scopeNotes:null}))}))};
}

export function evaluateWorkcellQuotes(template) {
  const architectures=(template.architectures||[]).map(a=>{
    const missing=[];
    for (const item of a.capitalItems||[]) {
      if (!Number.isFinite(item.lineTotalInr) || item.lineTotalInr<0) missing.push(`${item.category}: line total`);
      if (!item.supplier) missing.push(`${item.category}: supplier`);
      if (!item.quoteReference) missing.push(`${item.category}: quote reference`);
      if (!item.quoteDate) missing.push(`${item.category}: quote date`);
      if (typeof item.taxIncluded!=="boolean") missing.push(`${item.category}: tax inclusion`);
      if (typeof item.deliveryInstallationCommissioningIncluded!=="boolean") missing.push(`${item.category}: delivery/installation scope`);
    }
    const complete=missing.length===0 && (a.capitalItems||[]).length>0;
    return {id:a.id,label:a.label,status:complete?"QUOTE_INPUTS_COMPLETE":"NOT_COMPARABLE_MISSING_QUOTE_DATA",
      installedCapexInr:complete?a.capitalItems.reduce((sum,item)=>sum+item.lineTotalInr,0):null,
      scopeExclusions:complete?a.capitalItems.filter(item=>!item.taxIncluded||!item.deliveryInstallationCommissioningIncluded).map(item=>({category:item.category,taxIncluded:item.taxIncluded,deliveryInstallationCommissioningIncluded:item.deliveryInstallationCommissioningIncluded,notes:item.scopeNotes})):[],
      missingInputs:missing};
  });
  return {currency:template.currency||"INR",evidence:template.evidence,architectures,
    comparisonStatus:architectures.length>0&&architectures.every(a=>a.status==="QUOTE_INPUTS_COMPLETE")?"COMPARABLE_QUOTED_CAPEX":"INCOMPLETE_NO_ROI_OR_COST_PER_PANEL",
    limits:["This comparison only totals quoted capital line items after every required source and scope field is complete.","It does not estimate annual throughput, operating cost, process yield, revenue, cost per panel or payback.","Quotes need a qualified design basis and comparable scope before purchase or architecture selection."]};
}

export function runWorkcellQuoteScreen(root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..")) {
  const outputs=path.join(root,"outputs"), inputs=path.join(root,"inputs"), inputFile=path.join(inputs,"workcell_quotes.template.json");
  fs.mkdirSync(outputs,{recursive:true}); fs.mkdirSync(inputs,{recursive:true});
  if (!fs.existsSync(inputFile)) fs.writeFileSync(inputFile,JSON.stringify(createBlankQuoteTemplate(),null,2)+"\n");
  const template=JSON.parse(fs.readFileSync(inputFile,"utf8"));
  const result=evaluateWorkcellQuotes(template);
  fs.writeFileSync(path.join(outputs,"WORKCELL_QUOTE_COMPARISON.json"),JSON.stringify(result,null,2)+"\n");
  return result;
}

if (process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href) console.log(JSON.stringify(runWorkcellQuoteScreen(),null,2));
