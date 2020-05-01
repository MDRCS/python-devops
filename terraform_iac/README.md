# + Terraform Infrastructure

    - The policy attribute of the aws_s3_bucket resource above is an example of an S3 bucket policy
    that allows public access to the bucket. If you work with S3 buckets in an IaC context,
    it pays to familiarize yourself with the official AWS documentation on bucket and user policies.

### + Getting Started with terraform:
    - Terraform Tutorial :

      1- The first step in running Terraform is to invoke the `terraform init` command,
      which will read the contents of any module referenced by the main file.
      The next step is to run the `terraform plan` command, which creates the blueprint mentioned
      in the earlier discussion.
      To create the resources specified in the plan, run `terraform apply`.
        + terraform init
        + terraform plan
        + terraform apply

      2- Provisioning an SSL Certificate with AWS ACM
      The next module is created for the provisioning of an SSL certificate using the AWS Certificate Manager service.
      Create a directory called modules/acm with three files: main.tf, variables.tf,
      and outputs.tf. The main.tf file in the acm directory tells Terraform
      to create an ACM SSL certificate using DNS as the validation method.
      It uses a variable called domain_name which is declared in variables.tf
      and whose value is passed to it by the caller of this module. It outputs the ARN identifier of the certificate,
      which will be used by other modules as an input variable.

      3- Provisioning an Amazon CloudFront Distribution
      The next module is created for the provisioning of an Amazon CloudFront distribution.
      Create a directory called modules/cloudfront with three files: main.tf, variables.tf,
      and outputs.tf. The main.tf file in the cloudfront directory tells Terraform
      to create a CloudFront distribution resource. It uses several variables that are declared in variables.tf
      and whose values are passed to it by the caller of this module.
      It outputs the DNS domain name for the CloudFront endpoint and the hosted Route 53 zone ID for the CloudFront distribution,
      which will be used by other modules as input variables.
