# ISProject
What it does:
Most Texas electricity providers offer different pricing structures such as flat rate, time-of-use, free weekends, free highest-usage-days, and it's not obvious which one is actually cheapest without doing the math. This program does that math for you.
Upload interval usage data exported from Smart Meter Texas, enter the plan's rate(s), and it calculates your total cost. The comparison route runs all four plan types against the same data and tells you which one is the cheapest.

How it's built:

app.py — Flask routes and forms (Flask-WTF) for uploading data and entering rates

energyData.py — Parses the usage CSV and runs the cost calculations for each plan type

application.py — Deployment entry point (AWS Elastic Beanstalk)
