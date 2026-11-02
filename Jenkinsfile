```groovy
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Source code is checked out from GitHub.'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
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
                bat '"C:\\Users\\netra\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" build -t stockpilot-inventory:%BUILD_NUMBER% .'
            }
        }

        stage('Deploy Locally') {
            steps {
                bat '"C:\\Users\\netra\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" rm -f stockpilot-inventory || exit /b 0'
                bat '"C:\\Users\\netra\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" run -d --name stockpilot-inventory -p 5000:5000 stockpilot-inventory:%BUILD_NUMBER%'
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
```