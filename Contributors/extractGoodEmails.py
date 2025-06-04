import re
import csv

# Input and output filenames
input_file = "/home/iit/Downloads/Thesis/Code/unique_contributors.csv"
output_file = "filtered_contributors.csv"

# Define email filter regex (simplified "good" pattern)
EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)

# Keywords to exclude (no-reply, bots, or suspicious)
EXCLUDE_PATTERNS = [
    "users.noreply.github.com",
    "noreply", "no-reply", "do-not-reply", "donotreply",
    "example.com", "localhost",
    "@21.co", "git@", "bot@", "mailer@", "info@", "support@", "contact@"
]

def is_valid_email(email):
    if not EMAIL_PATTERN.match(email):
        return False
    for pattern in EXCLUDE_PATTERNS:
        if pattern.lower() in email.lower():
            return False
    # Heuristic: avoid email starting with mostly digits
    if re.match(r"^\d{3,}", email.split("@")[0]):
        return False
    return True

with open(input_file, newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        if len(row) != 2:
            continue
        name, email = row
        email = email.strip()
        if is_valid_email(email):
            writer.writerow([name.strip(), email])

print(f"✅ Filtered list saved to: {output_file}")
