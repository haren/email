define([
	'jquery',
	'underscore',
	'backbone',
	'views/emails/email',
	'text!views/emails/templates/emailsView.tpl',
	], function($, _, Backbone, EmailView, EmailCollectionTemplate) {
		var EmailsView = Backbone.View.extend({
			el: '', 			// pass from parent.
			collection: null, 	// pass from parent.

			render: function() {
				this.$el.html(_.template(EmailCollectionTemplate));

				var self=this;
				self.collection.each(function(email){
		            var emailView = new EmailView({
		            	model: email,
		            	el: self.$('#emails-list') // make sure to .append(), not .html() in child.
		            });
		            emailView.render();
					emailView.delegateEvents();

				}, self);
			}
		});
		return EmailsView;
	}
);