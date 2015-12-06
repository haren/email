define([
	'jquery',
	'underscore',
	'backbone',
	'text!views/emails/templates/emailsView.tpl',
	], function($, _, Backbone, emailsTemplate) {
		var indexView = Backbone.View.extend({
			el: 'body',
			events: {
		        "click #btn-back" : "routeToIndex"
		    },

		    routeToIndex: function(e) {
		    	console.log('clicked')
        		Backbone.history.navigate("/", true);
		    },

			render: function() {
				$(this.el).html(_.template(emailsTemplate));
			}
		});
		return new indexView;
	}
);