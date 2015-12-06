define([
	'jquery',
	'underscore',
	'backbone',
	'backboneCollectionView',
	'collections/emails',
	'views/emails/email',
	'text!views/emails/templates/emailsMainView.tpl',
	], function($, _, Backbone, BackboneCollectionView, EmailsCollection, EmailView, emailsTemplate) {
		var emailsView = Backbone.View.extend({
			el: 'body',
			// selectable: false,
			// collection: new EmailsCollection(),
			// modelView: EmailView,
			childView: new EmailView(),

			events: {
		        "click #btn-back" : "routeToIndex"
		    },

		    routeToIndex: function(e) {
        		Backbone.history.navigate("/", true);
		    },

			render: function() {
				var emails = new EmailsCollection();
				emails.fetch({
					success: function() { console.log(emails.models)}
				});
				$(this.el).html(_.template(emailsTemplate));
				this.childView.$el = this.$('#emails-list');
				console.log(this.childView);
				console.log(this.childView.$el);
				this.childView.render();
				this.childView.delegateEvents();
			}
		});
		return new emailsView;
	}
);