import test from "node:test";
import assert from "node:assert/strict";
import {catalogueTotals,evaluatePlant} from "../models/catalogue_cost_model.mjs";

test("education-scale totals reproduce documented catalogue arithmetic",()=>{
  const x=catalogueTotals();
  assert.equal(x.fourServoSubtotalInr,10316);
  assert.equal(x.fourServosPlusMegaInr,14066);
  assert.equal(x.fourServosMegaAndOptionalPwmInr,14315);
});
test("plant economics does not invent ROI when operating inputs are missing",()=>{
  const r=evaluatePlant({installedCapexInr:null,annualPanels:null});
  assert.equal(r.status,"NOT_CALCULABLE"); assert.equal(r.annualNetCashflowInr,null); assert.equal(r.paybackYears,null);
  assert.ok(r.missingInputs.includes("silverBearingRevenuePerPanelInr"));
});
test("complete supplied values compute transparent annual cashflow and payback",()=>{
  const r=evaluatePlant({installedCapexInr:1000,annualPanels:10,serviceRevenuePerPanelInr:200,silverBearingRevenuePerPanelInr:0,
    otherRevenuePerPanelInr:0,reagentPerPanelInr:10,energyPerPanelInr:10,waterPerPanelInr:5,labourAnnualInr:500,
    maintenanceAnnualInr:100,transportAnnualInr:100,disposalAnnualInr:0});
  assert.equal(r.annualNetCashflowInr,1050); assert.ok(Math.abs(r.paybackYears-(1000/1050))<1e-12);
});
