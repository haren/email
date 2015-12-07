define([
	'jquery',
	'underscore',
	'backbone',
	'toastr',
	'collections/emails',
	'text!views/index/templates/indexView.tpl',
	'text!views/index/templates/inputEmail.tpl',
	'models/email'
	], function($, _, Backbone, toastr, EmailsCollection, indexTemplate, emailInputTemplate, EmailModel) {
		var indexView = Backbone.View.extend({
			el: '#main',

			events: {
		        "click #btn-emails" 		: "routeToEmails",
		        "click .more-fields"		: "addMoreInputFields",
		        "submit #send-email-form"	: "formSubmitted"
		    },

		    initialize: function() {
		    	this.initializeToastr();
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

		    formSubmitted: function(e) {
		    	e.preventDefault();
		    	this.flipButtonState("#btn-submit");
		    	this.sendEmail();
		    },

		    flipButtonState: function(button_id) {
		    	$(button_id).attr(
		    		"disabled", !$(button_id).attr("disabled")
		    	);
		    },

		    cleanFormFields: function() {
		    	// do not clean body, could be too frustrating.
		    	$('#send-email-form').find("input[type=text], input[type=email]").val("");
		    },

		    sendEmail: function(e) {
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

		    	var self = this;
		    	email.send({
		    		callback: function(success, message) {
		    			 // unblock the button for potential corrections / next sends
		    			self.flipButtonState("#btn-submit");

		    			if (success) {
		    				self.addSentEmailToCollection(email);
			    			self.cleanFormFields();
			    			if (message == "QUEUED") {
			    				self.showMessage(
			    					"warning",
			    					"Your email to " + email.get('to') +
			    					" has been queued. We'll notify you when it's sent or rejected."
			    				);
			    				email.pollForStateUpdate();
			    			} else if (success &&  message == "SENT") {
			    				self.showMessage(
			    					"success",
			    					"Your email to " + email.get('to') + " has been sent!"
			    				);
			    			}
		    			} else {
		    				self.showMessage(
		    					"error",
		    					"Your email to " + email.get('to') +
		    					" could not be sent. " + message
		    				);
		    			}
		    		}
		    	});
		    	this.showMessage("info", "Your request has been sent to our servers.");
		    },

		    addSentEmailToCollection: function(email) {
		    	window.emailsCollection = window.emailsCollection || new EmailsCollection();
		    	window.emailsCollection.add(email);
		    },

		    initializeToastr: function() {
		    	toastr.options = {
				  "closeButton": false,
				  "debug": false,
				  "newestOnTop": true,
				  "progressBar": false,
				  "positionClass": "toast-bottom-right",
				  "preventDuplicates": false,
				  "onclick": null,
				  "showDuration": "300",
				  "hideDuration": "1000",
				  "timeOut": "5000",
				  "extendedTimeOut": "1000",
				  "showEasing": "swing",
				  "hideEasing": "linear",
				  "showMethod": "fadeIn",
				  "hideMethod": "fadeOut"
				}
				window.showMessage = this.showMessage; // make available for all views
		    },

		    showMessage: function(status, message) {
		    	// status: success info / warning / danger
		    	if (status == "success") {
					toastr.success(message);
				} else if (status == "info") {
					toastr.info(message);
				} else if (status == "warning") {
					toastr.warning(message);
				} else if (status == "error") {
					toastr.error(message, null, {timeOut: 0}); //don't fade out
				}
		    },

			render: function() {
				$(this.el).html(_.template(indexTemplate));
			}
		});
		return new indexView;
	}
);