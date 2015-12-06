define([
	'jquery',
	'underscore',
	'backbone',
	'views/index/index',
	'views/emails/emailsMain',
	],
	function($, _, Backbone, indexView, emailsView) {
		var AppRouter = Backbone.Router.extend({
			routes: {
				'emails'  : 'emails',
				'*actions': 'index'
			},

			index: function() {
				indexView.render();
			},

			emails: function() {
				emailsView.render();
			}
		});

		var init = function() {
			var app_router = new AppRouter;
			Backbone.history.start();
		};
		return {
			init: init
	 	}
	}
);