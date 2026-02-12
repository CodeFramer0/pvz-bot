#!/bin/sh
set -e

# ===== CONFIG =====
MC_ALIAS_NAME="${MC_ALIAS_NAME:-myminio}"
MC_URL="${MC_URL:-${MINIO_INTERNAL_ENDPOINT:-http://minio:9000}}"
MC_USER="${MINIO_ROOT_USER:-minioadmin}"
MC_PASSWORD="${MINIO_ROOT_PASSWORD:-minioadmin}"
MAX_RETRIES=30
RETRY_DELAY=2

echo "=========================================="
echo "MinIO Initialization Script"
echo "=========================================="
echo "URL: $MC_URL"
echo "User: $MC_USER"
echo "=========================================="

# ===== WAIT FOR MINIO =====
echo "Waiting for MinIO API..."
retry_count=0
until mc alias set "$MC_ALIAS_NAME" "$MC_URL" "$MC_USER" "$MC_PASSWORD" 2>/dev/null; do
  retry_count=$((retry_count + 1))
  if [ $retry_count -ge $MAX_RETRIES ]; then
    echo "❌ Failed to connect to MinIO after $MAX_RETRIES attempts"
    echo "Check credentials:"
    echo "  MINIO_ROOT_USER: $MC_USER"
    echo "  MINIO_ROOT_PASSWORD: [hidden]"
    exit 1
  fi
  echo "MinIO not ready, retrying... ($retry_count/$MAX_RETRIES)"
  sleep $RETRY_DELAY
done

echo "✅ Connected to MinIO successfully"

# ===== BUCKETS =====
echo ""
echo "Creating buckets..."
for bucket in "$MINIO_BUCKET_STATIC" "$MINIO_BUCKET_MEDIA" "$MINIO_BUCKET_DBBACKUP"; do
  if mc stat "$MC_ALIAS_NAME/$bucket" >/dev/null 2>&1; then
    echo "  ℹ️  Bucket '$bucket' already exists"
  else
    mc mb "$MC_ALIAS_NAME/$bucket"
    echo "  ✅ Bucket '$bucket' created"
  fi
done

# ===== ACCESS POLICIES =====
echo ""
echo "Setting access policies..."
mc anonymous set download "$MC_ALIAS_NAME/$MINIO_BUCKET_STATIC" 2>/dev/null && echo "  ✅ $MINIO_BUCKET_STATIC - public read" || echo "  ⚠️ Failed to set policy"
mc anonymous set none "$MC_ALIAS_NAME/$MINIO_BUCKET_MEDIA" 2>/dev/null && echo "  ✅ $MINIO_BUCKET_MEDIA - private" || echo "  ⚠️ Failed to set policy"
mc anonymous set none "$MC_ALIAS_NAME/$MINIO_BUCKET_DBBACKUP" 2>/dev/null && echo "  ✅ $MINIO_BUCKET_DBBACKUP - private" || echo "  ⚠️ Failed to set policy"

# ===== VERIFICATION =====
echo ""
echo "=========================================="
echo "Verification"
echo "=========================================="
mc ls "$MC_ALIAS_NAME"

echo ""
echo "✅ MinIO initialization completed successfully"
echo "=========================================="
echo "Access URLs:"
echo "  Console: http://console.s3.localhost"
echo "  API: http://s3.localhost"
echo "  Static: http://static.s3.localhost"
echo "  Media: http://media.s3.localhost"
echo "=========================================="
