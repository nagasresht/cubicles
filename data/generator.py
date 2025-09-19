import csv, random
from datetime import datetime

def generate_mock_csv(path="mock_logins.csv", rows=50):
    fields = ["timestamp", "user", "location", "logins_last_minute", "data_transfer_mb"]
    users = ["alice", "bob", "charlie"]
    locations = ["Delhi", "Mumbai", "Russia", "USA"]

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for _ in range(rows):
            writer.writerow({
                "timestamp": datetime.utcnow().isoformat(),
                "user": random.choice(users),
                "location": random.choice(locations),
                "logins_last_minute": random.randint(1, 200),
                "data_transfer_mb": random.randint(1, 1000)
            })

if __name__ == "__main__":
    generate_mock_csv()
