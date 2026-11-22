
#!/usr/bin/env bash

set -Eeuo pipefail
umask 077

SOURCE="/var/www/html/"
DESTINATION="ubuntu@195.148.21.188"
BACKUP_ROOT="/srv/backups/server-a"
SSH_KEY="/home/ubuntu/.ssh/id_ed25519_backup_auto"
LOG_FILE="/home/ubuntu/backup-scripts/backup.log"

TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
BACKUP_DIR="$BACKUP_ROOT/$TIMESTAMP"
TEMP_DIR="$BACKUP_ROOT/.incomplete-$TIMESTAMP"

log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

SSH_CMD="ssh -i $SSH_KEY -o BatchMode=yes -o IdentitiesOnly=yes"

log_message "Backup started: $TIMESTAMP"

if $SSH_CMD "$DESTINATION" \
    "mkdir -m 700 '$TEMP_DIR'" &&
   rsync -a --delete \
    -e "$SSH_CMD" \
    "$SOURCE" "$DESTINATION:$TEMP_DIR/" &&
   $SSH_CMD "$DESTINATION" \
    "mv '$TEMP_DIR' '$BACKUP_DIR'"
then
    log_message "SUCCESS: $BACKUP_DIR"
    echo "Backup completed successfully."
else
    log_message "FAILED: $TIMESTAMP"
    echo "Backup failed. Check the log." >&2
    exit 1
fi
