//-- This is a holder for the Arduino
//-- Uno + CNC Shield V3 + A4988 + 60mm fan stack,
//-- where the boards slide in USB interface first.
//-- Based on my earlier similar design for the P3Steel.

//-- by AndrewBCN - Barcelona, Spain - May 2015
//-- License is GPL V3

//-- Inspired by two Thingiverse objects: #8706 and #443013

//-- This is a new version specifically designed to use
//-- self-tapping wood screws to screw the holder to a
//-- wooden base.

//-- Parameters

//-- Arduino Uno dimensions
ard_l = 69;
ard_w = 53.5;

usb_w = 13.5;  // USB cutout width
power_w = 10;  // Arduino power connector cutout width

//-- Base dimensions
wall_th = 2; // wall thickness
side_wall_height = 7;
bottom_wall_height = 11;

base_l = ard_l + wall_th;
base_w = ard_w + wall_th + wall_th + 0.9; // 1mm margin to allow the arduino to slide in
base_h = wall_th + 1; // make it slightly thicker than walls

bottom_rail_height = -1.8; // I confess I eyeballed this value

//-- frame attachments dimensions
holder_corner_radius = 6.5;
holder_corner_height = 7;

nut_well_diameter = 8.8;
nut_well_depth = 5;
screw_diam = 3.4; // M3 nuts and bolts are used throughout

//-- P3Steel dimensions as measured
x1 = 68; // horizontal distance between bottom holes
x2 = 68; // horizontal distance between top holes
x_offset = 0; // approximate horizontal offset between top and bottom holes centerlines

y1 = 50; // vertical distance between holes


module base() {
//-- Build base, bottom wall, side wall, rails
//-- all are cubes
//-- note base is hollowed out using another cube

  rotate([0,0,90])
  translate([20,4,base_h/2]) {
    difference() {
      cube([base_l, base_w, base_h], center=true);
      cube([base_l-2*side_wall_height, base_w-2*side_wall_height, 3*base_h], center=true);
      translate([-29,-15.5,0])
	cylinder(r=3, h=3*base_h,$fn=30,center=true); // small prong cutout
    }
    translate([wall_th/2-base_l/2,0,bottom_wall_height/2])
      difference() {
	cube([wall_th, base_w, bottom_wall_height], center=true); // bottom wall
	translate([0,11.7,0])
	  cube([2*wall_th, usb_w+0.5, bottom_wall_height+2], center=true); // USB cutout
	translate([0,-19.3,0])
	  cube([2*wall_th, power_w+0.5, bottom_wall_height+2], center=true); // Arduino power connector cutout
      }
    translate([0,-wall_th/2+base_w/2,bottom_wall_height/2]) {
      cube([base_l, wall_th, bottom_wall_height], center=true); // side wall left
      translate([0,-wall_th/2,bottom_rail_height])
	cube([base_l, 1.8, 1], center=true); // bottom rail
      translate([0,-wall_th/2,bottom_rail_height+2.8]) // 2.8 = pcb thickness + rail thickness + some margin
	cube([base_l, 1.8, 1], center=true); // top rail
      }
    translate([0,wall_th/2-base_w/2,bottom_wall_height/2]) {
      cube([base_l, wall_th, bottom_wall_height], center=true); // side wall right
      translate([0,wall_th/2,bottom_rail_height])
	cube([base_l, 1.8, 1], center=true); // bottom rail
      translate([0,wall_th/2,bottom_rail_height+2.8]) // 2.8 = pcb thickness + rail thickness + some margin
	cube([base_l, 1.8, 1], center=true); // top rail
      }
    // small bumps to prevent the arduino sliding out of the holder
    translate([35,-27,3]) cylinder(r=0.6,h=5,$fn=10);
    translate([35,27,3]) cylinder(r=0.6,h=5,$fn=10);
  }
}

module stands() {
  difference() {
    cylinder(r=holder_corner_radius,h=holder_corner_height,$fn=30,center=true); // cylinder
    cylinder(r=screw_diam/2,h=2*holder_corner_height,$fn=30,center=true); // M3 screw hole
    translate([0,0,holder_corner_height-nut_well_depth])
      cylinder(r=nut_well_diameter/2,h=nut_well_depth+1,$fn=16,center=true); // M3 nut well
  }
}

module attachments() {
//-- OK, now we define the small stands that are going to be attaching
//-- our holder to the steel frame. These have to be positioned
//-- so they match the already laser-drilled holes in the frame.

//-- The centers of the four corner cylinders
//-- These are measured on the P3Steel frame on the left side
//-- P1, P4 : bottom holes
//-- P3, P4 : left holes

  P1=[x1/2,-y1/2,0];
  P2=[x2/2+x_offset,y1/2,0];
  P3=[-x2/2+x_offset,+y1/2,0];
  P4=[-x1/2,-y1/2,0];

  translate([-6,20,holder_corner_height/2]) {
      translate(P1)
	stands();
      translate(P2)
	stands();
      translate(P3)
	stands();
      translate(P4)
	stands();
  }
}

//-- a few cylinders conveniently placed and hulls to join them
//-- like, totally eyeballed...
module hull_shaper() {
 cylinder(r=1,h=base_h,$fn=10,center=true); // flat small cylinder
}

module arms() {
  // stand 1 right top
  #hull() {
  translate([20,-8,base_h/2]) hull_shaper();
  translate([40.7,-3,base_h/2]) hull_shaper();
  translate([40.7,4,base_h/2]) hull_shaper();
  translate([20,7,base_h/2]) hull_shaper();  
  }

  // stand 2 right bottom
  #hull() {
  translate([22,-22,base_h/2]) hull_shaper();
  translate([37.5,-42.5,base_h/2]) hull_shaper();
  translate([33.5,-48,base_h/2]) hull_shaper();
  translate([15,-30,base_h/2]) hull_shaper();  
  }

  // stand 3 left top
  #hull() {
  translate([-32,10,base_h/2]) hull_shaper();
  translate([-37,4,base_h/2]) hull_shaper();
  translate([-37,-3,base_h/2]) hull_shaper();
  translate([-32,-7,base_h/2]) hull_shaper();  
  }

  // stand 4 left bottom
  #hull() {
  translate([-34,-31,base_h/2]) hull_shaper();
  translate([-22,-30,base_h/2]) hull_shaper();
  translate([-38,-43,base_h/2]) hull_shaper();
  translate([-34,-46,base_h/2]) hull_shaper();  
  }
}

//-- Print the part
translate ([-2,0,0]) base();
attachments();
//arms(); // not used in this version

// these are used to check that the cutouts are correct
//translate([-33.5,-16,12]) color("blue") cube([9,1,2]);
//translate([18.5,-16,12]) color("blue") cube([3,1,2]);
//translate([-11,-16,12]) color("blue") cube([19,1,2]);