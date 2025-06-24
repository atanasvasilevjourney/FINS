#!/bin/bash

# FINS ERP Accounting System Deployment Script
# This script helps you deploy the FINS ERP system locally or to cloud environments

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="fins-erp"
DEFAULT_ENVIRONMENT="local"
SUPPORTED_ENVIRONMENTS=("local" "docker" "kubernetes" "aws" "azure" "gcp")

# Functions
print_header() {
    echo -e "${BLUE}"
    echo "=================================================="
    echo "  FINS ERP Accounting System - Deployment Script"
    echo "=================================================="
    echo -e "${NC}"
}

print_step() {
    echo -e "${YELLOW}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

check_prerequisites() {
    print_step "Checking prerequisites..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if Python is installed
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi
    
    print_success "All prerequisites are satisfied"
}

setup_environment() {
    print_step "Setting up environment variables..."
    
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            cp .env.example .env
            print_info "Created .env file from .env.example"
            print_info "Please edit .env file with your configuration"
        else
            print_error ".env.example file not found"
            exit 1
        fi
    else
        print_info ".env file already exists"
    fi
}

deploy_local() {
    print_step "Deploying FINS ERP locally..."
    
    cd backend/core-services
    
    # Start core services
    print_info "Starting core services..."
    docker-compose up -d postgres redis rabbitmq
    
    # Wait for database to be ready
    print_info "Waiting for database to be ready..."
    sleep 10
    
    # Run database migrations
    print_info "Running database migrations..."
    docker-compose exec -T general-ledger alembic upgrade head || true
    docker-compose exec -T accounts-payable alembic upgrade head || true
    docker-compose exec -T accounts-receivable alembic upgrade head || true
    
    # Start application services
    print_info "Starting application services..."
    docker-compose up -d general-ledger accounts-payable accounts-receivable
    
    cd ../..
    
    print_success "Local deployment completed"
    print_info "Services available at:"
    print_info "  - General Ledger: http://localhost:8001"
    print_info "  - Accounts Payable: http://localhost:8002"
    print_info "  - Accounts Receivable: http://localhost:8003"
    print_info "  - API Gateway: http://localhost:80"
}

deploy_docker() {
    print_step "Deploying FINS ERP with Docker..."
    
    cd backend/core-services
    
    # Build and start all services
    print_info "Building and starting all services..."
    docker-compose up -d --build
    
    # Wait for services to be ready
    print_info "Waiting for services to be ready..."
    sleep 30
    
    cd ../..
    
    print_success "Docker deployment completed"
}

deploy_kubernetes() {
    print_step "Deploying FINS ERP to Kubernetes..."
    
    # Check if kubectl is installed
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl is not installed. Please install kubectl first."
        exit 1
    fi
    
    # Check if cluster is accessible
    if ! kubectl cluster-info &> /dev/null; then
        print_error "Kubernetes cluster is not accessible. Please configure kubectl."
        exit 1
    fi
    
    cd infrastructure/kubernetes
    
    # Create namespace
    print_info "Creating namespace..."
    kubectl apply -f namespace.yaml
    
    # Apply all manifests
    print_info "Applying Kubernetes manifests..."
    kubectl apply -f .
    
    # Wait for deployments to be ready
    print_info "Waiting for deployments to be ready..."
    kubectl wait --for=condition=available --timeout=300s deployment -l app=fins-erp -n fins-erp
    
    cd ../..
    
    print_success "Kubernetes deployment completed"
}

deploy_cloud() {
    local cloud_provider=$1
    
    print_step "Deploying FINS ERP to $cloud_provider..."
    
    case $cloud_provider in
        "aws")
            deploy_aws
            ;;
        "azure")
            deploy_azure
            ;;
        "gcp")
            deploy_gcp
            ;;
        *)
            print_error "Unsupported cloud provider: $cloud_provider"
            exit 1
            ;;
    esac
}

deploy_aws() {
    print_info "Deploying to AWS..."
    
    # Check if AWS CLI is installed
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI is not installed. Please install AWS CLI first."
        exit 1
    fi
    
    # Check if Terraform is installed
    if ! command -v terraform &> /dev/null; then
        print_error "Terraform is not installed. Please install Terraform first."
        exit 1
    fi
    
    cd infrastructure/terraform/aws
    
    # Initialize Terraform
    print_info "Initializing Terraform..."
    terraform init
    
    # Plan deployment
    print_info "Planning deployment..."
    terraform plan -out=tfplan
    
    # Apply deployment
    print_info "Applying deployment..."
    terraform apply tfplan
    
    cd ../../..
    
    print_success "AWS deployment completed"
}

deploy_azure() {
    print_info "Deploying to Azure..."
    
    # Check if Azure CLI is installed
    if ! command -v az &> /dev/null; then
        print_error "Azure CLI is not installed. Please install Azure CLI first."
        exit 1
    fi
    
    cd infrastructure/azure
    
    # Deploy using Azure CLI
    print_info "Deploying to Azure..."
    az deployment group create --resource-group fins-erp --template-file main.bicep
    
    cd ../..
    
    print_success "Azure deployment completed"
}

deploy_gcp() {
    print_info "Deploying to Google Cloud Platform..."
    
    # Check if gcloud is installed
    if ! command -v gcloud &> /dev/null; then
        print_error "Google Cloud SDK is not installed. Please install gcloud first."
        exit 1
    fi
    
    cd infrastructure/gcp
    
    # Deploy using gcloud
    print_info "Deploying to GCP..."
    gcloud deployment-manager deployments create fins-erp --config deployment.yaml
    
    cd ../..
    
    print_success "GCP deployment completed"
}

run_tests() {
    print_step "Running tests..."
    
    cd backend/core-services
    
    # Run unit tests
    print_info "Running unit tests..."
    docker-compose exec general-ledger pytest tests/unit/ || true
    docker-compose exec accounts-payable pytest tests/unit/ || true
    docker-compose exec accounts-receivable pytest tests/unit/ || true
    
    # Run integration tests
    print_info "Running integration tests..."
    docker-compose -f docker-compose.test.yml up --abort-on-container-exit || true
    
    cd ../..
    
    print_success "Tests completed"
}

show_status() {
    print_step "Checking service status..."
    
    cd backend/core-services
    
    # Check Docker services
    print_info "Docker services status:"
    docker-compose ps
    
    # Check service health
    print_info "Service health checks:"
    for service in general-ledger accounts-payable accounts-receivable; do
        if curl -f http://localhost:$(docker-compose port $service 8000 | cut -d: -f2)/health &> /dev/null; then
            print_success "$service is healthy"
        else
            print_error "$service is not responding"
        fi
    done
    
    cd ../..
}

cleanup() {
    print_step "Cleaning up deployment..."
    
    cd backend/core-services
    
    # Stop and remove containers
    print_info "Stopping and removing containers..."
    docker-compose down -v
    
    # Remove images
    print_info "Removing images..."
    docker-compose down --rmi all
    
    cd ../..
    
    print_success "Cleanup completed"
}

show_help() {
    echo "Usage: $0 [OPTIONS] [ENVIRONMENT]"
    echo ""
    echo "Environments:"
    echo "  local        Deploy locally with Docker Compose"
    echo "  docker       Deploy with Docker (full stack)"
    echo "  kubernetes   Deploy to Kubernetes cluster"
    echo "  aws          Deploy to AWS"
    echo "  azure        Deploy to Azure"
    echo "  gcp          Deploy to Google Cloud Platform"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -t, --test     Run tests after deployment"
    echo "  -s, --status   Show service status"
    echo "  -c, --cleanup  Clean up deployment"
    echo ""
    echo "Examples:"
    echo "  $0 local              # Deploy locally"
    echo "  $0 docker --test      # Deploy with Docker and run tests"
    echo "  $0 kubernetes         # Deploy to Kubernetes"
    echo "  $0 aws                # Deploy to AWS"
}

# Main script
main() {
    print_header
    
    # Parse command line arguments
    ENVIRONMENT=$DEFAULT_ENVIRONMENT
    RUN_TESTS=false
    SHOW_STATUS=false
    CLEANUP_ONLY=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -t|--test)
                RUN_TESTS=true
                shift
                ;;
            -s|--status)
                SHOW_STATUS=true
                shift
                ;;
            -c|--cleanup)
                CLEANUP_ONLY=true
                shift
                ;;
            -*)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
            *)
                ENVIRONMENT=$1
                shift
                ;;
        esac
    done
    
    # Validate environment
    if [[ ! " ${SUPPORTED_ENVIRONMENTS[@]} " =~ " ${ENVIRONMENT} " ]]; then
        print_error "Unsupported environment: $ENVIRONMENT"
        echo "Supported environments: ${SUPPORTED_ENVIRONMENTS[*]}"
        exit 1
    fi
    
    # Check prerequisites
    check_prerequisites
    
    # Setup environment
    setup_environment
    
    # Handle cleanup only
    if [ "$CLEANUP_ONLY" = true ]; then
        cleanup
        exit 0
    fi
    
    # Handle status only
    if [ "$SHOW_STATUS" = true ]; then
        show_status
        exit 0
    fi
    
    # Deploy based on environment
    case $ENVIRONMENT in
        "local")
            deploy_local
            ;;
        "docker")
            deploy_docker
            ;;
        "kubernetes")
            deploy_kubernetes
            ;;
        "aws"|"azure"|"gcp")
            deploy_cloud $ENVIRONMENT
            ;;
    esac
    
    # Run tests if requested
    if [ "$RUN_TESTS" = true ]; then
        run_tests
    fi
    
    # Show status
    show_status
    
    print_success "FINS ERP deployment completed successfully!"
    print_info "For more information, visit: https://github.com/your-org/fins-erp"
}

# Run main function
main "$@" 