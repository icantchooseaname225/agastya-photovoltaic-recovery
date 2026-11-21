import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {createBlankQuoteTemplate,evaluateWorkcellQuotes,runWorkcellQuoteScreen} from "../models/workcell_quote_screen.mjs";

test("blank workcell quote template refuses an invented CAPEX comparison",()=>{
  const result=evaluateWorkcellQuotes(createBlankQuoteTemplate());
  assert.equal(result.comparisonStatus,"INCOMPLETE_NO_ROI_OR_COST_PER_PANEL");
  assert.equal(result.architectures.length,3);
  assert.ok(result.architectures.every(a=>a.installedCapexInr===null&&a.status==="NOT_COMPARABLE_MISSING_QUOTE_DATA"));
});

test("complete quoted capital lines total only after source and scope fields are filled",()=>{
  const template=createBlankQuoteTemplate(), a=template.architectures[0];
  a.capitalItems=a.capitalItems.map((item,i)=>({...item,lineTotalInr:1000+i*100,supplier:"Example supplier",quoteReference:`Q-${i}`,quoteDate:"2026-11-21",taxIncluded:i!==0,deliveryInstallationCommissioningIncluded:true,scopeNotes:"Synthetic test input only"}));
  const result=evaluateWorkcellQuotes(template), row=result.architectures[0];
  assert.equal(row.status,"QUOTE_INPUTS_COMPLETE");
  assert.equal(row.installedCapexInr,a.capitalItems.reduce((sum,item)=>sum+item.lineTotalInr,0));
  assert.equal(row.scopeExclusions.length,1);
  assert.equal(result.comparisonStatus,"INCOMPLETE_NO_ROI_OR_COST_PER_PANEL");
});

test("quote-screen CLI preserves and evaluates a populated template",()=>{
  const root=fs.mkdtempSync(path.join(os.tmpdir(),"agastya-quote-screen-"));
  try {
    const template=createBlankQuoteTemplate(), a=template.architectures[0];
    a.capitalItems=a.capitalItems.map((item,i)=>({...item,lineTotalInr:500+i,supplier:"Test supplier",quoteReference:`T-${i}`,quoteDate:"2026-11-21",taxIncluded:true,deliveryInstallationCommissioningIncluded:true,scopeNotes:"Synthetic test input"}));
    const input=path.join(root,"inputs","workcell_quotes.template.json"); fs.mkdirSync(path.dirname(input),{recursive:true}); fs.writeFileSync(input,JSON.stringify(template));
    const result=runWorkcellQuoteScreen(root), preserved=JSON.parse(fs.readFileSync(input,"utf8"));
    assert.equal(result.architectures[0].status,"QUOTE_INPUTS_COMPLETE");
    assert.equal(result.architectures[0].installedCapexInr,a.capitalItems.reduce((s,x)=>s+x.lineTotalInr,0));
    assert.equal(preserved.architectures[0].capitalItems[0].supplier,"Test supplier");
  } finally { fs.rmSync(root,{recursive:true,force:true}); }
});
