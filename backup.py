import os, subprocess, datetime, shutil, gzip

# Environment variables configuration
DB_USER = os.getenv('DB_USER', 'bica_user')
DB_NAME = os.getenv('DB_NAME', 'bica_db')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'bica_password')

BACKUP_DIR = os.getenv('BACKUP_DIR', '/mnt/backups')
RETENTION_DAYS = int(os.getenv('RETENTION_DAYS', '7'))

if __name__ == '__main__':

    # Generate archive file name
    filename = f"bica-backup-{datetime.datetime.now().strftime('%Y-%m-%d_%H%M')}.tar.gz"
    # Generate archive file path
    path = os.path.join(BACKUP_DIR, filename)
    print("backup ", path)

    # Configure dump command
    dump = ['pg_dump', '-h', DB_HOST, '-p', DB_PORT, '-U', DB_USER, '-d', DB_NAME]

    print(f"Backup started: {filename}")
    print(f"Backup path: {path}")
    print(dump)

    # Export password to environment variable
    os.environ['PGPASSWORD'] = DB_PASSWORD

    try:
        # Create backup file
        backup_file = open(f"{path}.tmp", 'wb')
        subprocess.check_call(dump, stdout=backup_file)

        print(f"Backup file created: {filename}")

        f_in = open(f"{path}.tmp", 'rb')
        # Zip backup archive
        f_out = gzip.open(path, 'wb')
        shutil.copyfileobj(f_in, f_out)

        # Close open files
        f_in.close()
        f_out.close()
        backup_file.close()

        print(f"Backup file compressed: {filename}")

        # Remove temporary file
        os.remove(f"{path}.tmp")
        print(f"Backup finished successfully: {filename}")


    except subprocess.CalledProcessError as e:
        print(f"Error creating backup: {e}")

    now = datetime.datetime.now()

    # Remove old backups
    for filename in os.listdir(BACKUP_DIR):
        if filename.startswith("bica-backup-") and filename.endswith(".tar.gz"):
            file_path = os.path.join(BACKUP_DIR, filename)
            file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if (now - file_mtime).days > RETENTION_DAYS:
                os.remove(file_path)
                print(f"Old backup removed: {filename}")
