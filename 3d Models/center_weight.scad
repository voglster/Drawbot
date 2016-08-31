$fa = 5;
$fs = 0.4;

pennys_to_hold = 40;
holder_thickness = 3;
penny_diameter = 19.3;
penny_rad = penny_diameter/2;
penny_thickness = 1.6;
penny_shaft_height = penny_thickness*pennys_to_hold;
shell_radius = penny_diameter/2 + holder_thickness;

module penny_shaft(){
rotate([0,90,0])
cylinder(r=penny_rad,h=penny_shaft_height,center=true);
}

module holder_shaft(){
rotate([0,90,0])
cylinder(r=penny_rad+holder_thickness,h=penny_shaft_height+2*holder_thickness,center=true); 
}

union(){
difference(){
    holder_shaft();
    penny_shaft();
    translate([0,0,penny_rad/1.5])
    cube(size=[penny_shaft_height*2,penny_diameter*2,penny_diameter],center=true);
}

difference(){
    cube(size=[penny_shaft_height+2*holder_thickness,penny_diameter+2*holder_thickness,penny_diameter+2*holder_thickness],center=true);
    translate([5,0,0])
    holder_shaft();
    translate([-5,0,0])
    holder_shaft();
    translate([0,0,penny_rad-.2])
    cube(size=[penny_shaft_height+2*holder_thickness+1,penny_diameter+2*holder_thickness+1,penny_diameter+2*holder_thickness],center=true);
}}