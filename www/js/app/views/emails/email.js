define([
	'jquery',
	'underscore',
	'backbone',
	'text!views/emails/templates/emailView.tpl',
	], function($, _, Backbone, emailTemplate) {
		var EmailView = Backbone.View.extend({
			el: '', // pass from parent.
			template: _.template(emailTemplate),
			model: null, // pass from parent
			events: {},

			initialize: function() {
				this.listenTo(this.model, "change", this.render);
			},

			render: function() {
				this.$el.append(this.template(this.model.toJSON()));
			}
		});
		return EmailView;
	}
);