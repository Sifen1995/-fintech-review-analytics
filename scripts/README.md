# Scripts
## Relational Database Storage Engine (Task 3)

The pipeline uses a relational database architecture hosted inside a Dockerized **PostgreSQL** instance to store our processed sentiment assets securely.

### Port Binding Mapping
Due to local environment port availability on the development machine, port bindings are mapped as follows:
* **Internal Container Port:** 5432
* **External Host Port Proxy:** 15432

### Relational Schema Blueprint
The database structure relies on two highly normalized tables to enforce data integrity:
1. `banks`: Holds metadata tracking short-codes and full application names.
2. `reviews`: Tracks cleaned feedback text strings, sentiment tracking floats, and classified operational themes linked back to the target entity using a `bank_id` Foreign Key.

### To Initialize and Populate Database:
Ensure your Docker container is actively proxying port `15432`, then run:
```bash
python3 scripts/db_uploader.py


---

## Step 3: Git Commit and Push to Turn Your Pipeline Green!
Since all your code files are finalized and testing green, it's time to push your work up to GitHub and merge it.

Run these git commands in order:

```bash
# 1. Add your new database assets to staging
git add scripts/schema.sql scripts/db_uploader.py scripts/verify_db.py README.md

# 2. Commit the changes cleanly
git commit -m "feat: design postgres relational schema, implement sqlalchemy data pipeline and execute validation scripts"

# 3. Push this branch up to your GitHub repository
git push origin task-3

