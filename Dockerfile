# Use image with both Python and PostgreSQL
FROM python:3.9-alpine

# Add needed tools
RUN apk add --no-cache postgresql-client bash gzip

# Copy backup script
COPY backup.py /usr/local/bin/backup.py

# Add Python dependencies
RUN pip install psycopg2-binary

# Copy crontab for scheduling
COPY crontab.txt /etc/crontabs/root

# Add permissions for the script to be executable
RUN chmod +x /usr/local/bin/backup.py

# Define entry point to start cron
CMD ["crond", "-f"]



