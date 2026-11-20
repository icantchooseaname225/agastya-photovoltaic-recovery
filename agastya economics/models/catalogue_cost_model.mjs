import fs from "node:fs";
import path from "node:path";
import { fileURLToPath,pathToFileURL } from "node:url";

export const catalogueItems = [
  {id:"ACEBOTT-4DOF",description:"ACEBOTT ESP32 4-DOF educational arm kit",unitPriceInr:5019,quantity:1,source:"https://robu.in/product/acebott-esp32-4-dof-robot-arm-kit/",boundary:"Listing title/spec conflict noted in source review; verify contents/specs. Classroom benchmark only."},
  {id:"ROBOKITS-6DOF",description:"Robokits 6-DOF DIY arm kit",unitPriceInr:13600,quantity:1,source:"https://robokits.co.in/robot-kits/robotic-arm-kit/robotic-arm-6-dof-diy-kit-with-usb-servo-controller-and-software",boundary:"Listing says 350 mm reach and 100 g max payload; not process-arm evidence."},
  {id:"HIWONDER-HPS-2027",description:"Hiwonder HPS-2027 servo listing",unitPriceInr:2579,quantity:4,source:"https://robu.in/product-category/hiwonder-servo-motor-and-accessories/",boundary:"Listing label is not used as a verified torque rating; voltage/current/duty data are missing."},
  {id:"ARDUINO-MEGA",description:"Arduino Mega 2560 listing",unitPriceInr:3750,quantity:1,source:"https://robu.in/product-category/classic-family/",boundary:"Controller-price reference only; not a safety controller."},
  {id:"PCA9685-OPTION",description:"PCA9685 16-channel PWM board listing (optional)",unitPriceInr:249,quantity:1,source:"https://robu.in/product-category/servo-motor-driver/",boundary:"PWM signal generation only; does not power servos or provide a safety function."}
];
export function catalogueTotals(items=catalogueItems) {
  const ace=items.find(x=>x.id==="ACEBOTT-4DOF")?.unitPriceInr??null;
  const kit=items.find(x=>x.id==="ROBOKITS-6DOF")?.unitPriceInr??null;
  const servos=items.filter(x=>x.id==="HIWONDER-HPS-2027").reduce((s,x)=>s+x.unitPriceInr*x.quantity,0);
  const mega=items.find(x=>x.id==="ARDUINO-MEGA")?.unitPriceInr??null;
  const pwm=items.find(x=>x.id==="PCA9685-OPTION")?.unitPriceInr??null;
  return {acebottKitInr:ace,robokitsKitInr:kit,fourServoSubtotalInr:servos,megaInr:mega,fourServosPlusMegaInr:servos+mega,fourServosMegaAndOptionalPwmInr:servos+mega+pwm};
}
const required=["installedCapexInr","annualPanels","serviceRevenuePerPanelInr","silverBearingRevenuePerPanelInr","otherRevenuePerPanelInr","reagentPerPanelInr","energyPerPanelInr","waterPerPanelInr","labourAnnualInr","maintenanceAnnualInr","transportAnnualInr","disposalAnnualInr"];
export function evaluatePlant(input) {
  const missing=required.filter(k=>!Number.isFinite(input?.[k]) || input[k]<0 || (k==="annualPanels" && input[k]===0));
  if(missing.length) return {status:"NOT_CALCULABLE",missingInputs:missing,annualNetCashflowInr:null,paybackYears:null};
  const variable=(input.serviceRevenuePerPanelInr+input.silverBearingRevenuePerPanelInr+input.otherRevenuePerPanelInr)-
    (input.reagentPerPanelInr+input.energyPerPanelInr+input.waterPerPanelInr+input.transportAnnualInr/input.annualPanels+input.disposalAnnualInr/input.annualPanels);
  const net=input.annualPanels*variable-input.labourAnnualInr-input.maintenanceAnnualInr;
  return {status:"CALCULATED_FROM_USER_INPUTS",annualNetCashflowInr:net,paybackYears:net>0?input.installedCapexInr/net:null};
}
export function runEconomicScreen(outputDir,templatePath) {
  fs.mkdirSync(outputDir,{recursive:true});
  const totals=catalogueTotals();
  const lineRows=catalogueItems.map(x=>({id:x.id,description:x.description,unit_price_inr:x.unitPriceInr,quantity:x.quantity,extended_price_inr:x.unitPriceInr*x.quantity,source:x.source,boundary:x.boundary}));
  const header=Object.keys(lineRows[0]), q=v=>{const s=String(v);return /[",\r\n]/.test(s)?'"'+s.replaceAll('"','""')+'"':s;};
  fs.writeFileSync(path.join(outputDir,"EDUCATION_SCALE_CATALOGUE_COMPARISON.csv"),[header.join(","),...lineRows.map(r=>header.map(k=>q(r[k])).join(","))].join("\n")+"\n");
  const template={currency:"INR",evidence:"Template only; unknown entries intentionally null.",inputs:{
    installedCapexInr:null,annualPanels:null,serviceRevenuePerPanelInr:null,silverBearingRevenuePerPanelInr:null,otherRevenuePerPanelInr:null,
    reagentPerPanelInr:null,energyPerPanelInr:null,waterPerPanelInr:null,labourAnnualInr:null,maintenanceAnnualInr:null,transportAnnualInr:null,disposalAnnualInr:null
  },requiredEvidence:["written equipment quotes including tax, installation, guarding and commissioning","measured throughput and uptime","measured panel mass and silver-bearing product assay / verified receiver price","measured energy, water, reagent, labour, transport and disposal costs"]};
  fs.writeFileSync(templatePath,JSON.stringify(template,null,2)+"\n");
  const result={priceCheckDate:"2026-11-20",currency:"INR",catalogueTotals:totals,
    excludedCosts:["servo supply and power distribution","hardwired safety relay and rated E-stop devices","fuses, wiring and enclosure","mechanical structure, fixtures and fabrication","delivery, tax, commissioning, guarding and maintenance"],
    processArm:{capexInr:null,costPerPanelInr:null,paybackYears:null,status:"NOT_ESTIMATED: process-arm specifications and measured operating data are absent"},
    plantModel:evaluatePlant(template.inputs),
    conclusion:"Educational catalogue values are bounded comparison points only. They do not price the 2 m process-arm concept. No vendor quote, machine purchase, production revenue, ROI or payback is established."};
  fs.writeFileSync(path.join(outputDir,"ECONOMIC_SCREEN_RESULTS.json"),JSON.stringify(result,null,2)+"\n");
  return result;
}
if(process.argv[1] && import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href){
  const root=path.dirname(fileURLToPath(import.meta.url)), out=process.argv[2]||path.resolve(root,"..","outputs"), template=path.resolve(root,"..","outputs","plant_economics_inputs.template.json");
  console.log(JSON.stringify(runEconomicScreen(out,template),null,2));
}
