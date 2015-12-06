define([
	'jquery',
	'underscore',
	'backbone',
	'backboneCollectionView',
	'collections/emails',
	'views/emails/email',
	'text!views/emails/templates/emailsView.tpl',
	], function($, _, Backbone, BackboneCollectionView, EmailCollection, EmailView, EmailCollectionTemplate) {
		var EmailsView = Backbone.View.extend({
			el: '#emails-list-container', // has to be passed from parent.
			collection: null, // can to be passed from parent.

			initalize: function() {
				console.log(this.collection);
			},

			render: function() {
				this.$el.html(_.template(EmailCollectionTemplate));
				var self=this;
				self.collection.each(function(email){
		            var emailView = new EmailView({
		            	model: email,
		            	el: self.$('#emails-list')
		            });
		            console.log(emailView.el);
		            // self.$el.append(emailView);
		            emailView.render();
					emailView.delegateEvents();

				}, self);
			}
		});
		return EmailsView;
	}
);