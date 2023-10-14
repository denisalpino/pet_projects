import re

class CaseHelper:
    __SNAKECASE = re.compile(r'[^a-z_]|\b_|_\b')
    __CAMELCASE = re.compile(r'\b[A-Z]')

    @staticmethod
    def is_snake(line: str) -> bool:
        return not bool(re.search(CaseHelper.__SNAKECASE, line))

    @staticmethod
    def is_upper_camel(line: str) -> bool:
        return bool(re.search(CaseHelper.__CAMELCASE, line))

    @staticmethod
    def to_snake(line: str) -> str:
        return re.sub(r'\B([A-Z])', r'_\1', line).lower()

    @staticmethod
    def to_upper_camel(line: str) -> str:
        return ''.join(map(str.title, line.split('_')))