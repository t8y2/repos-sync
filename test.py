import re

import inquirer
questions = [
  inquirer.Text('name', message="What's your name"),
  inquirer.Text('surname', message="What's your surname"),
  inquirer.Text('phone', message="What's your phone number",
                validate=lambda _, x: re.match('\+?\d[\d ]+\d', x),
                )
]
answers = inquirer.prompt(questions)
