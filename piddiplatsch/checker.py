class HandleChecker:
    checkers = {}

    def __init__(self, names=None):
        if names is None:
            names = self.checkers.keys()
        self.checkers = {k: self.checkers[k] for k in names}

    def __repr__(self):
        return f"<Checker checkers={sorted(self.checkers)}>"

    def checks(self, name):
        """
        This is a decorator to register a check function with a name.
        """

        def _checks(func):
            self.checkers[name] = func
            return func

        return _checks

    def check(self, record, name):
        if name not in self.checkers:
            return

        func = self.checkers[name]
        result, cause = None, None
        try:
            result = func(record)
        except Exception as e:
            cause = e
        if not result:
            raise ValueError(
                f"check {name!r} failed for record {record!r}: cause={cause}"
            )

    def run_checks(self, record):
        for name in self.checkers:
            self.check(record, name)


checker = HandleChecker()


@checker.checks(name="nothing")
def check_nothing(record):
    return True
