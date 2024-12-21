docker build -t gcr.io/innate-shell-334410/ecommerce-andri-be .

docker push gcr.io/innate-shell-334410/ecommerce-andri-be

source .env
gcloud run deploy ecommerce-demo-be \
  --set-env-vars DATABASE_URL=$DATABASE_URL \
  --image gcr.io/innate-shell-334410/ecommerce-andri-be \
  --platform managed \
  --region asia-southeast2 \
  --allow-unauthenticated \
  --project innate-shell-334410
