import datetime

# Example cookie sales forecast
sales = {
    "Thursday": 120,
    "Friday": 95,
    "Saturday": 150
}

# Generate HTML
html_content = f"""
<html>
<head><title>Cookie Forecast</title></head>
<body>
    <h1>Cookie Forecast</h1>
    <p>Last updated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
    <ul>
        {''.join(f'<li>{day}: {amount} cookies</li>' for day, amount in sales.items())}
    </ul>
</body>
</html>
"""

with open("cookieweb.html", "w") as f:
    f.write(html_content)

print("Website updated! Now commit and push to GitHub.")
