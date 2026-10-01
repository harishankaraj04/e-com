pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'cursor/flask-ecommerce-storefront',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/harishankaraj04/e-com.git'
            }
        }

        stage('Python Setup') {
            steps {
                sh '''
                    python3 --version
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    ./venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    ./venv/bin/python -m py_compile app.py
                    echo "Python syntax test passed"
                '''
            }
        }
    }

    post {
        success {
            echo 'CI Pipeline completed successfully!'
        }

        failure {
            echo 'CI Pipeline failed!'
        }
    }
}
