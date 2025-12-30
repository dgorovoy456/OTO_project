pipeline {
    agent any

    environment {
            HOME = "${WORKSPACE}"
        XDG_CONFIG_HOME = "${WORKSPACE}/.config"
        XDG_CACHE_HOME  = "${WORKSPACE}/.cache"
        XDG_DATA_HOME   = "${WORKSPACE}/.local"
        SE_CACHE_PATH   = "${WORKSPACE}/.selenium"
    }
    stages {
        stage('Build environment') {
            steps {
                        sh '''
            python3.10 -m venv venv
            . venv/bin/activate
            pip install -r src/requirements.txt
        '''
            }
        }
        stage('Run tests') {
            steps {
                script {
                    def platforms = ''
                    if (params.Platform == "both") {
                        platforms = 'web,mobile'
                    }
                    else {
                        platforms = params.Platform
                    }
                    sh """
                . venv/bin/activate
                mkdir -p "\$SE_CACHE_PATH"
                export SE_CACHE_PATH="\$SE_CACHE_PATH"
                cd src/
                pytest --cache-clear --headless --platforms="${platforms}"
            """
                }
            }
        }
    }
        post {
        always {
            archiveArtifacts artifacts: 'src/reports/junit.xml, src/reports/report.html', allowEmptyArchive: true
            junit 'src/reports/junit.xml'
        }
        success {
            echo "Tests passed for platform: ${params.Platform}"
        }
        failure {
            echo "Tests failed for platform: ${params.Platform}"
        }
    }
}