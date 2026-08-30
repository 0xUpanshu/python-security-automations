from pathlib import Path

import yara


class YaraScanner:

    def __init__(self, rules_directory: str):
        self.rules_directory = Path(rules_directory)
        self.rules = None
        self.available = False
        self.error = None

        self._load_rules()

    def _load_rules(self):

        try:
            rule_files = list(self.rules_directory.glob("*.yar"))

            if not rule_files:
                raise FileNotFoundError(
                    f"No YARA rules found in: {self.rules_directory}"
                )

            rule_sources = {}

            for index, rule_file in enumerate(rule_files):
                namespace = f"rule_{index}"
                rule_sources[namespace] = str(rule_file)

            self.rules = yara.compile(filepaths=rule_sources)
            self.available = True

        except (yara.Error, OSError, FileNotFoundError) as error:
            self.available = False
            self.error = str(error)

    def scan_file(self, file_path: str) -> list:

        if not self.available:
            return []

        try:
            matches = self.rules.match(file_path)

            return [match.rule for match in matches]

        except (yara.Error, OSError):
            return []