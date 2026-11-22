Cron Expression Parser
1. Assessment Overview
This assessment involved building a Python command-line application that parses standard cron expressions.
The application takes a cron expression, expands each of its time fields into individual values, and displays the results in a clear, structured table.
Cron expressions are commonly used in Linux and Unix systems to schedule tasks. The goal of this assessment was to make each part of an expression easier to understand by showing its expanded values.
Important: The application only parses and displays cron expressions. It does not schedule or run commands.
2. Understanding the Problem
A standard cron expression contains five time fields followed by a command:
minute hour day_of_month month day_of_week command

Each field represents a different part of the schedule.
FieldAllowed ValuesDescriptionMinute0–59Minute of the hourHour0–23Hour of the dayDay of Month1–31Day of the monthMonth1–12Month of the yearDay of Week0–7Day of the week
The application expands the five time fields and displays their values in a table. The command is kept unchanged.
3. Approach and Implementation
I broke the problem into smaller parts so that each function has a clear purpose.
Step 1: Accepting the Input
The application accepts a complete cron expression as a command-line argument. This makes it easy to test different expressions without changing the source code.
For example:
python cron_parser.py "*/15 0 1,15 * 1-5 /usr/bin/find"

Step 2: Separating the Fields
The input is split into five time fields and a command. I used Python’s split(maxsplit=5) so that spaces within the command don’t cause it to be split incorrectly.
Step 3: Expanding the Cron Fields
The get_field_values() function expands each time field. It supports the following formats:
ExpressionMeaningExpanded Values*Every allowed valueAll values in the field*/15Every 15 values0 15 30 451,15Specific values1 151-5Range1 2 3 4 51-10/2Range with step1 3 5 7 95Single value55/10Start at 5, then every 105 15 25 35 45 55 (for the minute field)
The function uses each field’s minimum and maximum values to keep the expanded results within the permitted range.
Step 4: Validating the Input
The application validates the input to avoid producing misleading results. It checks that:

All five time fields and a command are provided.
Numeric values fall within the permitted range.
Ranges are formatted correctly.
Step values are positive.
Each field uses a supported format.

When an expression is invalid, the custom CronExpressionError exception provides a clear error message.
Step 5: Formatting the Output
Once the fields have been expanded, the application displays them in a structured table.
The display_result() function aligns the field names in a 14-character column and places the expanded values beside them. The command appears in the final row, unchanged.
4. Example
Input:
*/15 0 1,15 * 1-5 /usr/bin/find

Output:
minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find

Interpreting the expression:

Minute: At 0, 15, 30, and 45 minutes past the hour.
Hour: During hour 0, which is midnight.
Day of Month: On the 1st and 15th of the month.
Month: Every month.
Day of Week: On days 1 through 5.
Command: /usr/bin/find is the command associated with the schedule.

The output shows the expanded values for each field; it does not calculate the actual dates or times when the command would run.
5. Code Organization
I separated the implementation into functions and components so each part is easier to understand, test, and maintain.
Function / ComponentResponsibilityCRON_FIELDSStores each field’s name and allowed range.CronExpressionErrorReports invalid cron expressions.get_field_values()Expands an individual cron field.parse_cron()Separates the input and processes the five time fields.display_result()Formats the expanded values as a table.main()Handles command-line input and displays the result.
6. Testing
I used Python’s built-in unittest framework to test the application. The tests cover:

Wildcard expressions.
Step expressions.
Comma-separated values.
Numeric ranges.
Ranges with steps.
Single values with steps.
Combined expressions with sorted, unique values.
Invalid field values.
Parsing a complete sample expression.
Commands containing spaces.
Incorrect numbers of fields.
Output formatting.

The test suite contains 12 test methods, and all 12 passed during testing.
Run the tests with:
python -m unittest discover -s tests -p "test_*.py" -v

7. Assumptions
The implementation follows these assumptions:

The input uses the standard five-field cron format, followed by a command.
The fields appear in this order: minute, hour, day of month, month, and day of week.
Each field is validated against its permitted numeric range.
The command is treated as all text after the five time fields.
Comma-separated values and ranges are expanded into sorted, unique values.
Step values must be positive integers.
Both 0 and 7 are accepted for the day-of-week field, as specified in the assessment.

8. Limitations
The parser focuses on the formats required for this assessment. It does not currently:

Support special cron strings such as @yearly, @monthly, or @daily.
Execute commands.
Calculate the next scheduled execution time.
Handle time zones.
Interpret platform-specific cron extensions.
Check whether the specified command exists on the system.
Apply the day-of-month and day-of-week interaction rules used by some cron schedulers.

These features could be added later if the parser needs to support more cron formats.
9. Technologies Used

Programming language: Python
Testing framework: Python unittest
Interface: Command-line interface (CLI)
Version control: Git and GitHub

The application does not require any external Python packages.
10. Submission Structure
The project is organized as follows:
Cron-Expression-Parser/
│
├── cron_parser.py
├── README.md
├── .gitignore
│
└── tests/
    └── test_cron_parser.py

11. Setup and Execution
Prerequisites
Install Python 3.9 or later.
Clone the repository
git clone https://github.com/Moulika-04/Cron-Expression-Parser.git

Navigate to the project directory
cd Cron-Expression-Parser

Run the application
python cron_parser.py "*/15 0 1,15 * 1-5 /usr/bin/find"

If your system uses python3 instead of python, run:
python3 cron_parser.py "*/15 0 1,15 * 1-5 /usr/bin/find"

Run the tests
python -m unittest discover -s tests -p "test_*.py" -v

12. Conclusion
I approached this assessment by separating input handling, field expansion, validation, and output formatting into individual functions.
This structure made the application easier to test and maintain, while keeping the implementation clear and focused on the assessment requirements. It also provides straightforward error handling and an output format that makes each cron field easier to understand.
