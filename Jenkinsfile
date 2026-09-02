pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out SmartComplaint from GitHub...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Django Check') {
            steps {
                echo 'Checking Django project...'
                bat 'python manage.py check'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running Django tests...'
                bat 'python manage.py test'
            }
        }
    }

    post {

        success {
            echo 'SMARTCOMPLAINT BUILD SUCCESSFUL'
        }

        failure {
            echo 'SMARTCOMPLAINT BUILD FAILED'
        }
    }
}