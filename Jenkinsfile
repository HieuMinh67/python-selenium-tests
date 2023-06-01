pipeline {
  parameters {
    string(defaultValue: 'Space-1', name: 'SpaceId', description: '', trim: true)
    string(defaultValue: 'Octopus', name: 'ServerId', description: '', trim: true)
    string(defaultValue: 'Selenoid', name: 'ProjectName', description: '', trim: true)
  }
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

    stage('Deployment') {
      steps {
        octopusCreateRelease(
          project: params.ProjectName,
          serverId: params.ServerId,
          spaceId: params.SpaceId,
          toolId: 'Default')
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