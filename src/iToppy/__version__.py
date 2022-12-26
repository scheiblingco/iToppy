"""Module information."""
import os

# The title and description of the package
__title__ = "iToppy"
__description__ = """
    Python package for the iTop CMDB/Service Management Rest API
"""

# The version and build number
# Without specifying a unique number, you cannot overwrite packages in the PyPi repo
__version__ = os.getenv("RELEASE_NAME", "0.0.0" + os.getenv("GITHUB_RUN_ID", ""))

# Author and license information
__author__ = "Lars Scheibling"
__author_email__ = "lars@scheibling.se"
__license__ = "GnuPG 3.0"

# URL to the project
__url__ = f"https://github.com/scheiblingcopip3/{__title__}"
