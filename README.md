TODO APPLICATION

This project implemenents an application that allows a user to create todo items that are stored locally.

Features Implemented:


TEAM
KupoKopu - Developer, Tester, Project manager
luyah231 - Developer, Tester

TOOLS
Version Control
- Git

Project management
- Jira

Testing
- unittest

Framework
- Flask (general application)
- sqlalchemy (database)

development environment
- Visual Studio Code

extensions
- Python (for general language support and integrations including linting)

linting
- autopep8

INSTRUCTIONS
- have python installed with pip (developed and tested with python 3.12.0)
- install flask `pip install flask`
- clone repo
- go in to terminal at root of repo
- run the app `flask run`
- a browser tab to localhost that the app will be running in will show up or enter the localhost url in the command line into your browser

DEV INSTRUCTIONS
- have python installed with pip (developed and tested with python 3.12.0)
- install flask `pip install flask`
- install autopep8 `pip install autopep8`
 - project already has workspace settings for auto-formatting via autopep8
- clone repo
- go in to terminal at root of repo
- run the app `flask run`
- a browser tab to localhost that the app will be running in will show up or enter the localhost url in the command line into your browser

PROJECT WORKFLOW
using kanban board and backlog. Create tickets in backlog and take them up into sprint.
Assign tickets, develop features in branches and put up a pull request to be reviewed.

TEST METHODOLOGY
Test Driven Development.

Create unit tests with happy path for ticket, code till happy path is achieved.
Create other unit tests to deal with edge case scenarios like errors, wrong input.

When in submitting a pull request, share a screenshot of unit test results.

Code reviews
Use code reviews to assess code against coding best practices. Approve the pull request or comment any improvements.

CODING BEST PRACTICES
- Write Readable and meaningful code
 - 'calculate_total' is more descriptive than 'calc'
- Use snake_case for variables and camelCase for class names
- Write modular code, if it is reusable then it should be it's own method/function
- Group related functions and classes
- Use Logging rather than print statements for logging runtime information
- Use specific exception types when throwing and handling errors
- Inline comments are for why an approach is taken, not what it does
- Docstring to describe the purpose of the function, class or module
- follow PEP 8 Style Guide
 - Indentation: Use 4 spaces per indentation level.
 - Line Length: Limit all lines to a maximum of 79 characters.
 - Blank Lines: Separate top-level function and class definitions with two blank lines. Use single blank lines to separate method definitions inside a class.
 - Imports: Import all modules at the beginning of the file, usually in three groups: standard library imports, related third-party imports, and local application/library-specific imports.
 - and much more...
 - this can be easily done with autopep8 automatic linting

CI PIPELINES
Using Github Actions to perform tests on pull request.

STANDARDS
IEEE 730
Standard for a Software Quality Assurance (SQA) plan.
Objective is to ensure software meets it's requirements and is of quality by defining systematic processes, tasks and responsibilities to ensure quality.

Reasons to following this Standard:
- Widely accepted industry standard
- flexible and scalable from small to big projects
- Encourages continuous imrpovement by aligning with agile and iterative development

To meet this standard the project will:
- assign roles and responsibilities
- implement processes to verify and validate the application through unit testing and end to tend testing
- manage risk by implementing a plan for implementation of the project

PERFORMANCE AND ACCESSIBILITY AUDITS
