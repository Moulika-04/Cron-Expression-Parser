"""Expand standard five-field cron expressions into readable values."""

import sys

CRON_FIELDS = [
    ("minute", 0, 59),
    ("hour", 0, 23),
    ("day of month", 1, 31),
    ("month", 1, 12),
    ("day of week", 0, 7),
]

class CronExpressionError(ValueError):
    """Raised when a cron expression or one of its fields is invalid."""

def get_field_values(field: str, min_value: int, max_value: int) -> list[int]:
    """Expand one cron field supporting *, */step, ranges, lists and steps."""
    if not field:
        raise CronExpressionError("Cron fields cannot be empty.")

    values = set()

    for item in field.split(","):
        if not item:
            raise CronExpressionError(f"Invalid empty item in field: {field!r}")

        pieces = item.split("/")
        if len(pieces) > 2:
            raise CronExpressionError(f"Invalid step expression: {item!r}")

        base = pieces[0]
        step = 1
        if len(pieces) == 2:
            try:
                step = int(pieces[1])
            except ValueError:
                raise CronExpressionError(f"Step must be an integer: {item!r}")
            if step <= 0:
                raise CronExpressionError(f"Step must be greater than zero: {item!r}")

        if base == "*":
            start, end = min_value, max_value
        elif "-" in base:
            bounds = base.split("-")
            if len(bounds) != 2:
                raise CronExpressionError(f"Invalid range: {base!r}")
            try:
                start, end = map(int, bounds)
            except ValueError:
                raise CronExpressionError(f"Range values must be integers: {base!r}")
            if start > end:
                raise CronExpressionError(f"Range start cannot exceed its end: {base!r}")
        else:
            try:
                start = int(base)
            except ValueError:
                raise CronExpressionError(f"Invalid cron value: {base!r}")
            # A stepped single value runs from that value through the field maximum.
            end = max_value if len(pieces) == 2 else start

        if start < min_value or end > max_value:
            raise CronExpressionError(
                f"Values in {item!r} must be between {min_value} and {max_value}."
            )

        values.update(range(start, end + 1, step))

    return sorted(values)

def parse_cron(expression: str) -> list[tuple[str, str]]:
    """Parse a cron expression and return labelled, expanded output rows."""
    parts = expression.strip().split(maxsplit=5)
    if len(parts) != 6:
        raise CronExpressionError(
            "Expected five time fields followed by a command."
        )

    rows = []
    for (name, min_value, max_value), field in zip(CRON_FIELDS, parts[:5]):
        field_values = get_field_values(field, min_value, max_value)
        rows.append((name, " ".join(map(str, field_values))))

    command = parts[5].strip()
    if not command:
        raise CronExpressionError("The command cannot be empty.")
    rows.append(("command", command))
    return rows

def display_result(rows: list[tuple[str, str]]) -> str:
    """Format rows using a 14-character field-name column."""
    return "\n".join(f"{name:<14}{value}" for name, value in rows)

def main() -> int:
    if len(sys.argv) != 2:
        print('Usage: python cron_parser.py "<minute> <hour> <day> <month> <weekday> <command>"',
              file=sys.stderr)
        return 2

    try:
        rows = parse_cron(sys.argv[1])
        print(display_result(rows))
        return 0
    except CronExpressionError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
