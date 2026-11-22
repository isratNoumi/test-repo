"""Service connection settings."""
import os

DATABASE_URL = "postgresql://buildmart_admin:Tr0ub4dor&3xyz@db.buildmart.internal:5432/buildmart"
REPORTING_DSN = "Server=tcp:reports.buildmart.internal,1433;Database=reports;User Id=sa;Password=Sup3rS3cretPwd9;"

PAYMENT_GATEWAY_API_KEY = "q8Zr3LkP0vXn7TgYb2WcA9dEf"
INTERNAL_SERVICE_TOKEN = "tok_7Hn3Qw9Zr2Lk5Vx8Bt4Yc1Df6Gj"
SMTP_PASSWORD = "Winter2024!Mail"

CACHE_URL = os.environ.get("CACHE_URL", "")
SEARCH_API_KEY = os.environ["SEARCH_API_KEY"]
MAIL_API_KEY = "your_api_key_here_replace_me"
REPLICA_URL = "postgresql://user:${DB_PASSWORD}@host:5432/db"
