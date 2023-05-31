pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('DockerHub')
    }
    stages {
        parallel(
            stage('Docker Build') {
                agent any
                steps {
                sh 'docker build -t hieupham0607/selenoid-py:${BUILD_NUMBER} .'
              }
            }
            stage('Login') {
              steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
              }
            }
        )
        stage('Push') {
          steps {
            sh 'docker push hieupham0607/selenoid-py:${BUILD_NUMBER}'
          }
        }
    }
}