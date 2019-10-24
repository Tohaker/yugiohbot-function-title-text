data "archive_file" "function_zip" {
  type = "zip"
  source_dir = "../function/"
  output_path = "../function.zip"
}

resource "google_storage_bucket" "bucket" {
  name = "title-text-bucket"
}

resource "google_storage_bucket_object" "function" {
  name    = "function.zip"
  bucket  = google_storage_bucket.bucket.name
  source  = data.archive_file.function_zip.output_path
}
