docker build -t gcr.io/innate-shell-334410/ecommerce-andri .

docker push gcr.io/innate-shell-334410/ecommerce-andri

gcloud run deploy ecommerce-demo \
  --image gcr.io/innate-shell-334410/ecommerce-andri \
  --platform managed \
  --region asia-southeast2 \
  --allow-unauthenticated \
  --project innate-shell-334410
