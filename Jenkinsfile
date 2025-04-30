pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build and Test') {
            steps {
                bat """
                    echo "Current directory:"
                    dir
                    echo "Checking Dockerfile location:"
                    dir market-risk-website\\backend
                    echo "Stopping any existing containers..."
                    docker-compose down
                    echo "Building Docker image..."
                    docker-compose build --no-cache
                    echo "Starting services..."
                    docker-compose up -d
                    echo "Waiting for services to start..."
                    timeout /t 30
                    echo "Checking MongoDB health..."
                    docker-compose ps
                    echo "Checking backend logs..."
                    docker-compose logs backend
                    echo "Testing health endpoint..."
                    curl -v http://localhost:5000/health
                """
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                bat """
                    echo "Deploying to production..."
                    rem Add your deployment steps here
                    rem For example: pushing to a container registry
                    rem docker-compose push
                """
            }
        }
    }
    
    post {
        always {
            bat """
                echo "Cleaning up..."
                docker-compose down
                docker system prune -f
            """
            cleanWs()
        }
    }
} 