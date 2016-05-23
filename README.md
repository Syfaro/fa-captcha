Recently, FA added a captcha to the login screen.

Naturally, this broke sites that requested your username and password to
import data, such as Furry Network. This is just a really bad example of
how you could just store the session server side and have the user solve
the captcha. It doesn't really add much complexity to the whole process.
