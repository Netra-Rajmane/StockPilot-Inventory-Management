# StockPilot — Inventory Management System

A beginner-friendly Flask + SQLite inventory application with an enhanced responsive dashboard, automated tests, Docker packaging, Jenkins CI/CD, and Terraform AWS infrastructure configuration.

## Features
- Dashboard cards: product count, stock units, low-stock count, inventory value
- Add products with unique SKU validation
- Update product quantity and unit price
- Delete products
- Search by product name and filter by category
- Stock status indicators: healthy, low, out of stock
- JSON endpoints: `/health` and `/api/products`

## Run locally (Windows)
1. Install Python 3.10+.
2. Open this folder in VS Code.
3. In the VS Code terminal run:
   ```powershell
   py -m venv venv
   .\\venv\\Scripts\\activate
   py -m pip install -r requirements.txt
   py app.py
   ```
4. Open `http://127.0.0.1:5000`.

## Run tests
```powershell
py -m pytest -v
```

## Run with Docker
```powershell
docker build -t stockpilot-inventory:local .
docker run --rm -p 5000:5000 stockpilot-inventory:local
```
Open `http://127.0.0.1:5000`.

## Jenkins
The included Jenkinsfile is written for a Windows Jenkins agent and uses `bat` steps. Ensure the Jenkins agent has Python, pip, Docker Desktop (with Linux containers), and Git installed and available on PATH. Create a Pipeline job, select **Pipeline script from SCM**, choose Git, enter your GitHub repository URL, select branch `*/main`, and set Script Path to `Jenkinsfile`.

Pipeline stages: Checkout → Install Dependencies → Run Automated Tests → Build Docker Image → Deploy Locally.

If Jenkins runs on Linux instead, replace `bat` with `sh` and adapt the Docker cleanup command.

## Terraform (AWS)
The `terraform/` directory defines a small demo EC2 instance and security group in the default VPC. It uses the AWS provider and Ubuntu 22.04 AMI lookup.

Prerequisites: Terraform CLI, AWS CLI, and AWS credentials configured with permission to read the default VPC/subnets and create EC2/security-group resources.

From the `terraform` folder:
```powershell
terraform init
terraform validate
terraform plan
terraform apply
```
Review the plan and expected AWS charges before applying. To remove resources created by this demo:
```powershell
terraform destroy
```

Important:
- `terraform plan` does not create resources.
- `terraform apply` can create billable AWS resources. Check current AWS pricing and your account eligibility first.
- The EC2 instance only installs Docker. You must deploy the application container separately to make the application URL work.
- SSH is restricted by default to `127.0.0.1/32` (effectively no remote access). If you need SSH, set `allowed_ssh_cidr` to your own public IP followed by `/32`.
- Never commit AWS access keys, `.tfstate` files, or real secrets to GitHub.

## GitHub upload
Create a new empty GitHub repository, then:
```powershell
git init
git add .
git commit -m "Initial StockPilot inventory application"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/stockpilot-inventory.git
git push -u origin main
```

## Suggested evidence screenshots
1. VS Code project structure
2. Dashboard in browser
3. Add product form and successful added product
4. GitHub repository files
5. Jenkins job configuration (Pipeline from SCM)
6. Jenkins stage view with successful stages
7. Jenkins console output and pytest results
8. Docker image and running container (`docker images`, `docker ps`)
9. Terraform directory files
10. `terraform init` success
11. `terraform validate` success
12. `terraform plan` output
13. `terraform apply` and AWS EC2 instance only if you actually apply
14. Browser access to deployed app only if you actually deploy it

## API quick checks
- `GET /health`
- `GET /api/products`
