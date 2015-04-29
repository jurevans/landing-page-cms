***Landing Page Generator***

In this project, users may register for access (to be approved by the Administrator) to develop, draft and publish their
own HTML landing page which may be published to a sub-domain.

The Django Admin has been heavily modified to export some functionality to Users. This incorporates the account sign-up
and approval process, and allows the Registered User to manage their account using tools based on the Admin.

NOTE: This project is not up-to-date with more recent standards, nor is it being maintained by any means. 
It is merely illustrative of older Django
mechanisms and serves more as a scaffold for a future rewrite. Originally developed in 2008, and needless to say, much can be done to 
bring it up to par with the
current version of Django as of this writing (1.8), something I may do in a separate repo. 

Considering the number of changes in
the Django framework, Python, HTML5/CSS3, etc., this project could be rewritten to incorporate new features and to avoid
deprecated features. Examples of improvements include, but are not limited to, the following:

* Update templates to HTML5
* 960.gs was and is nice, however, I would use Bootstrap for base grid, form, and widget styles
* It wouldn't hurt to have a "composer.json" file declaring dependancies within the "public" or "static" domain, along 
with a declaration of "pip" dependencies for installation within "virtualenv" or deployment to a Web server
* A base JavaScript library would be a nice touch. In fact, for the generated Landing Pages themselves, 
Single Page Application 
(SPA) functionality could be integrated based on features selected and implemented, allowing some kind of dynamic behavior
within the landing page (e.g., drafting and publishing a landing page might incorporate a NoSQL database such as Redis or
UnQLite, or a SQLLite database affiliated and published with the landing page), something local that can be configured 
dynamically and used by the author for storing of non-critical information. Implementation of the JavaScript application
could be envisioned with AngularJS. Django can be repurposed to serve as the "business" administration application,
with an exposed REST API for some extended functionality if the need is there.
* Implementation of E-Commerce tools available to allow users to embed products onto their landing page - this may involve
allowing users to configure a service such as Yahoo Commerce, Paypal, etc., for quick purchases. While the landing page is targeted to businesses for promotion, it would be nice to be able to use this framework for creating a one-off page with
an embedded E-Commerce component (an example might be a landing page which, while is promotional, might be promoting
something such as a book or other media that is specific to the business' campaign, allowing users to shop within the
context of the landing page itself, keeping all promotion and purchases related to that promotion centralized. As links
to larger E-Commerce sites might prove useful (e.g., View on Amazon), the ability to embed the E-Commerce component might
be kinda sweet.
* Integrate ANALYTICS!!! Not sure if this was done. It's been over 6 years. When building a page, a user should be able to add tracking code for events and page views at the very least!
* And so, so much more... In writing this, I almost feel obligated to implement the above and open a new repository to
share with the world.


