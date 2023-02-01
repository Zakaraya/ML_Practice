### Вашей команде поручили заняться разработкой сервиса для автоматического отлова ботов и предотвращения DDoS-атак. Для регистрации на сайте необходимо указать email-адрес. Не всегда указанный набор символов является корректным email.

### Вашему коллеге-стажёру поручили выполнить это маленькое задание, в результате разработан код, приведённый ниже:

```python
import re
from typing import List


def valid_emails(strings: List[str]) -> List[str]:
    """Take list of potential emails and returns only valid ones"""

    valid_email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    def is_valid_email(email: str) -> bool:
        return bool(re.fullmatch(valid_email_regex, email))

    emails = []
    for email in strings:
        if is_valid_email(email):
            emails.append(email)

    return emails
```
### Код работает корректно и полностью решает задачу, однако когда ваш TeamLead ревьюил код, то оставил комментарий, что его можно ускорить минимум в 2 раза, буквально поменяв две строчки. Однако он не сказал, как – лишь оставил ссылку [на страницу про регулярные выражения](https://docs.python.org/3/library/re.html) в Python в качестве подсказки.  