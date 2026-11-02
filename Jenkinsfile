
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out StockPilot source code from GitHub'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Automated Tests') {
            steps {
                echo 'Running automated tests using Pytest'
                bat 'python -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building StockPilot Docker image'
                bat '"C:\\Users\\netra\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" build -t stockpilot-inventory:%BUILD_NUMBER% .'
            }
        }

        stage('Deploy Locally') {
            steps {
                echo 'Removing previous StockPilot container if present'

                bat '"C:\\Users\\netra\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" rm -f stockpilot-inventory || exit /b 0'

                echo 'Starting StockPilot application container'

                bat '"C:\\Users\\netra\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" run -d --name stockpilot-inventory -p 5000:5000 stockpilot-inventory:%BUILD_NUMBER%'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: StockPilot application tested, built and deployed successfully.'
        }

        failure {
            echo 'FAILED: Check Jenkins Console Output for errors.'
        }

        always {
            echo 'StockPilot CI/CD Pipeline execution completed.'
        }
    }
}
