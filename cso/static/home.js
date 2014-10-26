$(document).ready(function(){
	//.parallax(xPosition, speedFactor, outerHeight) options:
	//xPosition - Horizontal position of the element
	//inertia - speed to move relative to vertical scroll. Example: 0.1 is one tenth the speed of scrolling, 2 is twice the speed of scrolling
	//outerHeight (true/false) - Whether or not jQuery should use it's outerHeight option to determine when a section is in the viewport
	$('#home').parallax("50%", -0.6, true);
	$('#event').parallax("50%", -0.4, true);
	$('#colleges').parallax("50%", -0.8, true);
//	$('#dates').parallax("50%", -0.4);
//	$('#about').parallax("50%", -0.6);
});
