gcloud functions deploy quizbot \
    --gen2 \
    --region=us-central1 \
    --entry-point=main \
    --runtime=python310 \
    --trigger-http \
    --allow-unauthenticated \
    --set-env-vars=TOKEN=$TOKEN,test=$test