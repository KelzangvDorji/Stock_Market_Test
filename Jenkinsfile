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
                    if errorlevel 1 (
                        echo "Docker build failed!"
                        exit /b 1
                    )
                    echo "Starting services..."
                    docker-compose up -d
                    if errorlevel 1 (
                        echo "Failed to start services!"
                        exit /b 1
                    )
                    echo "Waiting for services to start..."
                    for /l %%x in (1,1,30) do (
                        echo Waiting... %%x
                        docker-compose ps | findstr "healthy" > nul
                        if not errorlevel 1 (
                            echo "Services are healthy"
                            goto :continue
                        )
                        timeout /t 1 > nul
                    )
                    echo "Services failed to start within timeout"
                    exit /b 1
                    :continue
                    echo "Checking MongoDB health..."
                    docker-compose ps
                    echo "Checking backend logs..."
                    docker-compose logs backend
                    echo "Testing health endpoint..."
                    curl -v http://localhost:5000/health
                    if errorlevel 1 (
                        echo "Health check failed!"
                        exit /b 1
                    )
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
        failure {
            echo "Pipeline failed! Check the logs for details."
        }
    }
} 