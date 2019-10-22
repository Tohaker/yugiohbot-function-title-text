resource "google_storage_bucket" "bucket" {
  name = "title-text-bucket"
}

resource "google_storage_bucket_object" "function" {
  name    = "function.zip"
  bucket  = google_storage_bucket.bucket.name
  source  = var.source
}
