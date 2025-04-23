import os
import requests
from django.core.management.base import BaseCommand, CommandError


# Constant for the AddressBase Plus data package ID
ADDRESSBASEPLUS_FULL_DATA_PACKAGE_ID = "0040146917"


class Command(BaseCommand):
    help = """
    Downloads the latest version of AddressBase Plus from the OS Data Hub.
    Usage: $ OS_DATA_HUB_API_KEY=12345 python manage.py download_latest_addressbaseplus
    """

    def handle(self, *args, **options):
        self.set_api_key()
        self.check_data_package_exists()
        download_info = self.get_latest_version_download_info()
        self.download_file(download_info)

    def set_api_key(self):
        self.api_key = os.environ.get("OS_DATA_HUB_API_KEY")
        if not self.api_key:
            raise CommandError("OS_DATA_HUB_API_KEY environment variable not set")

    def check_data_package_exists(self):
        self.stdout.write("Checking data package exists...")

        response = requests.get(
            f"https://api.os.uk/downloads/v1/dataPackages/{ADDRESSBASEPLUS_FULL_DATA_PACKAGE_ID}",
            headers={"key": self.api_key},
        )

        if response.status_code != 200:
            raise CommandError(
                f"Data package does not exist or is not accessible: {response.text}"
            )

        package_info = response.json()
        self.stdout.write(f'Found data package: {package_info.get("name", "Unknown")}')

    def get_latest_version_download_info(self):
        self.stdout.write("Fetching latest version information...")

        response = requests.get(
            f"https://api.os.uk/downloads/v1/dataPackages/{ADDRESSBASEPLUS_FULL_DATA_PACKAGE_ID}/versions/latest",
            headers={"key": self.api_key},
        )

        if response.status_code != 200:
            raise CommandError(
                f"API request failed with status code {response.status_code}: {response.text}"
            )

        version_info = response.json()

        self.stdout.write(
            f'Found version {version_info.get("productVersion", "Unknown")} created on {version_info.get("createdOn", "Unknown")}'
        )

        if "downloads" not in version_info or not version_info["downloads"]:
            raise CommandError("No downloads available in the version info")

        return version_info["downloads"][0]

    def download_file(self, download_info):
        file_name = download_info["fileName"]
        download_url = download_info["url"]
        file_size = download_info["size"]

        self.stdout.write(f"Downloading {file_name} ({self.format_size(file_size)})...")

        try:
            response = requests.get(
                download_url, headers={"key": self.api_key}, stream=True
            )
            response.raise_for_status()

            with open(file_name, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            actual_size = os.path.getsize(file_name)
            if actual_size != file_size:
                self.stderr.write(
                    self.style.WARNING(
                        f"Downloaded file size ({actual_size} bytes) does not match expected size ({file_size} bytes)"
                    )
                )

            self.stdout.write(f"Download complete: {self.format_size(actual_size)}")
            self.stdout.write(
                self.style.SUCCESS("Successfully downloaded AddressBase Plus")
            )

        except Exception as e:
            if os.path.exists(file_name):
                os.remove(file_name)
                self.stdout.write("Removed partial download")
            raise e

    def format_size(self, size_bytes):
        """Format bytes into a human-readable string"""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size_bytes < 1024.0 or unit == "TB":
                break
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} {unit}"
