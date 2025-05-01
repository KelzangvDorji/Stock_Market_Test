pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_DIR = "market-risk-website/backend"
        GIT_BRANCH = "${env.BRANCH_NAME}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                bat """
                    echo "Current branch: %GIT_BRANCH%"
                    git config --global user.name "Jenkins"
                    git config --global user.email "jenkins@example.com"
                    git status
                """
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
                        curl -v http://localhost:8000/health
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
                    git tag -a "v${BUILD_NUMBER}" -m "Production release ${BUILD_NUMBER}"
                    git push origin "v${BUILD_NUMBER}"
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

        success {
            bat """
                echo "Pipeline succeeded. Current commit:"
                git rev-parse HEAD
            """
        }

        failure {
            echo "Pipeline failed. Check logs and health checks."
            bat """
                echo "Last commit:"
                git rev-parse HEAD
                echo "Git status:"
                git status
            """
        }
    }
}
