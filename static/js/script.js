jQuery( document ).ready( function ( $ ) {
	// JS uses milliseconds; PHP does not

	// min_date will never be empty string (unless incorrectly filtered in PHP)
	var min_date = new Date( php_vars.min_date * 1000 );

	// max_date will always be set but may be zero
	// empty string * 1000 is zero
	// non-empty string * 1000 is NaN
	// else we assume it is a PHP timestamp, which needs to convert to milliseconds
	var max_date = php_vars.max_date * 1000;
	if (
		0 === max_date ||
		isNaN( max_date ) ||
		min_date > max_date
	) {
		max_date = '';
	} else {
		max_date = new Date( max_date );
	}

	/**
	 * Set the minDate and maxDate and watch it for changes in case the user
	 * manually enters a value, in which case we set the value to blank and add
	 * the error class. Setting 'maxDate' to an empty string is as if it's not
	 * set so no worries there.
	 */
	$( '#EventStartDate' )
		.datepicker( 'option', 'minDate', min_date )
		.datepicker( 'option', 'maxDate', max_date )
		.on( 'change', function () {
			var start_value_date = $( this ).datepicker( 'getDate' );
			if (
				min_date > start_value_date ||
				(
					'date' === $.type( max_date ) &&
					max_date < start_value_date
				)
			) {
				// If the user submits with a blank start date, the event will be saved with a start date of Today.
				$( this ).datepicker( 'setDate', '' );
				$( this ).addClass( php_vars.error_class );
			} else {
				$( this ).removeClass( php_vars.error_class );
			}
		} );
} );