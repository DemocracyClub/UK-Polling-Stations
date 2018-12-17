# Contributing

At [DemocracyClub](https://democracyclub.org.uk/) we value contributions to our projects from volunteers and contirbutors. Please read and follow our [Code of Conduct](https://democracyclub.org.uk/code-of-conduct/).

## Issues
* To report a bug or suggest an improvement, [create an issue](https://github.com/DemocracyClub/UK-Polling-Stations/issues/new).
* Clearly describe the issue including steps to reproduce if it is a bug.

## Pull Requests
* If you are interested in helping out, issues tagged as [recommended for beginners](https://github.com/DemocracyClub/UK-Polling-Stations/issues?q=is%3Aopen+is%3Aissue+label%3A%22recommended+for+beginners%22) or [help wanted](https://github.com/DemocracyClub/UK-Polling-Stations/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22) are the best place to start.
* Fork the repository on GitHub.
* Create a topic branch on your fork of the repository.
* Make commits of logical units.
* Use descriptive commit messages.
* Check your work against our test suite. You can run tests locally using:
    * `pytest` (unit tests) and
    * `python manage.py harvest` (acceptance tests)
    or enable [travis-ci](https://travis-ci.org/) for your fork, so the tests will be executed after a `push`.
* Check your work against our coding standards. We use [pyflakes](https://github.com/PyCQA/pyflakes) for linting and [black](https://github.com/ambv/black) for code formatting:
     * `pytest --flake` (lint with pyflakes)
     * `black .` (auto-format with black)
* Push your changes to a topic branch in your fork of the repository.
* Submit a pull request to the repository.
* Reference the #issue number in your pull request.
* Keep pull requests limited to a single issue.
* Test any front-end changes (HTML, CSS, javascript) in multiple browsers.
