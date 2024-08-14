# How to create and run the container

## Create the container
```bash
docker build -t bica-backup-python .
```

## Run the container
```bash
docker run -d --name bica-backup-python \
     -e DB_HOST=localhost \
     -e DB_PORT=5432 \
     -e DB_USER=bica_user \
     -e DB_PASSWORD=bica_password \
     -e DB_NAME=bica_db \
     -e BACKUP_DIR=/mnt/backups \
     -e RETENTION_DAYS=7 \
     -v /mnt/backups:/mnt/backups \
     bica-backup-python
```   