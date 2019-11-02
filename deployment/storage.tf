data "archive_file" "function_zip" {
  type = "zip"
  source_dir = "${path.module}/function"
  output_path = "${path.module}/function.zip"
}

resource "google_storage_bucket" "bucket" {
  name = "title-text-bucket"
}

resource "google_storage_bucket_object" "function" {
  name    = "${var.function_name}.${data.archive_file.function_zip.output_md5}.zip"
  bucket  = google_storage_bucket.bucket.name
  source  = data.archive_file.function_zip.output_path
}
