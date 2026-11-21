import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";

test("recorded LTspice transient points agree with open and closed status states",()=>{
  const file=path.resolve(import.meta.dirname,"..","electronics","spice","outputs","LTSPICE_TRANSIENT_RESULTS.json");
  const result=JSON.parse(fs.readFileSync(file,"utf8"));
  assert.equal(result.tool,"LTspice 26.1.1 for Windows");
  assert.ok(result.measurements.find(x=>x.condition==="Open loop at 2 ms").voltageV>4.99);
  assert.ok(result.measurements.find(x=>x.condition==="Closed loop at 7 ms").voltageV<0.01);
  assert.match(result.interpretation,/not a safety circuit validation/);
});
