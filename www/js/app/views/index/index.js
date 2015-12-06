define([
	'jquery',
	'underscore',
	'backbone',
	'text!views/index/templates/indexView.tpl',
	'text!views/index/templates/inputEmail.tpl',
	'models/email'
	], function($, _, Backbone, indexTemplate, emailInputTemplate, EmailModel) {
		var indexView = Backbone.View.extend({
			el: 'body',

			events: {
		        "click #btn-emails" 		: "routeToEmails",
		        "click .more-fields"		: "addMoreInputFields",
		        "submit #send-email-form"	: "sendEmail"
		    },

			routeToEmails: function(e) {
        		Backbone.history.navigate("/emails", true);
		    },

		    addMoreInputFields: function(e) {
		    	var template = _.template(emailInputTemplate);

		    	if (e.target.id == "cc-button") {
		    		var parentEl = $('#cc-fields');
					parentEl.append(template({
						class_value : 'cc-input',
						placeholder: 'Cc address (optional)'
					}));
		    	} else if (e.target.id == "bcc-button") {
		    		var parentEl = $('#bcc-fields');
					parentEl.append(template({
						class_value : 'bcc-input',
						placeholder: 'Bcc address (optional)'
					}));
		    	}
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