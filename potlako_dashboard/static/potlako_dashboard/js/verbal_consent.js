function validateForm() {
	var error = 0;
	var signature = document.forms["verbal_consent"]["signature"].value;
	var f_init = signature.split("")[0];
	var l_init = signature.split("")[signature.length-1];

	var initials = document.forms["verbal_consent"]["initials"].value;
	var first_initial = initials.split("")[0];
	var last_initial = initials.split("")[initials.length-1];
 
    	if ((f_init != first_initial) || (l_init != last_initial)) {
    		error++;
    		document.getElementById('name_error').innerHTML = '*Participant initials do not match';
	}
	if(error>0) {
		return false;
	}
    return true;
}