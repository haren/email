define([
	'jquery',
	'underscore',
	'backbone',
	'text!views/index/templates/indexView.tpl',
	], function($, _, Backbone, indexTemplate) {
		var indexView = Backbone.View.extend({
			el: 'body',

			events: {
		        "click #btn-emails" 		: "routeToEmails",
		        "submit #send-email-form"	: "sendEmail"
		    },

			routeToEmails: function(e) {
        		Backbone.history.navigate("/emails", true);
		    },

		    sendEmail: function(e) {
		    	e.preventDefault();

		    	// TODO REPLACE WITH BACKBONE MODEL - VALIDATE + SAVE
		    	var email = {
		    		'to': $('#to-address').val(),
		    		'subject': $('#subject').val(),
		    		'text': $('#body').val()
		    	}
	    	    $.ajax({
			        type: "POST",
			        url: "/emails",
			        async: true,
			        cache: false,
			        data: email, dataType: "json",
			        success: function (result) { console.log(result) },
			        error: function (jqXHR, exception) {
			            console.log(exception);
			        } }
			    );
		    },

			render: function() {
				$(this.el).html(_.template(indexTemplate));
			}
		});
		return new indexView;
	}
);

// https://github.com/thedersen/backbone.validation