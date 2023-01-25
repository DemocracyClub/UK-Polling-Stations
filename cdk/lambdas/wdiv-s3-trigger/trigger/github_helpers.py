import requests
from requests.exceptions import HTTPError
from requests_paginator import RequestsPaginator


def get_next_page(page):
    if "Link" in page.headers:
        linkHeaders = page.headers["Link"].split(", ")
        for linkHeader in linkHeaders:
            (url, rel) = linkHeader.split("; ")
            url = url[1:-1]
            rel = rel[5:-1]
            if rel == "next":
                return url
    return None


class GitHubIssue:
    def __init__(self, api_key, repo, title, body):
        self.api_key = api_key
        self.repo = repo
        self.title = title
        self.body = body
        self.labels = ["Data Import", "ready"]

    def get_existing_issue(self):
        pages = RequestsPaginator(
            f"https://api.github.com/repos/{self.repo}/issues?state=open&labels=Data%20Import",
            get_next_page,
        )
        for page in pages:
            page.raise_for_status()
            issues = page.json()
            for issue in issues:
                if issue["title"] == self.title:
                    return issue["number"]
        return None

    def update_existing_issue(self, number):
        url = f"https://api.github.com/repos/{self.repo}/issues/{number}/comments"
        payload = {"body": f"Updated\n{self.body}"}
        return self.post(url, payload)

    def create_new_issue(self):
        url = f"https://api.github.com/repos/{self.repo}/issues"
        payload = {"title": self.title, "body": self.body, "labels": self.labels}
        return self.post(url, payload)

    def post(self, url, payload):
        r = requests.post(
            url, json=payload, headers={"Authorization": f"token {self.api_key}"}
        )
        try:
            r.raise_for_status()
        except HTTPError:
            # TODO: what should we do here if we can't raise an issue?
            raise
        issue = r.json()
        return issue["html_url"]

    def debug(self):
        print("GITHUB_API_KEY not set")
        print(f"repo: {self.repo}")
        print(f"title: {self.title}")
        print(f"body: {self.body}")
        print("---")
        return ""

    def raise_issue(self):
        if self.api_key:
            try:
                existing_issue = self.get_existing_issue()
            except HTTPError:
                # better to raise a duplicate issue than crash here
                existing_issue = None

            if existing_issue:
                return self.update_existing_issue(existing_issue)
            else:
                return self.create_new_issue()

        return self.debug()


def raise_github_issue(api_key, repo, report):
    title = (
        f"Import {report['gss']}-{report['council_name']} for {report['election_date']}"
    )
    try:
        body = f"EMS: {report['file_set'][0]['ems']}\nFiles:"
        for f in report["file_set"]:
            body = body + f"\n- `{f['key']}`"
    except KeyError:
        body = ""
    issue = GitHubIssue(api_key, repo, title, body)
    return issue.raise_issue()
