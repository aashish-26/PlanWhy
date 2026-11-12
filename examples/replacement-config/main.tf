# This synthetic resource is scanned as text only by the accompanying example.
# It is not a complete deployable Terraform configuration and must not be applied.
resource "aws_instance" "web" {
  user_data = timestamp()
}
