#!/bin/sh

# Variables d'authentification MinIO (doivent matcher docker-compose)
MINIO_HOST="http://minio:9000"
MINIO_ACCESS_KEY="minioadmin"
MINIO_SECRET_KEY="minioadmin"

# Configuration alias MinIO client
mc alias set localminio $MINIO_HOST $MINIO_ACCESS_KEY $MINIO_SECRET_KEY

# Création des buckets (si n'existent pas)
mc mb --ignore-existing localminio/raw
mc mb --ignore-existing localminio/processed

echo "[✔] Buckets créés (raw, processed)"
