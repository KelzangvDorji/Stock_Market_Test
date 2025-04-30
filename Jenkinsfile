pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_DIR = "market-risk-website/backend"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Run with Docker Compose') {
            steps {
                dir("${COMPOSE_PROJECT_DIR}") {
                    bat """
                        echo "Bringing down any existing containers..."
                        docker-compose down

                        echo "Building and starting containers..."
                        docker-compose up --build -d
                        
                        echo "Waiting for containers to stabilize..."
                        timeout /t 10 > nul
                        
                        echo "Checking backend health endpoint..."
                        curl -v http://localhost:5000/health
                        if errorlevel 1 (
                            echo "Health check failed!"
                            exit /b 1
                        )
                    """
                }
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                bat """
                    echo "Deploying to production..."
                    rem Add production deployment steps here
                    rem Example: docker-compose push, etc.
                """
            }
        }
    }

    post {
        always {
            dir("${COMPOSE_PROJECT_DIR}") {
                bat """
                    echo "Stopping containers and pruning Docker..."
                    docker-compose down
                    docker system prune -f
                """
            }
            cleanWs()
        }

        failure {
            echo "Pipeline failed. Check logs and health checks."
        }
    }
}
