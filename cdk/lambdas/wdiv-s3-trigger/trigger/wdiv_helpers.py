import requests
from requests.exceptions import HTTPError


def gss_to_council(gss, wdiv_api_key):
    r = requests.get(
        f"https://wheredoivote.co.uk/api/beta/councils/{gss}.json/?auth_token={wdiv_api_key}",
    )
    try:
        r.raise_for_status()
        council = r.json()
        return council["name"]
    except (HTTPError, KeyError):
        # if we can't get the name,
        # raising the issue with only a GSS code
        # isn't the end of the world
        return gss


def submit_report(url, wdiv_api_key, report):
    if wdiv_api_key:
        r = requests.post(
            url, json=report, headers={"Authorization": f"Token {wdiv_api_key}"}
        )
        r.raise_for_status()
    else:
        print("WDIV_API_KEY not set")
        print(url)
        print(report)
        print("---")
