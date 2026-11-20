// AGASTYA Stage 2 concept envelope, millimetres.
// Parametric visualization only; no material, wall, joint, bearing, motor, tool or load design.
$fn=48;
L1=1100; L2=900; shoulder_z=730; base_t=20; pedestal_h=650; yaw_t=60;
module arm_envelope() {
  color("slategray") translate([0,0,base_t/2]) cube([350,350,base_t],center=true);
  color("silver") translate([0,0,base_t+pedestal_h/2]) cube([160,160,pedestal_h],center=true);
  color("steelblue") translate([0,0,base_t+pedestal_h+yaw_t/2]) cylinder(d=250,h=yaw_t,center=true);
  color("orange") translate([0,0,shoulder_z]) rotate([90,0,0]) cylinder(d=230,h=100,center=true);
  color("royalblue") translate([L1/2,0,shoulder_z]) cube([L1,120,100],center=true);
  color("orange") translate([L1,0,shoulder_z]) rotate([90,0,0]) cylinder(d=179.4,h=100,center=true);
  color("royalblue") translate([L1+L2/2,0,shoulder_z]) cube([L2,100,80],center=true);
  color("orange") translate([L1+L2,0,shoulder_z]) rotate([90,0,0]) cylinder(d=133.4,h=80,center=true);
  color("gold") translate([L1+L2+60,0,shoulder_z]) cube([120,100,16],center=true);
}
arm_envelope();
