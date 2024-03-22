from piddiplatsch.pidmaker import PidMaker
from piddiplatsch.exceptions import CheckError


class HandleChecker:
    checkers = {}

    def __init__(self, names=None):
        if names is None:
            names = self.checkers.keys()
        self.checkers = {k: self.checkers[k] for k in names}

    def __repr__(self):
        return f"<Checker checkers={sorted(self.checkers)}>"

    @classmethod
    def _cls_checks(cls, name):
        def _checks(func):
            cls.checkers[name] = func
            return func

        return _checks

    def checks(self, name):
        """
        This is a decorator to register a check function with a name.
        """

        def _checks(func):
            self.checkers[name] = func
            return func

        return _checks

    def check(self, name, pid_maker, record, options):
        if name not in self.checkers:
            return

        func = self.checkers[name]
        result, cause = None, None
        try:
            result = func(pid_maker, record, options)
        except Exception as e:
            cause = e
        if not result:
            raise CheckError(
                f"check {name!r} failed for record {record!r}: cause={cause}"
            )

    def run_checks(self, pid_maker, record, options):
        for name in self.checkers:
            self.check(name, pid_maker, record, options)


@HandleChecker._cls_checks(name="ok")
def check_ok(pid_maker, record, options):
    return True


@HandleChecker._cls_checks(name="not_ok")
def check_not_ok(pid_maker, record, options):
    return False
