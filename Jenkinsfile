pipeline {
    agent any
    options {
        timestamps()
        disableConcurrentBuilds()
    }
    stages {
        stage('Checkout') {
            steps {
                echo 'Source code is checked out from the configured GitHub repository.'
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements.txt'
            }
        }
        stage('Run Automated Tests') {
            steps {
                bat 'python -m pytest -v'
            }
        }
        stage('Build Docker Image') {
            steps {
                bat 'docker build -t stockpilot-inventory:%BUILD_NUMBER% .'
            }
        }
        stage('Deploy Locally') {
            steps {
                bat 'docker rm -f stockpilot-inventory || exit /b 0'
                bat 'docker run -d --name stockpilot-inventory -p 5000:5000 stockpilot-inventory:%BUILD_NUMBER%'
            }
        }
    }
    post {
        success {
            echo 'SUCCESS: Inventory application passed tests, built and deployed.'
        }
        failure {
            echo 'FAILED: Check the stage logs above to identify the issue.'
        }
    }
}
