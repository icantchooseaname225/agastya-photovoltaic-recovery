import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

export function ncLoopVoltage({supplyV=5,pullupOhm=10000,contactOhm=0.5,closed=true}={}) {
  if (![supplyV,pullupOhm,contactOhm].every(Number.isFinite) || supplyV<=0 || pullupOhm<=0 || contactOhm<0) {
    throw new RangeError("Use a positive supply and pull-up resistance and non-negative contact resistance.");
  }
  if (!closed) return {inputV:supplyV,currentA:0,interpretation:"open loop: trip, broken wire, or disconnected contact"};
  const current=supplyV/(pullupOhm+contactOhm);
  return {inputV:current*contactOhm,currentA:current,interpretation:"closed NC contact"};
}
export function buildTruthTable() {
  return [
    {state:"healthy NC contact",closed:true,meaning:"normal loop",...ncLoopVoltage({closed:true})},
    {state:"E-stop pressed / auxiliary contact open",closed:false,meaning:"status fault",...ncLoopVoltage({closed:false})},
    {state:"broken/disconnected wire",closed:false,meaning:"fail-high status fault",...ncLoopVoltage({closed:false})},
  ];
}
export function runElectronicsModel(outputDir) {
  fs.mkdirSync(outputDir,{recursive:true});
  const rows=buildTruthTable();
  const header="state,closed,meaning,inputV,currentA,interpretation";
  const q=v=>{const s=String(v);return /[",\r\n]/.test(s)?'"'+s.replaceAll('"','""')+'"':s;};
  const csv=[header,...rows.map(r=>[r.state,r.closed,r.meaning,r.inputV,r.currentA,r.interpretation].map(q).join(","))].join("\n")+"\n";
  fs.writeFileSync(path.join(outputDir,"NC_LOOP_SIMULATION.csv"),csv);
  fs.writeFileSync(path.join(outputDir,"NC_LOOP_SIMULATION.json"),JSON.stringify({
    model:"5 V pull-up through 10 kohm; NC contact to signal ground; contact represented as 0.5 ohm when closed and open circuit otherwise.",
    evidence:"Executed DC circuit-equation model in Node.js and transient netlist in LTspice 26.1.1 batch mode; measured results are recorded separately.",
    ltspiceVerification:"LTSPICE_TRANSIENT_RESULTS.json",
    results:rows,
    limitations:["This is a single-channel status-input model, not a safety relay or safety function.",
      "It cannot detect every possible fault: a short to ground can look like a healthy closed contact.",
      "The example relay must independently interrupt a correctly rated servo supply; software status is not that interruption.",
      "No actual Mega input thresholds, noise immunity, EMC, isolation, relay ratings, wiring length or power rail are qualified."]
  },null,2)+"\n");
  return rows;
}
if (process.argv[1] && import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href) {
  const out=process.argv[2]||path.resolve(path.dirname(fileURLToPath(import.meta.url)),"outputs");
  console.log(JSON.stringify(runElectronicsModel(out),null,2));
}
