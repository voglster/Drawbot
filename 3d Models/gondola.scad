pen_radius = 5.6;

module cd_hole(){
    cylinder(r=10,h=10,center=true);
}

module pen(){
    cylinder(r=5.6,h=100, center=true);
}

module cd(){
    translate([0,0,-.5])
    difference(){
        cylinder(r=59,h=1,center=true);
        cd_hole();
    }
}

module base(){
    cylinder(r=20,h=3,center=true);
}

module small_cutout(){
    
}

*cd();
*pen();
*translate([0,0,2]){
    base();
}


$fn=100;
cd_hole_rad = 10;
small_rad = 4;
large_rad= 7;
hole_rad = cd_hole_rad;
base_height = 3;
shaft_thickness=3;
shaft_height = 30;
grub_hole_size = 3;

module tear(small_rad,large_rad,hole_rad,base_height,center=false){

up = hole_rad - large_rad;
down = -hole_rad + small_rad;

linear_extrude(height = base_height,center=center){
hull(){
translate([up,0,0])  circle(r=large_rad);
//polygon(points=[[up,-large_rad],[up,large_rad],[down,small_rad],[down,-small_rad]]);
translate([down,0,0]) circle(r=small_rad);
}
}
}

base_rad = 25;
base_height = 3;

module grub_hole(){
translate([hole_rad,0,shaft_height*2/3])
rotate([0,90,0])
cylinder(h=shaft_thickness*3,r=grub_hole_size,center=true);
}


difference(){
    union(){
    
    tear(small_rad+shaft_thickness,large_rad+shaft_thickness,hole_rad+shaft_thickness,shaft_height);
    cylinder(r=base_rad,h=base_height);    
    }
    translate([0,0,-.5])
    tear(small_rad,large_rad,hole_rad,shaft_height+1);
    grub_hole();
}


