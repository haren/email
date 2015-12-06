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
        rejected_at: null,
        status: null,
        status_at: null
      },
      initialize: function() {
          this.updateDerivedAttributes();

          this.on( // update derived property status and status_at
            'change:queued_at change:sent_at change:rejected_at',
            this.updateDerivedAttributes, this
          );
      },
      updateDerivedAttributes: function() {
        var new_status    = null;
        var new_status_at = null;

        if (this.get('sent_at')) {
          new_status = "SENT";
          new_status_at = this.get('sent_at');
        } else if (this.get('rejected_at')) {
          new_status = "REJECTED";
          new_status_at = this.get('rejected_at');
        } else if (this.get('queued_at')) {
          new_status = "QUEUED";
          new_status_at = this.get('queued_at');
        }

        if (new_status_at) {
          new_status_at = parseInt(new_status_at);
        }

        this.set({
            status: new_status,
            status_at: new Date(parseInt(new_status_at)).toString()
        }, {silent:false}); //trigger the change for the views to update
      },

      send: function (options) { // options object used to pass a callback by client object.
        if (!this.isValid()) {
          if (options.callback) {
            options.callback(false, this.validationError);
          }
          return;
        }
        // perform the POST request to send.
        this.save(null, { //pass null to save all attributes
          success: function(model, response, opts){
            if (options.callback) {
              if (response.status == 200) {
                options.callback(true, response);
              } else {
                options.callback(false, response);
              }
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