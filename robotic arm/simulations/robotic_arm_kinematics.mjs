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
export function staticGravityMoments({upperLinkMassKg,forearmMassKg,toolMassKg,payloadMassKg,link1M=1.1,link2M=0.9}={}) {
  const masses=[upperLinkMassKg,forearmMassKg,toolMassKg,payloadMassKg];
  if (!masses.every(Number.isFinite) || masses.some(x=>x<0) || ![link1M,link2M].every(Number.isFinite) || link1M<=0 || link2M<=0) {
    throw new RangeError("Provide finite non-negative masses and positive finite link lengths.");
  }
  const distalMass=toolMassKg+payloadMassKg, g=MODEL.gravityMps2;
  return {
    shoulderNm:g*(upperLinkMassKg*link1M/2+forearmMassKg*(link1M+link2M/2)+distalMass*(link1M+link2M)),
    elbowNm:g*(forearmMassKg*link2M/2+distalMass*link2M),
  };
}
function candidateJointEnvelope(rows) {
  const joints=["yaw_deg","shoulder_pitch_deg","elbow_pitch_deg","wrist_compensation_deg"];
  const reachable=rows.filter(r=>r.ik_reachable===true);
  return Object.fromEntries(joints.map(joint=>{
    const values=reachable.map(r=>Number(r[joint]));
    return [joint,{minimumDeg:+Math.min(...values).toFixed(4),maximumDeg:+Math.max(...values).toFixed(4),spanDeg:+(Math.max(...values)-Math.min(...values)).toFixed(4)}];
  }));
}
function staticMomentSweep(outDir) {
  // Grid values are analyst-selected sensitivity points, not measurements or mass estimates.
  const linkMasses=[0,2.5,5,7.5,10], toolAndPayloadMasses=[0,1,2,3,4], rows=[];
  for (const upperLinkMassKg of linkMasses) for (const forearmMassKg of linkMasses)
    for (const toolMassKg of toolAndPayloadMasses) for (const payloadMassKg of toolAndPayloadMasses) {
      const m=staticGravityMoments({upperLinkMassKg,forearmMassKg,toolMassKg,payloadMassKg});
      rows.push({upper_link_mass_kg:upperLinkMassKg,forearm_mass_kg:forearmMassKg,tool_mass_kg:toolMassKg,payload_mass_kg:payloadMassKg,
        shoulder_gravity_moment_Nm:+m.shoulderNm.toFixed(4),elbow_gravity_moment_Nm:+m.elbowNm.toFixed(4)});
    }
  writeCsv(path.join(outDir,"STATIC_GRAVITY_MOMENT_SENSITIVITY.csv"),rows);
  return {scenarioCount:rows.length,grid:{upperAndForearmLinkMassKg:linkMasses,toolAndPayloadMassKg:toolAndPayloadMasses},
    maximumGridShoulderMomentNm:Math.max(...rows.map(r=>r.shoulder_gravity_moment_Nm)),maximumGridElbowMomentNm:Math.max(...rows.map(r=>r.elbow_gravity_moment_Nm)),
    evidence:"Analyst-selected sensitivity grid only; none of these masses is measured or proposed as a design value."};
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
  const jointEnvelope=candidateJointEnvelope(rows);
  const staticMoments=staticMomentSweep(outDir);
  const summary={runId:"S2-3D-PLANAR-IK-2026-11-21-01",evidence:"Simulated from stated geometry; not validated against a physical robot.",
    software:"Node.js "+process.version+"; built-in modules only",
    model:{architecture:"base yaw plus shoulder, elbow and wrist pitch",linkLengthsMm:[1100,900],baseXYmm:[0,-867],shoulderZmm:730,targetPlaneZmm:0,
      reachableAnnulusMm:[200,2000],branchSelection:"minimum |shoulder pitch| + |elbow pitch|; no joint stops"},
    selectedSolutionJointEnvelopeDegrees:jointEnvelope,
    staticGravityMomentSensitivity:staticMoments,
    inputs:{taskPointCount:rows.length},results:{reachableTaskPoints:good.length,totalTaskPoints:rows.length,coveragePercent:rows.length?+(100*good.length/rows.length).toFixed(2):0,
      maxShoulderToTargetMm:Math.max(...rows.map(r=>r.shoulder_to_target_mm)),maxForwardKinematicsClosureErrorMm:good.length?Math.max(...good.map(r=>Number(r.fk_error_mm))):null},
    limitations:["The 71 points represent an illustrative 2278 x 1134 mm panel and 300 mm standoff, not measured feed.",
      "Task points are projected into a radial vertical plane and base yaw is solved separately.",
      "No collision, joint limits, actuator curves, deflection, backlash, repeatability, tool pose, speed or acceleration are included.",
      "The selected-solution joint envelope describes this discrete point set only; it is not a commanded joint limit and does not include collisions, clearance or alternate task approaches.",
      "Payload-only moments exclude links, wrist, tool, acceleration, friction, duty and design factors.",
      "The link/tool/payload moment grid is an analyst-selected sensitivity range, not measured mass data or actuator sizing.","This is not a robot selection or safe motion plan."]};
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
    "## Candidate angle envelope\n\n"+Object.entries(jointEnvelope).map(([joint,x])=>"- "+joint+": **"+x.minimumDeg+"° to "+x.maximumDeg+"°** ("+x.spanDeg+"° span over these 71 selected solutions). This is a discrete geometry screen, not a required joint travel specification.\n").join("")+"\n"+
    "## Static gravity-moment sensitivity\n\n"+"The generated `STATIC_GRAVITY_MOMENT_SENSITIVITY.csv` evaluates 625 combinations of analyst-selected link, tool and payload masses. The link centers of mass are assumed at their midpoints; the assembly is horizontal and fully extended; tool and payload centers are placed at the wrist. The grid demonstrates how omitted masses affect gravity moment. Its mass values are not measurements or selected design values, and the results are not actuator ratings.\n\n"+
    "![Workspace screen](IK_WORKSPACE_SCREEN.svg)\n\n## Limits\n\n"+
    "The points and base location are illustrative. Unlimited joint travel, free yaw and a rigid ideal chain are assumed. There are no collision, link mass, tool, actuator, speed, structural, force, duty-cycle or safety models. Replace the panel and tool assumptions and obtain manufacturer data before considering a guarded physical build.\n";
  fs.writeFileSync(path.join(outDir,"IK_MODEL_REPORT.md"),report);
  return summary;
}
if (process.argv[1] && import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href) {
  const here=path.dirname(fileURLToPath(import.meta.url)), input=process.argv[2]||path.join(here,"inputs","perimeter_task_points.csv"), output=process.argv[3]||path.join(here,"outputs");
  console.log(JSON.stringify(runModel(input,output),null,2));
}
