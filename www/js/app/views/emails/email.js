define([
	'jquery',
	'underscore',
	'backbone',
	'text!views/emails/templates/emailView.tpl',
	], function($, _, Backbone, emailTemplate) {
		var EmailView = Backbone.View.extend({
			// el: '', // has to be passed from parent.
			events: {},

			render: function() {
				console.log(this.$el);
				this.$el.append(_.template(emailTemplate));
			}
		});
		return EmailView;
	}
);