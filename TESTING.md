# Testing

Here we will document the numerous testing and validation methods taken to ensure Radicool functions as intended while providing a positive, accessible user experience:

---

## Contents

---

- [Code Validation](#code-validation)
    - [W3C HTML Validator](#w3c-html-validation) 
    - [W3C CSS Validator](#w3c-css-validation)
    - [JSHint Validator](#jshint-validation)
    - [CI Python Linter](#CI-Python-Linter)
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

<details><summary>W3C HTML Validation - Errors</summary><img src="" alt="W3C HTML Errors Screen"></details>

Using these results, I:

- Refactored the deleteModal by moving it outside of Django if/or statements and deleting duplicates. Calling the modal from the HTML body rather than from within the statements.

- Placed modal at the top of the HTML body inline with [Bootstrap Document](https://getbootstrap.com/docs/4.0/components/modal/#:~:text=Whenever%20possible%2C%20place%20your%20modal,using%20modals%20on%20mobile%20devices.) guidance.

- Removed redundant `Section` tags.

- Fixed Header hierarchy.

- Refactored `Featured Item` Cards to remove duplicate/redundant code.

```

Modals use position: fixed, which can sometimes be a bit particular about its rendering. Whenever possible, place your modal HTML in a top-level position to avoid potential interference from other elements. You’ll likely run into issues when nesting a .modal within another fixed element.

```

- a

<details><summary>W3C HTML Validation - Pass</summary><img src="officechampion/static/assets/images/docs/validation/w3c_html2.png" alt="W3C HTML Pass Screen"></details>

---

## W3C CSS Validation

- [W3C CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator/)

Next, I carried out validation of the CSS file by running the page through W3C CSS Validation Service - Jigsaw.

<details><summary>W3C CSS Pass</summary><img src="officechampion/static/assets/images/docs/validation/w3c_css.png" alt="W3C CSS Pass Screen"></details>

The results came back successful.

---

## JSHINT Validation

- [JSHint Validator](https://jshint.com/)

I utilised JSHint as a validation tool to help detect if there were any errors or potential problems within my JavaScript code.

<details><summary>JSHint Validation</summary><img src="officechampion/static/assets/images/docs/validation/jshint.png" alt="JSHint Validation"></details>

- The undefined variables were all required by Materialize's inbuilt components to initialise forms and other components.

- The removeNode function is called from within HTML pages whenever an alert is clicked by the user. This allows users to close alert pop-ups.

---

## CI Python Linter

- [Code Institute Python Linter - Pep8 Validator](https://pep8ci.herokuapp.com/)

I used Code Institute's Python Linter to check the validity of my code based on Pep 8 styling standards.

I ran each Python page individually through the linter. With each returning a result of: "All clear, no errors found."

<details><summary>Python Lint for - "__init__.py"</summary><img src="officechampion/static/assets/images/docs/validation/ci_init.png" alt="Python Lint Results #1"></details>
<details><summary>Python Lint for - "models.py"</summary><img src="officechampion/static/assets/images/docs/validation/ci_models.png" alt="Python Lint Results #2"></details>
<details><summary>Python Lint for - "routes.py"</summary><img src="officechampion/static/assets/images/docs/validation/ci_routes.png" alt="Python Lint Results #3"></details>
<details><summary>Python Lint for - "run.py"</summary><img src="officechampion/static/assets/images/docs/validation/ci_run.png" alt="Python Lint Results #4"></details>

---

## Wave Validator

- [Wave Web Accessibility Evaluation Tool](https://wave.webaim.org/)

This was used to check that the Office Champion website was accessible to as many individuals' needs as possible.

On an initial scan, I discovered the following accessibility errors:
- The Materialize default of white text on an amber background was actually being flagged as a contrast issue.
- Underlining being used on page headers wasn't the best practice. A user could easily mistake this for a hyperlink.
- The home button contained the same link as the adjacent "Office Champions" Hero Image, that was included in the navbar. Repeating adjacent links seemed unnecessary to Wave.

<details><summary>Wave Error #1</summary><img src="officechampion/static/assets/images/docs/validation/wave1.png" alt="Wave Error #1"></details>

<details><summary>Wave Error #2</summary><img src="officechampion/static/assets/images/docs/validation/wave5.png" alt="Wave Error #2"></details>

To fix the above issues:
- I recoloured all menu and navigation text to black. Providing adequate contrast for users.
- I removed all underlining throughout the website's headers.

I also decided to keep the "redundant" additional navigation link of "home". My reasoning is that most users will expect the navbar icon to take them home as this is an extremely common feature across numerous websites. The addition of the written "home" button will provide a means of getting to the home page for users without this expectation without harming the website or other users.

After carrying out the above steps, Office Champion passed Wave validation.

<details><summary>Wave Validation Pass</summary><img src="officechampion/static/assets/images/docs/validation/wave4.png" alt="Wave Validation Screen #4"></details>

---

## A11y Contrast Validator

- [A11y Color Contrast Accessibility Validator](https://color.a11y.com/Contrast/)

This was used to ensure the website's colour contrast met WCAG 2.1 Guidelines.

An initial check showed that the burger menu icon on the side-nav bar was a contrast issue. I recoloured this icon from white to black, fixing the issue.

<details><summary>A11y Validation Pass</summary><img src="officechampion/static/assets/images/docs/validation/a11y_val.png" alt="A11y Validation Screen"></details>
