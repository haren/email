<p>Send your email the seamless way.</p>


<form id="send-email-form">
<div>
  <div>
    <input id="to-address" type="email" placeholder="Send To (single address)" required>
  </div>
</div>
<div id="cc-fields">
  <div>
    <input class="cc-input" type="email" placeholder="Cc address (optional)">
  </div>
  <div>
    <button type="button" id="cc-button" class="more-fields">Add more</button>
  </div>
</div>
<div id="bcc-fields">
  <div>
    <input class="bcc-input" type="email" placeholder="Bcc address (optional)">
  </div>
  <div>
    <button type="button" id="bcc-button" class="more-fields">Add more</button>
  </div>
</div>
<div>
  <div>
    <input id="subject" type="text" placeholder="Email subject" required>
  </div>
</div>
<div>
  <div>
    <textarea id="body" cols="40" rows="5" placeholder="Email body" required></textarea>
  </div>
</div>
<div>
    <button type="submit">Send your email!</button>
</div>
</form>

<button id="btn-emails">Sent mails</button>