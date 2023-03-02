"""

{
            "github_issue": f"https://github.com/{self.repo}/issues/1",
            "gss": "X01000000",
            "council_name": "Piddleton Parish Council",
            "election_date": "2019-12-12",
            "timestamp": "2019-09-30T17:00:02.396833",
            "file_set": [
                {
                    "key": "X01000000/2019-12-12/2019-09-30T17:00:02.396833/data.csv",
                    "csv_valid": True,
                    "csv_rows": 10,
                    "csv_encoding": "utf-8",
                    "ems": "Idox Eros (Halarose)",
                    "errors": "",
                }
            ],
        }
"""
from pydantic import BaseModel, HttpUrl, Field


class Report(BaseModel):
    github_issue: HttpUrl = Field(description="A URL to the GitHub issue")
