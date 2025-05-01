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
                        ping -n 30 127.0.0.1 > nul
                        
                        echo "Checking container status..."
                        docker-compose ps
                        
                        echo "Checking backend health endpoint..."
                        for /l %%i in (1,1,5) do (
                            curl -v http://localhost:8000/health
                            if not errorlevel 1 (
                                echo "Health check passed!"
                                exit /b 0
                            )
                            echo "Attempt %%i failed, retrying in 5 seconds..."
                            ping -n 5 127.0.0.1 > nul
                        )
                        echo "Health check failed after 5 attempts!"
                        echo "Checking container logs..."
                        docker-compose logs backend
                        exit /b 1
                    """
                }
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
        }

        success {
            bat """
                echo "Pipeline succeeded. Current commit:"
                git rev-parse HEAD
            """
        }

        failure {
            echo "Pipeline failed. Check logs and health checks."
            dir("${COMPOSE_PROJECT_DIR}") {
                bat """
                    echo "Container logs:"
                    docker-compose logs
                """
            }
        }
    }
}
