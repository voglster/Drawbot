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

pennys_to_hold = 20;

holder_thickness = 3;

penny_diameter = 19.3;
penny_thickness = 1.6;

penny_shaft_height = penny_thickness*pennys_to_hold;

shell_radius = penny_diameter/2 + holder_thickness;

ball_diameter = 3.1;
ball_radius = ball_diameter/2;
ball_spacing = 4.3;
ball_segment_length = ball_spacing - ball_diameter;

top_height = ball_diameter * 3;


module top(base_r,top_r,top){
    difference(){
    cylinder(r1=base_r,r2=top_r*2, h=top, center=true);
    translate([7,0,2])
    rotate([0,90,0])
        union(){
            cylinder(r=ball_diameter/2*1.1, h=penny_diameter/2+holder_thickness, center=true);
            translate([top_height/4,0,0])
            cube(size=[top_height/2,ball_diameter*1.1,penny_diameter/2+holder_thickness],center=true);
            translate([-ball_segment_length,0,-1/2 * (penny_diameter/2+holder_thickness)])
            sphere(r=ball_diameter/2,center=true);
            translate([(top_height - ball_diameter - ball_segment_length*1.5)/2,0,-shell_radius/2])
            rotate([0,90,0])
            cylinder(r=ball_diameter/2, h=top_height - ball_segment_length - ball_radius, center=true);
            cube(size=[9,1,14],center=true);
        }
    }
}
translate([-5,-10,20])
rotate([90,-90,-20]) 
top(10,1.55,10);

translate([-5,10,20])
rotate([270,-90,20]) 
top(10,1.55,10);


