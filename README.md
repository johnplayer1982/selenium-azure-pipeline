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
