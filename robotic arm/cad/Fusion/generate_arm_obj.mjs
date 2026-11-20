import fs from "node:fs";
import path from "node:path";
import {fileURLToPath,pathToFileURL} from "node:url";
const outDefault=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"exports");
function box(name,x0,x1,y0,y1,z0,z1,mat){
  return {name,mat,v:[[x0,y0,z0],[x1,y0,z0],[x1,y1,z0],[x0,y1,z0],[x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]],
    f:[[1,2,3,4],[5,8,7,6],[1,5,6,2],[2,6,7,3],[3,7,8,4],[4,8,5,1]]};
}
function cylinder(name,cx,cy,cz,r,len,axis,mat,n=32){
  const v=[];
  for(let end=0;end<2;end++) for(let i=0;i<n;i++){
    const a=2*Math.PI*i/n, t=end?len/2:-len/2;
    if(axis==="z") v.push([cx+r*Math.cos(a),cy+r*Math.sin(a),cz+t]);
    else v.push([cx+r*Math.cos(a),cy+t,cz+r*Math.sin(a)]);
  }
  const f=[];
  for(let i=0;i<n;i++){const j=(i+1)%n;f.push([i+1,j+1,n+j+1,n+i+1]);}
  f.push(Array.from({length:n},(_,i)=>i+1).reverse(),Array.from({length:n},(_,i)=>n+i+1));
  return {name,mat,v,f};
}
export function generateObj(outDir=outDefault){
  fs.mkdirSync(outDir,{recursive:true});
  const parts=[
    box("BASE-01",-175,175,-175,175,0,20,"base"),
    box("PEDESTAL-01",-80,80,-80,80,20,670,"structure"),
    cylinder("J1-YAW",0,0,700,125,60,"z","joint"),
    cylinder("J2-SHOULDER",0,0,730,115,100,"y","joint"),
    box("LINK-01",0,1100,-60,60,680,780,"link"),
    cylinder("J3-ELBOW",1100,0,730,89.7,100,"y","joint"),
    box("LINK-02",1100,2000,-50,50,690,770,"link"),
    cylinder("J4-WRIST",2000,0,730,66.7,80,"y","joint"),
    box("TOOL-00-PLACEHOLDER",2000,2120,-50,50,722,738,"tool")
  ];
  const colors={base:[0.34,0.39,0.44],structure:[0.62,0.66,0.7],joint:[0.92,0.45,0.2],link:[0.18,0.44,0.72],tool:[0.9,0.72,0.18]};
  const mtl=Object.entries(colors).map(([k,c])=>"newmtl "+k+"\nKd "+c.join(" ")+"\nKa 0.08 0.08 0.08\n").join("\n");
  fs.writeFileSync(path.join(outDir,"agastya_arm_envelope.mtl"),mtl);
  let text="# AGASTYA concept envelope OBJ; dimensions in millimetres; not fabrication geometry\nmtllib agastya_arm_envelope.mtl\n";
  let offset=0;
  for(const p of parts){
    text+="\no "+p.name+"\ng "+p.name+"\nusemtl "+p.mat+"\n";
    for(const v of p.v) text+="v "+v.join(" ")+"\n";
    for(const face of p.f) {
      const tris=[];
      for(let i=1;i<face.length-1;i++) tris.push([face[0],face[i],face[i+1]]);
      for(const tri of tris) text+="f "+tri.map(i=>i+offset).join(" ")+"\n";
    }
    offset+=p.v.length;
  }
  const obj=path.join(outDir,"agastya_arm_envelope.obj");
  fs.writeFileSync(obj,text);
  const triangles=[];
  for(const p of parts) for(const face of p.f) for(let i=1;i<face.length-1;i++) triangles.push([p.v[face[0]-1],p.v[face[i]-1],p.v[face[i+1]-1]]);
  const facets=triangles.map(t=>{
    const u=t[1].map((v,i)=>v-t[0][i]), v=t[2].map((x,i)=>x-t[0][i]);
    const n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]], mag=Math.hypot(...n)||1;
    const normal=n.map(x=>x/mag).join(" ");
    return " facet normal "+normal+"\n  outer loop\n"+t.map(p=>"   vertex "+p.join(" ")).join("\n")+"\n  endloop\n endfacet";
  });
  const stl=path.join(outDir,"agastya_arm_envelope.stl");
  fs.writeFileSync(stl,"solid agastya_arm_envelope\n"+facets.join("\n")+"\nendsolid agastya_arm_envelope\n");
  return {obj,mtl:path.join(outDir,"agastya_arm_envelope.mtl"),stl,components:parts.length,triangleCount:triangles.length};
}
if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href) console.log(JSON.stringify(generateObj(process.argv[2]||outDefault),null,2));
