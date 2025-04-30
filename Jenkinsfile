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
                    docker-compose down
                    docker-compose build --no-cache
                    docker-compose up -d
                    timeout /t 10
                    curl http://localhost:5000/health
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
                docker-compose down
                docker system prune -f
            """
            cleanWs()
        }
    }
} 