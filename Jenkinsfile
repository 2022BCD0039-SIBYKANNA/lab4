pipeline {
    agent any

    environment {
        DOCKERHUB_CREDS = credentials('dockerhub-creds')
        BEST_ACCURACY   = credentials('best-accuracy')
        IMAGE_NAME      = "sibykannabcd39/wine_predict_2022bcd0039"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                sh '''
                python3 -m venv venv
                venv/bin/pip install --upgrade pip
                venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                mkdir -p app/artifacts
                venv/bin/python scripts/train.py
                '''
            }
        }

        stage('Read Accuracy') {
            steps {
                script {
                    if (!fileExists('app/artifacts/metrics.json')) {
                        error("metrics.json not found!")
                    }

                    def metrics = readJSON file: 'app/artifacts/metrics.json'

                    if (!metrics.containsKey("accuracy")) {
                        error("Accuracy field not found in metrics.json!")
                    }

                    env.CURRENT_ACCURACY = metrics["accuracy"].toString()

                    echo "Current Accuracy: ${env.CURRENT_ACCURACY}"
                }
            }
        }

        stage('Compare Accuracy') {
            steps {
                script {

                    if (env.CURRENT_ACCURACY == null) {
                        error("Current accuracy is null!")
                    }

                    def best = BEST_ACCURACY.toDouble()
                    def current = env.CURRENT_ACCURACY.toDouble()

                    echo "Best Accuracy: ${best}"
                    echo "Current Accuracy: ${current}"

                    if (current > best) {
                        echo "Model improved! Proceeding with Docker build."
                        env.MODEL_IMPROVED = "true"
                    } else {
                        echo "Model did not improve."
                        env.MODEL_IMPROVED = "false"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            when {
                expression { env.MODEL_IMPROVED == "true" }
            }
            steps {
                sh """
                docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                """
            }
        }

        stage('Push Docker Image') {
            when {
                expression { env.MODEL_IMPROVED == "true" }
            }
            steps {
                sh """
                echo ${DOCKERHUB_CREDS_PSW} | docker login -u ${DOCKERHUB_CREDS_USR} --password-stdin
                docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                docker push ${IMAGE_NAME}:latest
                """
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'app/artifacts/**', allowEmptyArchive: true
        }
    }
}
