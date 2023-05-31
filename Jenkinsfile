pipeline {
  agent any
  stages {
    stage('Parallel Setup') {
      parallel {
        stage('Docker Build') {
          agent any
          steps {
            sh 'docker build -t hieupham0607/selenoid-py:${BUILD_NUMBER} --progress=plain . 2>&1 | tee logs.txt'
          }
        }

        stage('Login') {
          steps {
            sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin 2>&1 | tee push.txt'
          }
        }

      }
    }

    stage('Push') {
      steps {
        sh 'docker push hieupham0607/selenoid-py:${BUILD_NUMBER}'
      }
    }
  }
  environment {
    DOCKERHUB_CREDENTIALS = credentials('DockerHub')
  }
  post {
    always {
        archiveArtifacts(artifacts: '**\\*')
    }

  }
}