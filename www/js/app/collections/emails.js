define([
  'jquery',
  'underscore',
  'backbone',
  'models/email'
  ], function($, _, Backbone, EmailModel) {
    var EmailsCollection = Backbone.Collection.extend({
      url: '/emails',
      model: EmailModel,
      parse: function(response, options) {
        return response.emails;
      }
    });
    return EmailsCollection;
  }
);