define([
	'jquery',
	'underscore',
	'backbone',
	'views/index/index',
	],
	function($, _, Backbone, indexView) {
		var AppRouter = Backbone.Router.extend({
			routes: {
				'*actions': 'index'
			},

			index: function() {
				indexView.render();
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