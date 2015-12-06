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
				// load all emails in the collection
				// the collection view will update automatically.
				self.collection.each(function(email){
		            var emailView = new EmailView({
		            	model: email,
		            	tagName: 'tr',
		            });
		            self.$el.append(emailView.render().el);
				}, self);
			}
		});
		return EmailsView;
	}
);