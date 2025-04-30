pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
        VENV_PATH = 'venv'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                bat """
                    python -m venv %VENV_PATH%
                    call %VENV_PATH%\\Scripts\\activate
                    pip install -r market-risk-website\\backend\\requirements.txt
                """
            }
        }
        
        stage('Lint') {
            steps {
                bat """
                    call %VENV_PATH%\\Scripts\\activate
                    pip install flake8
                    flake8 market-risk-website\\backend\\
                """
            }
        }
        
        stage('Test') {
            steps {
                bat """
                    call %VENV_PATH%\\Scripts\\activate
                    cd market-risk-website\\backend
                    python -m pytest tests\\
                """
            }
        }
        
        stage('Build') {
            steps {
                bat """
                    call %VENV_PATH%\\Scripts\\activate
                    cd market-risk-website\\backend
                    start /B python app.py
                    timeout /t 5
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
                    rem For example: deploying to a cloud platform or updating a server
                """
            }
        }
    }
    
    post {
        always {
            bat """
                taskkill /F /IM python.exe /FI "WINDOWTITLE eq app.py" || exit 0
            """
            cleanWs()
        }
    }
} 