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
        + terraform init
        + terraform plan
        + terraform apply

        2-1 You should Complete Validation of SSL certificat:
        - Buy a Domain name (Freenom Free!)
        + [How to link between Certificat SSL and Domain name DNS]
        - (https://www.youtube.com/watch?v=h6OSHlEje84)

      3- Provisioning an Amazon CloudFront Distribution
      The next module is created for the provisioning of an Amazon CloudFront distribution.
      Create a directory called modules/cloudfront with three files: main.tf, variables.tf,
      and outputs.tf. The main.tf file in the cloudfront directory tells Terraform
      to create a CloudFront distribution resource. It uses several variables that are declared in variables.tf
      and whose values are passed to it by the caller of this module.
      It outputs the DNS domain name for the CloudFront endpoint and the hosted Route 53 zone ID for the CloudFront distribution,
      which will be used by other modules as input variables.

      + Add a reference to the cloudfront module in the main Terraform file.
        Pass s3_www_website_endpoint and acm_certificate_arn as input variables to the cloudfront module.
        Their values are retrieved from the outputs of the other modules, s3 and acm, respectively.

      + The terraform apply step took almost 23 minutes in this case.
        Provisioning an Amazon CloudFront distribution is one of the lengthiest operations in AWS,
        because the distribution is being deployed globally by Amazon behind the scenes.
        + terraform init
        + terraform plan
        + terraform apply


      4- Provisioning a Route 53 DNS Record
      The next module was for the creation of a Route 53 DNS record for the main domain
      of the site www.devops4all.dev. Create a directory called modules/route53 with two files:
      main.tf and variables.tf. The main.tf file in the route53 directory tells Terraform
      to create a Route 53 DNS record of type A as an alias to the DNS name of the CloudFront endpoint.
      It uses several variables that are declared in variables.tf and whose values are passed
      to it by the caller of this module.
      + terraform init
      + terraform plan
      + terraform apply

      5- Copying Static Files to S3
      To test the provisioning of the static website from end to end, create a simple file called index.html
      that includes a JPEG image, and copy both files to the S3 bucket previously provisioned with Terraform.
      Make sure that the AWS_PROFILE environment variable is set to a correct value already present
      in the ~/.aws/credentials file.

      + cd ~/.aws
      + aws configure list
      + aws configure --profile IAM_SES
      + aws s3 cp static_files/index.html s3://www.pydevops.ml/index.html
      + aws s3 cp static_files/all.jpg s3://www.pydevops.ml/all.jpg

      NB: Deleting All AWS Resources Provisioned with Terraform
          Whenever you provision cloud resources, you need to be mindful of the cost associated with them.
          It is very easy to forget about them, and you may be surprised by the AWS bill you receive at the end of the month.
          Make sure to delete all the resources provisioned above. Remove these resources by running the `terraform destroy`
          command. One more thing to note is that the contents of the S3 bucket need to be removed before running terraform
          destroy because Terraform will not delete a nonempty bucket.
