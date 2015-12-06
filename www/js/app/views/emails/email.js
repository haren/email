define([
	'jquery',
	'underscore',
	'backbone',
	'text!views/emails/templates/emailView.tpl',
	], function($, _, Backbone, emailTemplate) {
		var EmailView = Backbone.View.extend({
			el: '', 		// pass from parent.
			model: null, 	// pass from parent
			template: _.template(emailTemplate),

			className: function() {
				if (this.model.get('status') == "SENT") {
					return "success";
				} else if (this.model.get('status') == "REJECTED") {
					console.log("NO ZWRACAM KUHWA")
					return "danger";
				} else if (this.model.get('status') == "QUEUED") {
					return "warning";
				}
				return "";
			},

			updateClassName: function() {
				this.$el.removeClass().addClass(this.className());
			},

			initialize: function() {
				this.listenTo(this.model, "change", this.render);
			},

			render: function() {
				this.updateClassName();
				this.$el.html(this.template(this.model.toJSON()));
				return this;
			}
		});
		return EmailView;
	}
);