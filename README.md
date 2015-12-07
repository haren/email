# Web Email Sending Service

This repository contains a sample email sending REST server with a web app.

The server documentation can be found in the [server](https://github.com/haren/email/tree/master/server) directory.

The web app documentation can be found in the [www](https://github.com/haren/email/blob/master/www) directory.

The project is currently deployed [here](http://ec2-52-31-146-15.eu-west-1.compute.amazonaws.com/) and supports sending plain text emails.

## Additional information

- Emails sent using text not html.
- All emails sent (in the current setup) from my personal email - please don’t abuse.
- Some rejections (e.g. Maligun) can take up to a few minutes to arrive through the webhook (patience advised).
- Mandrill sometimes confirms email send even though the address is incorrect (validation explained below). So it is possible to get a sent confirmation even though the email does not get send in this case.
- Email body is not cleaned on purpose on form submission. In case user sends to a wrong address or something else go wrong, retyping the whole body could be frustrating.
- Users are identified using a simple secret cookie mechanism.

