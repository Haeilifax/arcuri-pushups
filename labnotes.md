# Lab Notebook

## 2026-01-07

Starting a little late on this -- we threw this together in a morning, a very free flowing and easy experience. Got it to 1.0 basically immediately, and it's in active use

Goal of this is a fun little pushup tracker for my family to use for this year (2026) -- we (those of us participating) each have the goal of 10,000 pushups by the end of the year

Now we're going to update to be able to notify users when someone posts pushups

The original thought was to do SMS messaging (with a side of possibly WhatsApp?)

After reviewing AWS's SMS via SNS offering, we decided against that
- Varying set-up costs, some decent, some exorbitant, but more than I want to pay
  - 10 digit long code (10DLC) -- something like $60
  - Toll-free -- not sure, might be minimal, but it's fishy that they don't mention it
  - Short codes -- like 650??????
- Monthly recurring costs as well -- I'm not against paying something for my side projects, but I'd like it to stay in the <5/mo tier
  - 10DLC and toll free -- like 4/mo
  - Short Codes -- like $1000?????
- And then pay-as-you-go costs, which are totally reasonable and I'd love to only pay them
  - Like .5 cents per text

Checked Twilio, which in addition to having monthly costs that I wouldn't much mind, also has a lower limit of $20 to fund the account, which means an upfront cost of $20, which I'm not interested in paying, as well as monthly costs of ~$1.15/mo

Checked Whatsapp directly -- this has potential, but Meta wants you to sign up as a business with them, or you use one of the redistributers of the Whatsapp api, and all of this is just annoying and ridiculous

Considered a few other options, like Sinch, but nothing was going to really get around "I need a phone number", which will cost money.

One option to get around "I need a phone number" would be to use my phone remotely via one of any number of packages, and text direct from my phone. The issue is that I like my phone number, and carriers don't like this -- they'll ban your number for using automation. Could probably get away with it anyway, because it's so low volume, but the risk is too high (getting a new number would be such a hassle)

My current thought is to use Push notifications to serve the same purpose, for free.

Req's for push notifications:
Installed App (PWA or Native) for background notifications
Notifications in the App
Push in the app (for background)

Decided to go with PWA because I don't really know how to make a native app (Claude non-withstanding), and because it'll be easy to distribute

So I need to:
- Upgrade my website to a PWA
- Add Notifications to my website
- Add Push capabilities to my website

MDN docs on PWAs: https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps

Random Medium article on it: https://medium.com/@gxgemini777/complete-guide-to-implementing-background-push-notifications-in-pwas-d36340a06817

Making PWAs installable:

https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable

WebApp Manifest:
- name or short_name
- icons must contain a 192px and a 512px icon
- start_url
- display and/or display_override
- prefer_related_applications must be false or not present

Served using HTTPS (or a couple dev options)

So we need icons -- having ChatGPT make them, we'll see how it goes

We'll also need to make this manifest file -- I wonder how easy it would be to just plug in flask here, so I can stop my stupid, ad-hoc, if-elif based routing system.

Annnnd that's it -- So, we just need icons and a manifest file? Seems super easy.

I'm going to add Flask -- that's one of the key techs people ask for pretty often

Flask Documentation / Flask Docs : https://flask.palletsprojects.com/en/stable/

God I hate everything and everyone. I just wanna know how to connect event and context to flask, and convert the response to one I can use.

Okay, nope, this is dumb and I'm going to only use Flask / Django on an actual machine with an actual webserver. There are only bad options here for converting between the Lambda event and context and the wsgi environment, and the response from the flask app

We're gonna take a quick peek for alternative routing tech, and then we're just gonna go.

That's enough, we're building it ourselves

So what does routing look like?

- Be able to register routes on functions (that's how everyone else does it)
- Run a single router that passes down the event and context to the correct function

Simple as pie, a little stupid that I didn't start wtih this.

We're going to create a registrars dict, and have a registration decorator function that will take in a method and a route, and select the correct function to run.

Then, we're going to have a main function function that just calls the router, passing in event and context.

Should we make the router the main function, the lambda_handler? No, because we want this to be a little bit modular -- I'm envisioning a future where this is broken out, because it's a useful and usable library on its own
