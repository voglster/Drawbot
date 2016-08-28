// Parametric ball chain pulley
// Based on "Parametric Ball Pulley" by zignig (http://www.thingiverse.com/thing:1322)

// Quality of cylinders/spheres
$fa = 10;
$fs = 0.4;

// 0 = use grub screws and captive nut
// 1 = use a hose clamp
// 2 = use two "flat spots" on the shaft
// 3 = use one "flat spot" on the shaft
// 4 = one flat with grub screw
fastening_method = 4;

// General options
shaft_diameter = 5.5;
ball_diameter = 3.1;
ball_count = 18;
ball_spacing = 4.3; // The distance from the centre of one ball to the next
link_diameter = 0.9;
guide_thickness = 2;
guide_extra_radius = 2;

guide_enabled = 1;

// Screw options
screw_diameter = 2.5;
screw_count = 1;
nut_diameter = 0; // correct?
nut_height = 0; // correct?

// Hose clamp options
clamp_inner_diameter = 13;
clamp_width = 8;

// Flat spot options
flat_spot_diameter = 5;

// Calculate dimensions
PI = 3.1415927;
wheel_diameter = ball_count*ball_spacing / PI;
guide_height = guide_thickness * guide_enabled;
wheel_height = ball_diameter*1;
boss_diameter = ( fastening_method == 0 ? shaft_diameter + (nut_height*2)*2 : ( fastening_method == 1 ? clamp_inner_diameter : shaft_diameter*2 ) );
boss_height = 8;
pulley_height = wheel_height + boss_height+ (2 * guide_height);



module guide(){
cylinder(h = guide_thickness, r1 = wheel_diameter/2, r2 = wheel_diameter/2 + guide_extra_radius, center = true);
}

module wheel_base(){
    cylinder (wheel_height, r = wheel_diameter/2, center=true, $fn = ball_count);
}

module balls_base(){
    for (i = [1:ball_count])
		{	
			rotate ([0, 0, (360/ball_count) * i])		
			translate ([wheel_diameter/2,0,0])
			sphere (r = ball_diameter/2);
		}
}

module lines_between_balls(){
    // Holes for links between balls
		rotate ([0, 0, -90]) // Rotate -90 to match face direction of cylinder
		rotate_extrude (convexity = 5, $fn = ball_count)
		translate ([wheel_diameter/2, 0, 0])
		circle (r = link_diameter/2, center = true);
}

module balls(){
    union(){
        balls_base();
        lines_between_balls();
    }
}

module guided_pulley(){
    translate ([0, 0, -1 * (wheel_height + guide_height)/2])
    rotate([180,0,0]){
            guide();
    }
    difference(){
        wheel_base();
        balls();
    }
    translate ([0, 0, (wheel_height + guide_height)/2])
    guide();
}

module shaft_sleeve_base(){
    cylinder (boss_height + wheel_height + 2* guide_height, r = boss_diameter/2, center=true);
}

module motor_shaft_cutout(){
    intersection () {
				cylinder ( boss_height + wheel_height + 2* guide_height+5, r = shaft_diameter/2, center = true);
				
				translate ([ (fastening_method == 3 || fastening_method == 4 ? shaft_diameter/2 - flat_spot_diameter/2 : 0) , 0, 0])
				cube ([flat_spot_diameter, shaft_diameter*2,  pulley_height*3], center = true);
			}
}

module shaft_sleeve_set_screw_hole(){
    translate ([0, 0, pulley_height/2 - boss_height/3])
			for (i = [1: screw_count]) {
				rotate ([0, 0, 360/screw_count * i + 180]) {
					translate ([boss_diameter/2, 0, 0])
					rotate ([0 ,90 , 0])
					cylinder (boss_diameter, r = screw_diameter/2, center = true);
					
					translate ([shaft_diameter/2 + (boss_diameter/2 - shaft_diameter/2)/2 - nut_height/4, 0, 0]) {
						rotate ([0 , 90, 0])
						cylinder (nut_height, r = nut_diameter/2, center = true, $fn = 6);
						
						translate ([0, 0, boss_height / 2])
						cube ([nut_height, sin(60) * nut_diameter, boss_height], center = true);
					}
				}
			}
}


module shaft_sleeve(){
    difference(){
        shaft_sleeve_base();
        motor_shaft_cutout();
        shaft_sleeve_set_screw_hole();
    }
}


module pulley () {
    union(){
        difference(){
            guided_pulley();
            shaft_sleeve_base();
        }
        translate([0,0,boss_height/2])
        shaft_sleeve();
    }
}
translate ([0, 0, wheel_height/2 + guide_thickness])
pulley();

echo ( str ("Pulley height: ", pulley_height) );
echo ( str ("Pulley diameter: ", wheel_diameter ) );