define([
  'jquery',
  'underscore',
  'backbone'
  ], function($, _, Backbone) {
    var EmailModel = Backbone.Model.extend({
      urlRoot: '/emails',
      defaults: {
        to: null,
        cc: [],
        bcc: [],
        subject: null,
        text: null,
        queued_at: null,
        sent_at: null,
        rejected_at: null
      },
      initialize: function(){},
      send: function (options) { // options object used to pass a callback by client object.
        if (!this.isValid()) {
          if (options.callback) {
            options.callback(false, this.validationError);
          }
          return;
        }
        console.log('x');
        // perform the POST request to send.
        this.save(null, { //pass null to save all attributes
          success: function(model, response, opts){
            if (options.callback) {
              options.callback(true, response);
            }
          },
          error: function(model, response, opts){
            if (options.callback) {
              options.callback(false, response);
            }
          }
        });
      },
      validate: function(attrs) {
        if (!attrs.to) {
          console.log(attrs.to);
          return "Provide to address."
        } else if (!attrs.subject) {
          return "Provide email subject."
        } else if (!attrs.text) {
          return "Provide email text."
        } else if (attrs.queued_at || attrs.sent_at || attrs.rejected_at) {
          return "This email has already been sent.";
        }
        // success, no need to return anything - save will continue.
      }
    });
    return EmailModel;
  }
);