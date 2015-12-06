<div class="well bs-component col-lg-6 col-lg-offset-3">
<form id="send-email-form" class="form-horizontal">
<fieldset>
  <legend>Send your email the seamless way.</legend>
  <div class="form-group">
    <label for="to-address" class="col-lg-2 control-label">Recipient</label>
    <div class="col-lg-10">
      <input id="to-address" class="form-control" type="email" placeholder="Email" required>
    </div>
  </div>
  <div id="cc-fields">
    <div class="form-group">
      <div>
        <label for="cc-input" class="col-lg-2 control-label">Cc</label>
        <div class="col-lg-10">
          <input id="cc-input" class="cc-input form-control" type="email" placeholder="Cc address (optional)">
        </div>
      </div>
    </div>
  </div>
  <div class="form-group">
    <div class="col-lg-10 col-lg-offset-2">
      <button type="button" id="cc-button" class="more-fields btn btn-default">Add more</button>
    </div>
  </div>
  <div id="bcc-fields">
    <div class="form-group">
      <div>
        <label for="bcc-input" class="col-lg-2 control-label">Bcc</label>
        <div class="col-lg-10">
          <input id="bcc-input" class="cc-input form-control" type="email" placeholder="Bcc address (optional)">
        </div>
      </div>
    </div>
  </div>
  <div class="form-group">
    <div class="col-lg-10 col-lg-offset-2">
      <button type="button" id="bcc-button" class="more-fields btn btn-default">Add more</button>
    </div>
  </div>
  <div class="form-group">
    <label for="subject" class="col-lg-2 control-label">Subject</label>
    <div class="col-lg-10">
      <input id="subject" class="form-control" type="text" placeholder="Email subject" required>
    </div>
  </div>
  <div class="form-group">
    <label for="body" class="col-lg-2 control-label">Body</label>
    <div class="col-lg-10">
      <textarea class="form-control" rows="5" id="body" required></textarea>
      <span class="help-block">Provide your email body above.</span>
    </div>
  </div>
  <div class="form-group">
      <div class="col-lg-10 col-lg-offset-2">
        <button id="btn-emails" type="button" class="btn btn-default">Sent mails</button>
        <button id="btn-submit" type="submit" class="btn btn-primary">Send your email!</button>
      </div>
    </div>
</fieldset>
</form>
</div>