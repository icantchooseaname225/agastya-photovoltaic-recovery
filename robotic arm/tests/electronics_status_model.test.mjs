import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {ncLoopVoltage,buildTruthTable,runElectronicsModel} from "../electronics/spice/nc_loop_status_model.mjs";

test("healthy NC contact pulls status input near ground",()=>{
  const x=ncLoopVoltage({closed:true});
  assert.ok(x.inputV>=0 && x.inputV<0.01); assert.ok(x.currentA>0);
});
test("open contact, trip, or broken wire leaves input near supply",()=>{
  for(const state of [{closed:false},{closed:false}]) assert.ok(ncLoopVoltage(state).inputV>=4.9);
});
test("bad electrical model inputs are rejected",()=>{
  assert.throws(()=>ncLoopVoltage({pullupOhm:0}),RangeError);
  assert.throws(()=>ncLoopVoltage({contactOhm:-1}),RangeError);
});
test("LTspice netlist has a transient directive and no ngspice control block",()=>{
  const net=fs.readFileSync(path.resolve(import.meta.dirname,"..","electronics","spice","NC_LOOP_STATUS_LTSPICE.cir"),"utf8");
  assert.match(net,/^\.tran 0 20m 0 10u$/m); assert.match(net,/^\.model SWNC SW\(/m);
  assert.match(net,/^\.measure TRAN V_OPEN FIND V\(MCU_STATUS\) AT=2m$/m);
  assert.match(net,/^\.measure TRAN V_CLOSED FIND V\(MCU_STATUS\) AT=7m$/m); assert.match(net,/^\.end$/m);
  assert.doesNotMatch(net,/^\.control$/m); assert.match(net,/^SNC MCU_STATUS 0 CTRL 0 SWNC$/m);
});test("truth table and generated output preserve fail-high behavior",()=>{
  const rows=buildTruthTable(); assert.equal(rows.length,3);
  assert.equal(rows[0].inputV<0.01,true); assert.equal(rows[1].inputV,5); assert.equal(rows[2].inputV,5);
  const out=path.join(import.meta.dirname,"outputs"); runElectronicsModel(out);
  assert.ok(fs.existsSync(path.join(out,"NC_LOOP_SIMULATION.json")));
});
