import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

export const MODEL = Object.freeze({ link1Mm:1100, link2Mm:900, shoulderZMm:730, baseXmm:0, baseYmm:-867, panelZmm:0, gravityMps2:9.80665 });

function readCsv(file) {
  const lines = fs.readFileSync(file, "utf8").trim().split(/\r?\n/);
  const headers = lines.shift().split(",");
  return lines.map(line => Object.fromEntries(line.split(",").map((v,i) => [headers[i],v])));
}
function writeCsv(file, rows) {
  if (!rows.length) throw new Error("No rows to write: " + file);
  const headers = Object.keys(rows[0]);
  const q = v => { const s=String(v ?? ""); return /[",\r\n]/.test(s) ? '"' + s.replaceAll('"','""') + '"' : s; };
  fs.writeFileSync(file, [headers.join(","), ...rows.map(r=>headers.map(h=>q(r[h])).join(","))].join("\n") + "\n");
}
export function forwardPlanar(q1,q2,l1=MODEL.link1Mm,l2=MODEL.link2Mm) {
  return {r:l1*Math.cos(q1)+l2*Math.cos(q1+q2), z:l1*Math.sin(q1)+l2*Math.sin(q1+q2)};
}
export function inversePlanar(r,z,l1=MODEL.link1Mm,l2=MODEL.link2Mm) {
  if (![r,z,l1,l2].every(Number.isFinite) || l1<=0 || l2<=0) throw new TypeError("Coordinates and positive link lengths must be finite.");
  const d=Math.hypot(r,z), min=Math.abs(l1-l2), max=l1+l2;
  if (d<min-1e-9 || d>max+1e-9) return [];
  const c=Math.max(-1,Math.min(1,(d*d-l1*l1-l2*l2)/(2*l1*l2))), a=Math.acos(c);
  return [a,-a].map(q2=>({q1:Math.atan2(z,r)-Math.atan2(l2*Math.sin(q2),l1+l2*Math.cos(q2)),q2}));
}
export function payloadMoments(massKg, radiusM, forearmM=0.9) {
  if (![massKg,radiusM,forearmM].every(Number.isFinite) || massKg<0 || radiusM<0 || forearmM<0) throw new RangeError("Mass and moment arms must be finite and non-negative.");
  const force=massKg*MODEL.gravityMps2;
  return {payloadForceN:force,shoulderMomentNm:force*radiusM,elbowMomentNmAtFullExtension:force*forearmM};
}
export function renderWorkspaceSvg(rows,file) {
  const w=1080,h=700,s=0.24,ox=250,oy=365, sx=r=>ox+r*s, sy=z=>oy-z*s;
  const min=Math.abs(MODEL.link1Mm-MODEL.link2Mm), max=MODEL.link1Mm+MODEL.link2Mm;
  const out=['<svg xmlns="http://www.w3.org/2000/svg" width="'+w+'" height="'+h+'" viewBox="0 0 '+w+' '+h+'">',
    '<rect width="100%" height="100%" fill="white"/>',
    '<text x="36" y="42" font-family="Arial" font-size="24" font-weight="bold">Arm side-plane inverse-kinematics screen</text>',
    '<text x="36" y="70" font-family="Arial" font-size="14" fill="#444">Links: 1100 + 900 mm; shoulder z=730 mm; target plane z=0 mm</text>',
    '<circle cx="'+sx(0)+'" cy="'+sy(0)+'" r="'+(max*s)+'" fill="none" stroke="#90a4ae" stroke-dasharray="7 6" stroke-width="2"/>',
    '<line x1="36" y1="'+sy(0)+'" x2="1030" y2="'+sy(0)+'" stroke="#888"/>',
    '<circle cx="'+sx(0)+'" cy="'+sy(0)+'" r="7" fill="#d32f2f"/>',
    '<text x="'+(sx(0)+10)+'" y="'+(sy(0)-12)+'" font-family="Arial" font-size="13">shoulder</text>'];
  for (const row of rows) if (row.ik_reachable==="true") {
    const radius=Number(row.shoulder_to_target_mm), z=MODEL.shoulderZMm;
    out.push('<circle cx="'+sx(radius).toFixed(1)+'" cy="'+sy(-z).toFixed(1)+'" r="3" fill="#1976d2"><title>'+row.task_point_id+'</title></circle>');
  }
  out.push('<text x="36" y="650" font-family="Arial" font-size="13" fill="#444">Points collapse to radial side-plane reach. Collision, limits and tool approach are excluded.</text></svg>');
  fs.writeFileSync(file,out.join("\n"));
}
export function runModel(inputFile,outDir) {
  fs.mkdirSync(outDir,{recursive:true});
  const points=readCsv(inputFile);
  const rows=points.map(p=>{
    const x=Number(p.x_mm), y=Number(p.y_mm), yaw=Math.atan2(y-MODEL.baseYmm,x-MODEL.baseXmm);
    const radial=Math.hypot(x-MODEL.baseXmm,y-MODEL.baseYmm), dz=MODEL.panelZmm-MODEL.shoulderZMm, d=Math.hypot(radial,dz);
    const sols=inversePlanar(radial,dz);
    if (!sols.length) return {task_point_id:p.task_point_id,edge:p.edge,x_mm:x,y_mm:y,radial_mm:+radial.toFixed(3),shoulder_to_target_mm:+d.toFixed(3),ik_reachable:false,yaw_deg:"",shoulder_pitch_deg:"",elbow_pitch_deg:"",wrist_compensation_deg:"",fk_error_mm:""};
    sols.sort((a,b)=>(Math.abs(a.q1)+Math.abs(a.q2))-(Math.abs(b.q1)+Math.abs(b.q2)));
    const q=sols[0], wrist=-(q.q1+q.q2), fk=forwardPlanar(q.q1,q.q2);
    return {task_point_id:p.task_point_id,edge:p.edge,x_mm:x,y_mm:y,radial_mm:+radial.toFixed(3),shoulder_to_target_mm:+d.toFixed(3),ik_reachable:true,
      yaw_deg:+(yaw*180/Math.PI).toFixed(4),shoulder_pitch_deg:+(q.q1*180/Math.PI).toFixed(4),elbow_pitch_deg:+(q.q2*180/Math.PI).toFixed(4),
      wrist_compensation_deg:+(wrist*180/Math.PI).toFixed(4),fk_error_mm:+Math.hypot(fk.r-radial,fk.z-dz).toExponential(4)};
  });
  writeCsv(path.join(outDir,"IK_TASK_POINT_RESULTS.csv"),rows);
  const good=rows.filter(r=>r.ik_reachable===true);
  const summary={runId:"S2-3D-PLANAR-IK-2026-11-20-01",evidence:"Simulated from stated geometry; not validated against a physical robot.",
    software:"Node.js "+process.version+"; built-in modules only",
    model:{architecture:"base yaw plus shoulder, elbow and wrist pitch",linkLengthsMm:[1100,900],baseXYmm:[0,-867],shoulderZmm:730,targetPlaneZmm:0,
      reachableAnnulusMm:[200,2000],branchSelection:"minimum |shoulder pitch| + |elbow pitch|; no joint stops"},
    inputs:{taskPointCount:rows.length},results:{reachableTaskPoints:good.length,totalTaskPoints:rows.length,coveragePercent:rows.length?+(100*good.length/rows.length).toFixed(2):0,
      maxShoulderToTargetMm:Math.max(...rows.map(r=>r.shoulder_to_target_mm)),maxForwardKinematicsClosureErrorMm:good.length?Math.max(...good.map(r=>Number(r.fk_error_mm))):null},
    limitations:["The 71 points represent an illustrative 2278 x 1134 mm panel and 300 mm standoff, not measured feed.",
      "Task points are projected into a radial vertical plane and base yaw is solved separately.",
      "No collision, joint limits, actuator curves, deflection, backlash, repeatability, tool pose, speed or acceleration are included.",
      "Payload torque excludes links, wrist, tool, acceleration, friction, duty and design factors.","This is not a robot selection or safe motion plan."]};
  fs.writeFileSync(path.join(outDir,"IK_SUMMARY.json"),JSON.stringify(summary,null,2)+"\n");
  const torque=[];
  for (const mass of [0.5,1,2,5]) for (const reach of [0.5,1,1.5,2]) {
    const m=payloadMoments(mass,reach);
    torque.push({payload_kg:mass,shoulder_radius_m:reach,payload_force_N:+m.payloadForceN.toFixed(4),shoulder_payload_only_Nm:+m.shoulderMomentNm.toFixed(4),elbow_payload_only_at_full_extension_Nm:+m.elbowMomentNmAtFullExtension.toFixed(4)});
  }
  writeCsv(path.join(outDir,"PAYLOAD_ONLY_MOMENT_SWEEP.csv"),torque);
  renderWorkspaceSvg(rows,path.join(outDir,"IK_WORKSPACE_SCREEN.svg"));
  const report="# Stage 2 inverse-kinematics and payload screen\n\n**Run:** "+summary.runId+"<br>\n**Evidence:** simulated from concept dimensions; not experimentally validated.\n\n"+
    "## Result\n\n- Reachable perimeter points: **"+good.length+"/"+rows.length+" ("+summary.results.coveragePercent+"%)**.\n- Maximum shoulder-to-target distance: **"+summary.results.maxShoulderToTargetMm+" mm**.\n- Maximum FK closure error: **"+summary.results.maxForwardKinematicsClosureErrorMm+" mm**.\n\n"+
    "Two-link IK uses cos(q2)=(d^2-L1^2-L2^2)/(2 L1 L2); both elbow branches are solved and the branch with minimum absolute pitch sum is retained. The wrist pitch cancels shoulder-plus-elbow pitch for a nominal horizontal tool.\n\n"+
    "![Workspace screen](IK_WORKSPACE_SCREEN.svg)\n\n## Limits\n\n"+
    "The points and base location are illustrative. Unlimited joint travel, free yaw and a rigid ideal chain are assumed. There are no collision, link mass, tool, actuator, speed, structural, force, duty-cycle or safety models. Replace the panel and tool assumptions and obtain manufacturer data before considering a guarded physical build.\n";
  fs.writeFileSync(path.join(outDir,"IK_MODEL_REPORT.md"),report);
  return summary;
}
if (process.argv[1] && import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href) {
  const here=path.dirname(fileURLToPath(import.meta.url)), input=process.argv[2]||path.join(here,"inputs","perimeter_task_points.csv"), output=process.argv[3]||path.join(here,"outputs");
  console.log(JSON.stringify(runModel(input,output),null,2));
}
