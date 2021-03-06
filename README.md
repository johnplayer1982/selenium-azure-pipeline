# Money Helper Selenium Tests

These tests are designed to run on a remote browser kicked off by an azure pipeline.

## Running tests locally

To run tests locally:

- Install python
- Clone the repo
- CD into the prohect root ``cd selenium-azure-pipeline``
- Install the requirements ``pip install -r requirements.txt``
- CD into the Regression folder ``cd Regression``
- Run local file ``python local.py`` 

## Common pipeline errors:

```Message: CBT Error: A new session could not be created.```

This is a failure on the Cross browser testing end, it means that a browser session could not be created.  Occurs quite rarely and not a code or test issue.

## Safari

If writing tests, please consider the following for safari:

- Colour opacity is assumed, for example the colour of an element in Chrome includes the opacity: ``rgba(255, 255, 255, 1)`` whereas the opacity isnt returned in Safari: ``rgb(255, 255, 255)``.  To prevent test issues, when asserting colour, rather than using ``assert element.value_of_css_property('color') == rgba(255, 255, 255, 1)`` use ``assert "255, 255, 255" in element.value_of_css_property('color')``
