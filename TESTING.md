# Testing

Here we will document the numerous testing and validation methods taken to ensure Radicool functions as intended while providing a positive, accessible user experience:

---

## Contents

---

- [Code Validation](#code-validation)
  - [W3C HTML Validator](#w3c-html-validation) 
  - [W3C CSS Validator](#w3c-css-validation)
  - [JSHint Validator](#jshint-validation)
  - [Flake8 Linter](#flake8-python-linter)
  - [Wave Validator](#wave)
  - [Lighthouse](#lighthouse)
- [Testing User Stories](#testing-user-stories)
  - [First Time User](#first-time-user)
  - [Returning User](#returning-user)
  - [Website Owner](#website-owner)
- [Bugs](#bugs)

Return to [README.md ↑](/README.md#testing)

---

# Code Validation

This section will cover the automated testing procedures undertaken and justifies design decisions made during the creative processes undertaken.

---

## W3C HTML Validation

---

-  [W3C HTML Validator](https://validator.w3.org/)

  - <details><summary>W3C HTML Validation - Errors</summary><img src="docs/testing/w3html1.png" alt="W3C HTML Errors Screen"></details>

**80 Total suggestions were returned. Using these results, I:**

- Refactored the deleteModal by moving it outside of Django if/or statements and deleting duplicates. Calling the modal from the HTML body rather than from within the statements.

- Placed modal at the top of the HTML body inline with [Bootstrap Document](https://getbootstrap.com/docs/4.0/components/modal/#:~:text=Whenever%20possible%2C%20place%20your%20modal,using%20modals%20on%20mobile%20devices.) guidance.

```

Modals use position: fixed, which can sometimes be a bit particular about its rendering. Whenever possible, place your modal HTML in a top-level position to avoid potential interference from other elements. You’ll likely run into issues when nesting a .modal within another fixed element.

```

- Removed redundant `Section` tags.

- Fixed Header hierarchy.

- Refactored `Featured Item` Cards to remove duplicate/redundant code.

- <details><summary>W3C HTML Validation - Home Pass</summary><img src="docs/testing/w3html2.png" alt="W3C HTML Pass Screen"></details>

- <details><summary>W3C HTML Validation - Products Pass</summary><img src="docs/testing/w3html3.png" alt="W3C HTML Pass Screen"></details>

- <details><summary>W3C HTML Validation - Checkout Pass</summary><img src="docs/testing/w3html4.png" alt="W3C HTML Pass Screen"></details>

---

## W3C CSS Validation

- [W3C CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator/)

- <details><summary>W3C CSS Validation </summary><img src="docs/testing/w3css.png" alt="W3C HTML Pass Screen"></details>

**1 "Error" was returned.**

This error is a false flag, as proven by this article from [W3Schools](https://www.w3schools.com/cssref/css_pr_scale.php) explaining how to use the scale property and providing "%" as a valid input, also stating that:

```
Note: An alternative technique to scale an element is to use CSS transform property with CSS scale() function.
The CSS scale property, as explained on this webpage, is arguably a simpler and more direct way to scale an element.
```

[Mig281](https://github.com/validator/validator/issues/1091) in a GitHub discussion explains that the validator expects this instead:

```
#foo, .bar {
  transform: scale(0.8);
}

The MDN docs do state:
The scale CSS property allows you to specify scale transforms individually and independently of the transform property. This maps better to typical user interface usage, and saves having to remember the exact order of transform functions to specify in the transform value.
```

As shown here this is an issue with the validator not recognising this "newer" CSS property rather than an issue with my CSS code.

I am satisfied with the results of this validation and consider it to be passed, as I have used a more efficient method for my use-case than the suggested "fix".

---

## JSHINT Validation

- [JSHint Validator](https://jshint.com/)

I utilised JSHint as a validation tool for the "Checkout.JS" file. Which contains all of the projects internal JS used for Stripe and payment handling. The validator passed Radicool's JS.

  - <details><summary>JSHint Validation</summary><img src="docs/testing/jshint.png"></details>

---

## Flake8 Python Linter

- [Flake8 Validator](https://pep8ci.herokuapp.com/)

This was ran internally using GitPod's CLI.

Initially a number of formatting errors were shown:

  - <details><summary>Initial Python Lint</summary><img src="docs/testing/flake8.png" alt="Python Lint Results #1"></details>

Upon refactoring, Radicool passed the Python Linting process. 

  - <details><summary>Python Linting - Pass</summary><img src="docs/testing/flake8pass.png" alt="Python Lint Results #2"></details>

The entire project was inserted into a file and checked. This was to avoid false flags from other frameworks or plugins beyond my control.

---

## Wave Validator

- [Wave Web Accessibility Evaluation Tool](https://wave.webaim.org/)

This was used to check the accessibility of Radicool in meeting individual user needs.

included in the navbar. Repeating adjacent links seemed unnecessary to Wave.

  - <details><summary>Wave Error #1</summary><img src="docs/testing/wave1.png" alt="Wave Error #1"></details>

Improvements-made:

- `sr-only` label added to `search_bar` for screen-reader use.

- `sr-only` span elements added inside of empty links that use icons as their context rather than text, such as the social links in the footer.

After carrying out the above steps, Radicool passed Wave validation.

  - <details><summary>Wave Validation Pass</summary><img src="docs/testing/wave2.png" alt="Wave Validation"></details>

As justification for the remaining contrast errors and alerts:

- Alerts are referring almost entirely to "redundant links" but I feel a user would expect multiple elements within the same card to lead to that cards `info` html page. As such these have been left in to provide a better user experience, as they cause no issues to the website.

- Contrast errors are all in reference to white text appearing on the Radicool green. This is a similar colour convention's used by world renowned brands such as: Subway, Asda, Starbucks and Xbox. I am confident users will have no issue interacting with these elements and have ensured it is only used on elements that are not-integral to a users purchase journey such as sort buttons and a website banner.

---

## Lighthouse

- [Google Chrome Lighthouse Validator](https://developer.chrome.com/docs/lighthouse/overview/)

Google Lighthouse was used to run performance, accessibility & SEO audits of Radicool.

<details><summary>Lighthouse Initial Check - Desktop</summary><img src="docs/testing/lighthouse1.png"></details>

The performance results were concerning, to improve this statistic and raise scores the following was done:

- `<Meta>` tags were added to the base template's head to improve the SEO potential of Radicool.

- Stripe JS was moved to the checkout page where it was required instead of being ran from the Base template.

- Replaced images within the Amazon Bucket. Changing .jpg's and .png's into .webp images using [Cloud Convert](https://cloudconvert.com/). Boosted "Home" Performance to 56%.

- Navbar links coloured darker and made bolder.

- Javascript moved to base template footer from head.

- Hero Image pre-loaded within the HTML.

After implementing all of the above changes there was only a marginal shift in my Performance score.

<details><summary>Lighthouse Desktop</summary><img src="docs/testing/lighthouse-desktop.png"></details>

<details><summary>Lighthouse Mobile</summary><img src="docs/testing/lighthouse-mobile.png"></details>

Running a test on the same project locally instead gave these results.

<details><summary>Lighthouse Local Desktop Check</summary><img src="docs/testing/lighthouse-local-test.png"></details>

With the above in mind I feel as though I've done what I can to improve the scores & that further improvements to "Performance" would require me to purchase and upgrade my subscriptions to either Heroku, Railway or - most likely - Amazon's services.

With that in mind, I am happy with the above results and feel this testing process has dramatically improved the overall speed and best practice across the Radicool E-commerce store. Images have been drastically condensed in file-size, the order of elements and frameworks loading has been improved and sped-up.

All-in-all a better user-experience has been achieved. 

[Back to Top ↑](#testing-document)

---

# Device Testing

The website was tested and functioned as expected on the following devices:

- Novatech LTD. AMD Ryzen 7 3800x, 32GB Desktop
- Lenovo IdeaPad 5 Pro
- Samsung Galaxy S20 & S21
- Samsung Galaxy Tab S7
- MacBook Air with M1 chip
- iPhone 11, 13 & 14
- iPad Air
- Samsung Chrome Book

The website has been tested on up-to-date versions of the following browsers:

- Microsoft Edge
- Google Chrome
- Chrome for android
- Mozilla Firefox
- Opera
- Safari
- Internet Explorer
- Duck Duck Go

The website has also been tested on monitors of 16:9, 16:10 and 21:9 resolutions.

[Back to Top ↑](#testing-document)

---

# Manual Testing

Manual testing played a crucial role in the development of this  project.

It has been carried out at each step of development through the use of Chrome Dev Tools, family & friends user tests and by asking and solving questions about the sites functionality in order to find any additional development oversights.

Once the project had reached its developmental conclusion I compiled a list of main concerns that would need to be passed to confirm the site worked as intended. Through this methodology, I can ensure that I've satisfied my project brief and provided a fully functional full-stack website, fit for consumption by multiple users.

---

1. Can users create a new account?

Here we created a new user account with a test email from [Temp Mail](https://temp-mail.org/en/) and attempt to sign up to Radicool.

**Passes Testing:**

- A user is warned of incorrect or insecure data when signing up through Django AllAuth & Alert messages.

- The user is sent an email allowing them to authenticate their account.

- Once authenticated a user is able to sign in to their account.

- This is a responsive, positive user experience, with informative prompts and interactive elements to guide the user.

<details><summary>Sign Up - Quality check</summary><img src="docs/testing/signup_test/2.png" alt="Sign Up"></details>

<details><summary>Sign Up - Test</summary><img src="docs/testing/signup_test/verify-email.png" alt="Sign Up 2"></details>

<details><summary>Sign Up - Email Verification Required</summary><img src="docs/testing/signup_test/verify-email2.png" alt="Sign Up 3"></details>

<details><summary>Sign Up - Email Received</summary><img src="docs/testing/signup_test/verify-email3.png" alt="Sign Up 4"></details>

<details><summary>Sign Up - Email Confirmation</summary><img src="docs/testing/signup_test/verify-email4.png" alt="Sign Up 5"></details>

<details><summary>Sign Up - Email Verified</summary><img src="docs/testing/signup_test/verify-email5.png" alt="Sign Up 6"></details>

---

2. Can users login on their verified accounts?

**Passes Testing:** Alerts tell the user of issues preventing login. The user is able to login to the website with the correct information.

<details><summary>Login - Test</summary><img src="docs/testing/signup_test/6.png" alt="Sign Up 7"></details>

<details><summary>Login - Warning</summary><img src="docs/testing/signup_test/7.png" alt="Sign Up 8"></details>

<details><summary>Login - Success</summary><img src="docs/testing/signup_test/8.png" alt="Sign Up 9"></details>

---

3. Does a "Brand Account" user have C.R.U.D. functionality from the Front-End?

For this test:

- The user "Test" was given a "Brand Account" group class within Django Admin.

- The user "Test2" serves as a standard user account.

**Passes Testing:** 

- The Brand Account user is able to access a limited version of the Admin section from the Front-End. Viewing order history and having C.R.U.D. functionality over Merchandise.

- They can perform C.R.U.D. functionality from the Front-End via the "Add" & "Edit" pages.

- They are able to Delete products from the Front-End via a defensively designed delete modal.

- Regular users are blocked from accessing Brand Account only pages if they navigate to the URL directly and are informed of this by Alerts.

<details><summary>Brand Account - Assigning group</summary><img src="docs/testing/brand_account/a_create.png" alt="Assigning group"></details>

<details><summary>Brand Account - Brand footer</summary><img src="docs/testing/brand_account/a_footer.png" alt="Brand footer"></details>

<details><summary>Brand Account - Navbar</summary><img src="docs/testing/brand_account/a_dropdown.png" alt="Brand Navbar"></details>

<details><summary>Brand Account - Card footer</summary><img src="docs/testing/brand_account/a_card.png" alt="Card footer"></details>

<details><summary>Brand Account - Add Page</summary><img src="docs/testing/brand_account/a_add.png" alt="Add Page"></details>

<details><summary>Brand Account - Edit Page</summary><img src="docs/testing/brand_account/a_edit.png" alt="Edit Page"></details>

<details><summary>Brand Account - Delete Page</summary><img src="docs/testing/brand_account/a_dlt.png" alt="Delete Page"></details>

<details><summary>Brand Account - Admin</summary><img src="docs/testing/brand_account/a_admin.png" alt="Admin"></details>

<details><summary>Standard User - Sign in & Navbar</summary><img src="docs/testing/brand_account/s_signin.png" alt="Sign in"></details>

<details><summary>Standard User - Redirect Message</summary><img src="docs/testing/brand_account/s_msg.png" alt="Redirect"></details>

---

4. Can users add items to their cart?

**Passes Testing:** 

- Users are able to add items to their cart and this is reflected by the live updating cart in the top right of the site.

- The cart functions as expected by updating it's subtotal and quantity.

- Button text provides live positive feedback.

<details><summary>Cart - Add Test</summary><img src="docs/testing/cart_test/add1.png" alt="Cart - Add Test"></details>

<details><summary>Cart - Added</summary><img src="docs/testing/cart_test/add2.png" alt="Cart - Added"></details>

---

5. Can users edit items within their cart?

**Passes Testing:** 

- Users are able to remove items from the cart via interactive buttons.

- The totals dynamically update to inform the user of shipping costs, sub totals for each item and the carts grand total.

- Size and quantity can be updated for each item dynamically within the cart.

- Button text provides live positive feedback for update. Page refreshes on removal.

<details><summary>Cart - Test</summary><img src="docs/testing/cart_test/cart.png" alt="Cart - Test"></details>

<details><summary>Cart - Remove</summary><img src="docs/testing/cart_test/remove.png" alt="Cart - Remove"></details>

<details><summary>Cart - Update</summary><img src="docs/testing/cart_test/update.png" alt="Cart - Update"></details>

<details><summary>Cart - Updated</summary><img src="docs/testing/cart_test/update2.png" alt="Cart - Updated"></details>


---

6. Can users checkout and complete a purchase?

**Passes Testing:** 

- The user can enter and save their information to their profile.

- Stripe payment is accepted.

- Stripe Webhooks are received.

- The user is shown a confirmation page.

- The order appears within the users Profile under Order History and is viewable.

- A confirmation email is sent to the user.

- Users can save delivery information in their Profile, that is then called in the Checkout.

<details><summary>Checkout - Test</summary><img src="docs/testing/checkout_test/ch1.png" alt="Checkout - Test"></details>

<details><summary>Checkout - Info Entered</summary><img src="docs/testing/checkout_test/ch2.png" alt="Checkout - Info Entered"></details>

<details><summary>Checkout - Confirmed</summary><img src="docs/testing/checkout_test/ch3.png" alt="Checkout - Confirmed"></details>

<details><summary>Checkout - Email Received</summary><img src="docs/testing/checkout_test/ch4.png" alt="Checkout - Email Received"></details>

<details><summary>Checkout - Email Contents</summary><img src="docs/testing/checkout_test/ch5.png" alt="Checkout -  Email Contents"></details>

<details><summary>Checkout - Order History</summary><img src="docs/testing/checkout_test/ch6.png" alt="Checkout - Order History"></details>

<details><summary>Profile - Past Order</summary><img src="docs/testing/checkout_test/chpast.png" alt="Profile - Past Order"></details>

<details><summary>Profile Info - Test</summary><img src="docs/testing/checkout_test/prof1.png" alt="Profile Info - Test"></details>

<details><summary>Profile Saved</summary><img src="docs/testing/checkout_test/prof2.png" alt="Profile Saved"></details>

<details><summary>Checkout - Calls Profile Info</summary><img src="docs/testing/checkout_test/prof3.png" alt="Checkout - Calls Profile Info"></details>

<details><summary>Stripe- Success</summary><img src="docs/testing/checkout_test/stripe.png" alt="Stripe- Success"></details>

---

7. Can users use their Wish List?

**Passes Testing:** 

- The user is able to add & remove items from their wish list.

- The correct buttons display by items to show the user if they are within their list or not.

- Merchandise on the wish list page link correctly to their `info` pages when interacted with.

- The user has front-end C.R.U.D. functionality over their wish list.

- Unauthorised users are directed to the sign up page, thus being incentivised to sign up for Radicool's services.

- Toast Alerts provide positive feedback for users.

<details><summary>Wish List - Empty</summary><img src="docs/testing/wishlist_test/1.png" alt="Wish List - Empty"></details>

<details><summary>Wish List - Add</summary><img src="docs/testing/wishlist_test/2.png" alt="Wish List - Add"></details>

<details><summary>Wish List - Add Alert</summary><img src="docs/testing/wishlist_test/3.png" alt="Wish List - Add Alert"></details>

<details><summary>Wish List</summary><img src="docs/testing/wishlist_test/4.png" alt="Wish List"></details>

<details><summary>Wish List - Remove</summary><img src="docs/testing/wishlist_test/5.png" alt="Wish List - Remove"></details>

<details><summary>Wish List - Saved between sessions, browsers and devices.</summary><img src="docs/testing/wishlist_test/6_sesh.png" alt="Wish List - Sessions"></details>

---

8. Can Guests checkout?

**Passes Testing:** 

- Guests are able to checkout and receive confirmation emails the same as regular users.

<details><summary>Checkout - Guest</summary><img src="docs/testing/checkout_test/ch_g1.png" alt="Checkout - Guest"></details>

<details><summary>Checkout - Guest Email Received</summary><img src="docs/testing/checkout_test/ch_g2.png" alt="Checkout - Guest Email Received"></details>

<details><summary>Checkout - Guest Email</summary><img src="docs/testing/checkout_test/ch_g3.png" alt="Checkout - Guest Email"></details>

---

**Additional Tests:** 

- Users are able to sign in on multiple devices.

- Alert Toasts can be closed by clicking them.

- Users cannot see other users' data.

[Back to top ↑](#testing_document)

---

# Testing User Stories

Here we will test our previously defined user goals by providing and acknowledging evidence that shows they are met by the current deployed project.

---

## First-time User

**As a First-Time user, I want to:**

| ID      | GOAL          | GOAL MET? (X=MET)      |
| -------------|:-------------:|:-------------:|
| A1           | Browse Merch on the website          | X |
| A2           | Search for Merchandise directly      | X |
| A3           | Add items to Cart   | X |
| A4           | View my Cart     | X |
| A5           | Edit my Cart    | X |
| A6           | Checkout as Guest    | X |
| A7           | Receive Order Confirmations  | X |
| A8           | Have a reason to sign up | X |
| A9           | Create an account | X |
| A10          | Access the site on different devices | X |

- A1 is met by the Products, Categories & Collections pages.
- A2 is met by the above & the search bar function.
- A3-A5 is met by the Cart section and proven in earlier testing.
- A6-A7, A9 & A10 are proven in the above Manual Testing section.
- A8 is met by the website featuring the Wish List & Profile section of the website.

---

## Returning User

**As a Returning user, I want to:**

| ID      | GOAL          | GOAL MET? (X=MET)      |
| -------------|:-------------:|:-------------:|
| B1           | Login to my account          | X |
| B2           | Save my Cart between sessions     | X |
| B3           | Save my information for faster purchases  | X |
| B4           | View my Order History    | X |
| B5           | Save items to a Wish List    | X |

- B1-B5 are all met and proven in the above Testing section.
- B2 the Cart is saved in the user's session remaining on the same device and browser.
- The Wish List & Order History is saved across all devices.

---

## Brand User

**As a Brand user, I want to:**

| ID      | GOAL          | GOAL MET? (X=MET)      |
| -------------|:-------------:|:-------------:|
| C1           | Add items to the store          | X |
| C2           | Add Categories & Collections    | X |
| C3           | View Users' Order History  | X |
| C4           | Update items within the store    | X |
| C5           | Remove items from the store    | X |

- C1-C5 are all met and proven in the above Testing section.
- Functionality is provided on the Front-End through the `Add` & `Edit` pages.
- They are able to view users order history within their Admin section.

---

## Site Admin

**As the Site Admin, I want to:**

| ID      | GOAL          | GOAL MET? (X=MET)      |
| -------------|:-------------:|:-------------:|
| D1           | Have the same C.R.U.D. functionality as Brands | X |
| D2           | View & manage User Accounts    | X |
| D3           | View & manage Orders  | X |
| D4           | Receive Stripe payments   | X |
| D5           | Ensure site users have their expected experiences  | X |

- D1 & D5 are met by the above section goals being met.
- D2 & D3 are achievable through Django's Admin pages.
- D4 is proven in the above Manual Testing section.

---

I am confident that the above examples further substantiate the evidence provided in the previous "Plane Analysis" sections and will be strengthened further by the following "Testing" sections. 

I have substantial reason to declare all user and site-owner stories met.

[Back to top ↑](#testing_document)

---

# Bugs

Over the course of this project, I encountered numerous bugs that either impacted the functionality or design of the website and needed to be fixed.

## Chrome Dev Tools

Chrome Dev Tools served as one of my most important methods of debugging from start to finish. It allowed me to find numerous errors in the code such as: 

- Noticing discrepancies in my `<div>` arrangements and classes and ordering them correctly so that elements opened and closed when they should have.

- Test out the inline styles on numerous elements before committing those changes to CSS.
    - Used heavily while deciding on card designs.

- See if an object had unintentional padding or margins being applied to it by default Materialize classes and remove/add where necessary.

- Diagnose numerous bugs and hierarchical code issues present throughout the project.

- See additional "issues" that may impact the performance of my project or stop it from meeting best practice guidelines.

---

### BUG #1

---

**Bug:** Index Promo cards squished and unreadable on smaller devices.

<details><summary>Bug 1</summary><img src="" alt=""></details>

**Fix:** I realised I needed to change the default Materialize column class to make it responsive on smaller devices. Set it to display single cards on smaller devices and rows of 2 and 3 on larger screens.

<details><summary>Bug 1 - Fix</summary><img src="" alt="Bug 1 Fix"></details>

---

## Known Bugs

---

If a User refreshes the Order Confirmation page it will resend the Confirmation email.

This is a minor issue that would only effect a very small subset of users, that happen to refresh their order confirmations.

A warning has been added to the bottom of Confirmation Emails to inform the user that if they receive multiple emails with the same order number, that they haven't been billed more than once.

This is a satisfactory - yet temporary - solution and something I would look to improve upon in future builds of this project.

[Back to Top ↑](#testing-document)

[Return to README.md ↑](/README.md#testing)