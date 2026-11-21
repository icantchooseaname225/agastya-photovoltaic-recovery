import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { forwardPlanar,inversePlanar,payloadMoments,staticGravityMoments,runModel } from "../simulations/robotic_arm_kinematics.mjs";

test("both inverse branches close at a representative reachable point",()=>{
  const target={r:1500,z:-700}, solutions=inversePlanar(target.r,target.z);
  assert.equal(solutions.length,2);
  for(const q of solutions){const p=forwardPlanar(q.q1,q.q2);assert.ok(Math.hypot(p.r-target.r,p.z-target.z)<1e-8);}
});
test("annulus rejects points outside and includes both boundaries",()=>{
  assert.equal(inversePlanar(0,199.9).length,0); assert.equal(inversePlanar(0,200).length,2);
  assert.equal(inversePlanar(2000,0).length,2); assert.equal(inversePlanar(2000.1,0).length,0);
});
test("payload-only moments equal m*g*r and invalid inputs fail",()=>{
  const m=payloadMoments(1,2); assert.ok(Math.abs(m.shoulderMomentNm-19.6133)<1e-8);
  assert.ok(Math.abs(m.elbowMomentNmAtFullExtension-8.825985)<1e-8); assert.throws(()=>payloadMoments(-1,1),RangeError);
});
test("horizontal gravity moments include link, tool and payload mass",()=>{
  const x=staticGravityMoments({upperLinkMassKg:2,forearmMassKg:1,toolMassKg:0.5,payloadMassKg:1});
  assert.ok(Math.abs(x.shoulderNm-9.80665*(2*0.55+1*1.55+1.5*2))<1e-9);
  assert.ok(Math.abs(x.elbowNm-9.80665*(1*0.45+1.5*0.9))<1e-9);
  assert.throws(()=>staticGravityMoments({upperLinkMassKg:-1,forearmMassKg:0,toolMassKg:0,payloadMassKg:0}),RangeError);
});
test("all 71 illustrative perimeter points get IK closure and outputs",()=>{
  const root=path.resolve(import.meta.dirname,"..",".."), input=path.join(root,"robotic arm","simulations","inputs","perimeter_task_points.csv");
  const out=path.join(root,"robotic arm","simulations","outputs"), result=runModel(input,out);
  assert.equal(result.inputs.taskPointCount,71); assert.equal(result.results.reachableTaskPoints,71);
  assert.equal(fs.readFileSync(path.join(out,"IK_TASK_POINT_RESULTS.csv"),"utf8").trim().split(/\r?\n/).length,72);
  assert.ok(fs.existsSync(path.join(out,"IK_WORKSPACE_SCREEN.svg")));
  assert.equal(result.staticGravityMomentSensitivity.scenarioCount,625);
  assert.ok(result.selectedSolutionJointEnvelopeDegrees.shoulder_pitch_deg.spanDeg>0);
  assert.equal(fs.readFileSync(path.join(out,"STATIC_GRAVITY_MOMENT_SENSITIVITY.csv"),"utf8").trim().split(/\r?\n/).length,626);
});
