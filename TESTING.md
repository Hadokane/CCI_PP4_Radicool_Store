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

**Passes Testing:** Here we created a new user account with a test email from [Temp Mail](https://temp-mail.org/en/) successfully. Email Verification was carried out successfully.

<details><summary>Sign Up - Quality check</summary><img src="docs/testing/signup_test/2.png" alt="Sign Up"></details>

<details><summary>Sign Up - Test</summary><img src="docs/testing/signup_test/verify-email.png" alt="Sign Up 2"></details>

<details><summary>Sign Up - Email Verification Required</summary><img src="docs/testing/signup_test/verify-email2.png" alt="Sign Up 3"></details>

<details><summary>Sign Up - Email Received</summary><img src="docs/testing/signup_test/verify-email3.png" alt="Sign Up 4"></details>

<details><summary>Sign Up - Email Confirmation</summary><img src="docs/testing/signup_test/verify-email4.png" alt="Sign Up 5"></details>

<details><summary>Sign Up - Email Verified</summary><img src="docs/testing/signup_test/verify-email5.png" alt="Sign Up 6"></details>

**Additional Testing Passed:**

- A user is warned of incorrect or insecure data when signing up through Django AllAuth & Alert messages.

- The user is sent an email allowing them to authenticate their account.

- Once authenticated a user is able to sign in to their account.

- This is a responsive, positive user experience, with informative prompts and interactive elements to guide the user.

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

- The user is shown a confirmation page.

- The order appears within the users profile and is accessible.

- A confirmation email is sent.

<details><summary>Checkout - Test</summary><img src="docs/testing/signup_test/6.png" alt="Checkout - Test"></details>

---
