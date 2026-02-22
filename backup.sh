#!/bin/sh
set -e

# ===== CONFIG =====
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_${TIMESTAMP}.sql.gz"
MC_ALIAS="myminio"

echo "=========================================="
echo "PostgreSQL Backup"
echo "=========================================="
echo "Timestamp: $TIMESTAMP"

# ===== DUMP =====
echo "Creating dump..."
pg_dump -h db -U "$POSTGRES_USER" "$POSTGRES_DB" | gzip > "/tmp/$BACKUP_FILE"
echo "✅ Dump created: $BACKUP_FILE"

# ===== UPLOAD TO MINIO =====
echo "Uploading to MinIO..."
mc alias set "$MC_ALIAS" "$MC_URL" "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"
mc cp "/tmp/$BACKUP_FILE" "$MC_ALIAS/$MINIO_BUCKET_DBBACKUP/$BACKUP_FILE"
echo "✅ Uploaded to MinIO"

# ===== ROTATION (оставляем последние 30 бэкапов) =====
echo "Rotating old backups..."
mc ls "$MC_ALIAS/$MINIO_BUCKET_DBBACKUP" \
  | awk '{print $NF}' \
  | sort \
  | head -n -30 \
  | while read -r old_file; do
      mc rm "$MC_ALIAS/$MINIO_BUCKET_DBBACKUP/$old_file"
      echo "  🗑 Removed: $old_file"
    done

# ===== CLEANUP =====
rm "/tmp/$BACKUP_FILE"

echo ""
echo "✅ Backup completed: $BACKUP_FILE"
echo "=========================================="