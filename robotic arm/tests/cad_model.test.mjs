import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {generateObj} from "../cad/Fusion/generate_arm_obj.mjs";

test("concept CAD generator writes a nine-component OBJ and ASCII STL mesh",()=>{
  const out=path.resolve(import.meta.dirname,"..","cad","Fusion","exports"), r=generateObj(out);
  assert.equal(r.components,9); assert.ok(r.triangleCount>100);
  const obj=fs.readFileSync(r.obj,"utf8"), stl=fs.readFileSync(r.stl,"utf8");
  assert.equal((obj.match(/^o /gm)||[]).length,9);
  assert.equal((stl.match(/ facet normal /g)||[]).length,r.triangleCount);
  assert.match(obj,/TOOL-00-PLACEHOLDER/);
});
