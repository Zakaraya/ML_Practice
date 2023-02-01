from typing import List
import re


def valid_emails(strings: List[str]) -> List[str]:
    """Take list of potential emails and returns only valid ones"""

    valid_email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    def is_valid_email(email: str) -> bool:
        return bool(valid_email_regex.fullmatch(email))

    emails = [email for email in strings if is_valid_email(email)]

    return emails
