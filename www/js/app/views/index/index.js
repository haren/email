define([
	'jquery',
	'underscore',
	'backbone',
	'text!views/index/templates/indexView.tpl',
	], function($, _, Backbone, indexTemplate) {
		var indexView = Backbone.View.extend({
			el: 'body',

			render: function() {
				$(this.el).html(_.template(indexTemplate));
			}
		});
		return new indexView;
	}
);