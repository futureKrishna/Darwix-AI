# CI/CD Setup Guide

## 🔧 Setting Up CI/CD Pipeline

### 1. GitHub Actions Setup

The CI/CD pipeline is automatically triggered on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

### 2. Required GitHub Secrets

Set up the following secrets in your GitHub repository settings:

```bash
# Docker Hub credentials (for image publishing)
DOCKER_USERNAME=your-dockerhub-username
DOCKER_PASSWORD=your-dockerhub-token

# Optional: Codecov token for coverage reporting
CODECOV_TOKEN=your-codecov-token
```

### 3. Repository Setup Steps

1. **Fork or clone the repository**
2. **Configure GitHub Secrets**:
   - Go to Repository Settings → Secrets and variables → Actions
   - Add the required secrets listed above

3. **Enable GitHub Actions**:
   - Actions are enabled by default for new repositories
   - The workflow will run automatically on the next push

### 4. Local Development Setup

Install pre-commit hooks for local quality checks:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install

# Test the full local CI pipeline
./test-ci.sh    # Linux/Mac
test-ci.bat     # Windows
```

### 5. Pipeline Status and Monitoring

Monitor your CI/CD pipeline:
- **Actions Tab**: View running and completed workflows
- **Pull Requests**: See status checks before merging
- **Badges**: Add status badges to your README

Example status badge:
```markdown
![CI Pipeline](https://github.com/yourusername/darwix-ai/workflows/CI%20Pipeline/badge.svg)
```

### 6. Troubleshooting Common Issues

#### **Test Failures**
- Check test output in the "Test Job" logs
- Run tests locally: `make test`
- Ensure 90% coverage requirement is met

#### **Docker Build Failures**
- Verify Dockerfile syntax
- Check for missing dependencies in requirements.txt
- Test locally: `make docker-test`

#### **Type Check Failures**
- Run locally: `mypy app/ --ignore-missing-imports`
- Fix type annotations in your code
- Update mypy.ini if needed

#### **Security Scan Failures**
- Review Bandit security warnings
- Update vulnerable dependencies with `safety check`
- Add security exclusions if false positives

### 7. Customizing the Pipeline

Modify `.github/workflows/ci.yml` to:
- Add new test environments
- Include additional security scans
- Deploy to different cloud platforms
- Add performance benchmarks

### 8. Production Deployment

The pipeline automatically:
- Builds Docker images on successful tests
- Pushes images to Docker Hub (main branch only)
- Includes proper tagging and labeling
- Provides deployment-ready artifacts

Use the Docker images for deployment:
```bash
docker pull yourusername/darwix-ai:latest
docker run -p 8000:8000 yourusername/darwix-ai:latest
```
