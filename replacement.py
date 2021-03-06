import random

from mutator import Mutator, SimplePattern, get_mutators


class Replacement:
    def __init__(
        self, start_col: int, end_col: int, old_val: str, new_val: str
    ) -> None:
        self.start_col = start_col
        self.end_col = end_col
        self.old_val = old_val
        self.new_val = new_val

    def apply(self, line: str) -> str:
        # if the whole line is to be replaced, return the new value
        if self.end_col - self.start_col == len(line) - 1:
            return self.new_val

        return "{prefix}{replacement}{suffix}".format(
            prefix=line[: self.start_col],
            replacement=self.new_val,
            suffix=line[self.end_col :],
        )

    def __repr__(self) -> str:
        return '[({begin_col}:{end_col}) "{old_val}" -> "{new_val}"]'.format(
            begin_col=self.start_col,
            end_col=self.end_col,
            old_val=self.old_val,
            new_val=self.new_val,
        )


def reverse(r: Replacement) -> Replacement:
    return Replacement(r.start_col, r.end_col, r.new_val, r.old_val)


class Mutation:
    def __init__(
        self,
        mutator_id: str,
        mutator_description: str,
        line_number: int,
        replacement: Replacement,
    ):
        self.id = mutator_id  # name of mutation ran on line
        self.description = mutator_description  # describes mutation
        self.line = line_number  # line number of mutated line
        self.replacement = replacement  # info on old and new values


def random_mutaor(omit: List[str], max_lines: int) -> Mutation:
    mutators = get_mutators()
    mutator = random.choice(list(mutators.values()))
    if len(mutators) <= len(omit):
        return Mutation(
            mutator.mutator_id,
            mutator.description,
            random.randrange(0, max_lines),
            random_replacement(mutator),
        )


def random_replacement(mutator: Mutator) -> Replacement:
    if mutator.mutator_id in [
        "lineDeletion",
        "decimalNumberLiteral",
        "hexNumberLiteral",
    ]:
        pass
    else:
        start_col = random.randrange(0, 100)
        old_val, new_vals = random.choice(
            list(mutator.pattern.replacement_patterns.items())
        )
        new_val = random.choice(new_vals)

        return Replacement(start_col, start_col + len(old_val), old_val, new_val)
