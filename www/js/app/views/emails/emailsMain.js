define([
	'jquery',
	'underscore',
	'backbone',
	'collections/emails',
	'views/emails/emails',
	'text!views/emails/templates/emailsMainView.tpl',
	], function($, _, Backbone, EmailsCollection, EmailCollectionView, emailsTemplate) {
		var emailsView = Backbone.View.extend({
			el: '#main',
			childView: new EmailCollectionView(),

			events: {
		        "click #btn-back" : "routeToIndex"
		    },

		    routeToIndex: function(e) {
        		Backbone.history.navigate("/", true);
		    },

			render: function() {
				$(this.el).html(_.template(emailsTemplate));

				// make sure to initialize only once
				this.childView.collection =
					this.childView.collection || window.emailsCollection || new EmailsCollection();

				var self = this;
				this.childView.collection.fetch({
					success: function() {
						self.childView.$el = self.$('#emails-list-container');
						self.childView.render();
						self.childView.delegateEvents();
					}
				});
			}
		});
		return new emailsView;
	}
);