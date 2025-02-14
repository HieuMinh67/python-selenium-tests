pipeline {
  parameters {
    string(defaultValue: 'Production', description: '', name: 'EnvironmentName', trim: true)
    string(defaultValue: 'Spaces-1', name: 'SpaceId', description: '', trim: true)
    string(defaultValue: 'Local', name: 'ServerId', description: '', trim: true)
    string(defaultValue: 'Development Project', name: 'ProjectName', description: '', trim: true)
    string(defaultValue: 'main', name: 'GitRef', description: '', trim: true)
    booleanParam(name: 'IsDeploy', defaultValue: false, description: '')
  }
  agent { node { label 'local' } }
  options {
      skipDefaultCheckout(true)
  }
  stages {
    stage("Custom checkout") {
      steps {
        checkout scmGit(
          branches: [[name: "*/master"]],
          userRemoteConfigs: [[credentialsId: "gogs", url: "http://localhost:10880/henry/Selenoid"]]
        )
      }
    }
    stage('Parallel Setup') {
      parallel {
        stage('Notify on Slack') {
          steps {
            slackSend(channel: "#lab", message: "New build(${BUILD_NUMBER}) have been created")
          }
        }

        stage('Dependencies check') {
          steps {
            dependencyCheck additionalArguments: 'scan="." --format HTML', odcInstallation: 'OWASP'
          }
        }

        stage('Docker Build') {
          steps {
            sh 'docker build -t hieupham0607/selenoid-py:${BUILD_NUMBER} --progress=plain . 2>&1 | tee logs.txt'
          }
        }

        stage('Code quality') {
          steps {
            sh 'docker run --rm --net=host -v $PWD:/selenoid sonarsource/sonar-scanner-cli sonar-scanner \
                -D sonar.projectBaseDir=/selenoid \
                -D sonar.host.url=http://localhost:9090 \
                -D sonar.login=50bb61ad483f36bcc4a34dab4dc7b09828805ea1 \
                -D sonar.sources=. \
                -D sonar.python.coverage.reportPaths=coverage.xml \
                -D sonar.dependencyCheck.htmlReportPath=dependency-check-report.html'
          }
        }

        stage('Login') { 
          steps {
            sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin 2>&1 | tee push.txt'
          }
        }

      }
    }

    stage('Run tests') {
      steps {
        sh 'docker run --rm -v $(pwd):/app -e SELNOID_HOST=selenoid --network host hieupham0607/selenoid-py:${BUILD_NUMBER} pytest --cov-report xml:coverage.xml --cov=main'
      }
    }

    stage('Push') {
      steps {
        sh 'docker push hieupham0607/selenoid-py:${BUILD_NUMBER}'
      }
    }

    stage('Release') {
      steps {
        octopusCreateRelease(
          project: params.ProjectName,
          serverId: params.ServerId,
          spaceId: params.SpaceId,
          releaseVersion: env.BUILD_NUMBER,
          gitRef: params.GitRef,
          toolId: 'Default')
      }
    }

    stage('Deploy') {
      when {
        expression {params.IsDeploy == true}
      }
      steps {
        octopusDeployRelease(
          project: params.ProjectName,
          releaseVersion: env.BUILD_NUMBER,
          serverId: params.ServerId,
          spaceId: params.SpaceId,
          environment: params.EnvironmentName,
          toolId: 'Default')
      }
    }
  }
  environment {
    DOCKERHUB_CREDENTIALS = credentials('DockerHub')
  }
  post {
    success {
        archiveArtifacts(artifacts: '**\\*')
    }
  }
}