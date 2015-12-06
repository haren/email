define([
	'jquery',
	'underscore',
	'backbone',
	'text!views/index/templates/indexView.tpl',
	], function($, _, Backbone, indexTemplate) {
		var indexView = Backbone.View.extend({
			el: 'body',

			events: {
		        "click #btn-emails" : "routeToEmails"
		    },

			routeToEmails: function(e) {
        		Backbone.history.navigate("/emails", true);
		    },

			render: function() {
				$(this.el).html(_.template(indexTemplate));
			}
		});
		return new indexView;
	}
);