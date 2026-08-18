pipeline {

    agent any

    stages {

        stage('Checkout') {

            steps {

                checkout scm

            }

        }

        stage('Install Dependencies') {

            steps {

                bat 'python -m pip install --upgrade pip'

                bat 'pip install -r requirements.txt'

            }

        }

        stage('Run Tests') {

            steps {

                bat 'python manage.py test'

            }

        }

        stage('Check Django') {

            steps {

                bat 'python manage.py check'

            }

        }

    }

    post {

        success {

            echo 'Build and tests completed successfully.'

        }

        failure {

            echo 'Build failed. Check the console output.'

        }

    }

}