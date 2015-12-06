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

		    	var cc_addresses = [];
		    	$(".cc-input").each(function() {
				    var cc = $(this).val();
		    		if (cc.length) {
		    			cc_addresses.push(cc);
		    		}
				});

				var bcc_addresses = [];
				$(".bcc-input").each(function() {
				    var bcc = $(this).val();
		    		if (bcc.length) {
		    			bcc_addresses.push(bcc);
		    		}
				});

		    	var email = new EmailModel({
		    		'to': 		$('#to-address').val(),
		    		'cc': 		cc_addresses,
		    		'bcc': 		bcc_addresses,
		    		'subject': 	$('#subject').val(),
		    		'text': 	$('#body').val()
		    	});
		    	email.send({
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