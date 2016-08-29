$fa = 5;
$fs = 0.4;

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

module pennyshaft(){
    cylinder(r=penny_diameter/2, h=penny_shaft_height + penny_thickness, center=true);
}

module holder_base(){
    cylinder(r=penny_diameter/2+holder_thickness, h=penny_thickness*pennys_to_hold+holder_thickness*2, center=true);
}

module view_cutout(){
    cube(size=[penny_diameter + holder_thickness*2,penny_diameter/1.3,penny_thickness*pennys_to_hold], center=true);
    translate([penny_diameter/2,0,penny_thickness])
    cube(size=[penny_diameter + holder_thickness*2,penny_diameter/1.3,penny_thickness*pennys_to_hold], center=true);
}

module penny_cutout(){
    cube(size=[penny_diameter,penny_diameter,penny_thickness], center=true);
}

module top(){
    difference(){
    translate([0,0,(penny_thickness*pennys_to_hold+holder_thickness*2)/2 + top_height/2])
    cylinder(r1=penny_diameter/2+holder_thickness,r2=ball_diameter, h=top_height, center=true);
    translate([(penny_diameter/2+holder_thickness)/2,0,(penny_thickness*pennys_to_hold+holder_thickness*2)/2 + top_height - ball_diameter/2 - (ball_spacing - ball_diameter)*.95])
    rotate([0,90,0])
        union(){
            cylinder(r=ball_diameter/2*1.1, h=penny_diameter/2+holder_thickness, center=true);
            translate([top_height/2,0,0])
            cube(size=[top_height,ball_diameter*1.1,penny_diameter/2+holder_thickness],center=true);
            translate([-ball_segment_length,0,-1/2 * (penny_diameter/2+holder_thickness)])
            sphere(r=ball_diameter/2,center=true);
            translate([(top_height - ball_diameter - ball_segment_length*1.5)/2,0,-shell_radius/2])
            rotate([0,90,0])
            cylinder(r=ball_diameter/2, h=top_height - ball_segment_length - ball_radius, center=true);
            cube(size=[10,1,14],center=true);
        }
    }
}

union(){

difference(){
    holder_base();
    translate([0,0,penny_thickness/2])
    pennyshaft();
    view_cutout();
    translate([penny_diameter/2,0,(penny_thickness*(pennys_to_hold+1)) /2])
    penny_cutout();
}
    top();
}