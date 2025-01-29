import re


class DomainException(Exception):
    pass

class Domain:
    """Сlass Domain is intended for working with domains. This class supports
    three ways to create its instance: directly through the class call, as well
    as with the help of two class methods from_url() and from_email()
    """

    def __init__(self, domain: str) -> None:
        dom = re.fullmatch(r'(https?://|[a-z]+@)?([a-z]+\.[a-z]+)', domain)
        if not bool(dom):
            raise DomainException('Недопустимый домен, url или email')
        self.dom = dom.group(2)

    def __str__(self) -> str:
        return self.dom

    @classmethod
    def from_url(cls, url: str):
        return cls(url)

    @classmethod
    def from_email(cls, email: str):
        return cls(email)