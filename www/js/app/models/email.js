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
      send: function () {
        // TODO move to this validate //this.validate()
        if (this.queued_at || this.sent_at || this.rejected_at) {
          // TODO return fail so that message can be shown
          console.log("This email has already been sent.");
        }

        // perform the POST request to send.
        this.save(null, { //pass null to save all attributes
          success: function(model, response, opts){
            console.log(response);
          },
          error: function(model, response, opts){
            console.log(response);
          }
        });
      }
    });
    return EmailModel;
  }
);