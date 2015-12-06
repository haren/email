define([
	'jquery',
	'underscore',
	'backbone',
	'text!views/index/templates/indexView.tpl',
	'models/email'
	], function($, _, Backbone, indexTemplate, EmailModel) {
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

		    	var email = new EmailModel({
		    		'to': 		$('#to-address').val(),
		    		'subject': 	$('#subject').val(),
		    		'text': 	$('#body').val()
		    	});
		    	var sendResult = email.send({
		    		callback: function(success, message) {
		    			// TODO show message with send result
		    			console.log(success, message)
		    		}
		    	});
		    },

			render: function() {
				$(this.el).html(_.template(indexTemplate));
			}
		});
		return new indexView;
	}
);