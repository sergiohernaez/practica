pipeline {
    agent any

     stages {
        stage('Get Code') {
            steps {
                git 'https://github.com/sergiohernaez/practica.git'
            }
        }

    stage('Build') {
        steps {
            echo 'Eyyyy, esto es Python. No hay que compilar nada!!!'
	    echo WORKSPACE
	    bat 'dir'
        }
    }

    stage('Tests')
    {
        parallel {

            stage('Unit') {
                agent{label 'agent1'}
                steps {
                    catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                        bat '''
                            set PYTHONPATH=%WORKSPACE%
                            coverage run --branch --source=app --omit=app\\__init__.py,app\\app.py -m pytest --junitxml=result-unit.xml test\\unit
                            coverage xml
                        '''
                    }
                    stash name:'result-unit', includes:'result-unit.xml'
                }
            }

            stage('Rest') {
                agent{label 'agent2'}
                steps {sleep time: 3000, unit: 'MILLISECONDS'
                    catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                        bat '''
                            set FLASK_APP=app\\app.py
                            set FLASK_ENV=development
                            start flask run
                            start java -jar C:\\Unir\\Ejercicios\\wiremock\\wiremock-jre8-standalone-2.28.0.jar --port 9090 --root-dir test\\wiremock
                            set PYTHONPATH=%WORKSPACE%
                            pytest --junitxml=result-rest.xml test\\rest
                        '''
                        stash name:'result-rest', includes:'result-rest.xml'
                    }
                }
            }

            stage('Coverage') {
                steps {
                    recordCoverage qualityGates: [[integerThreshold: 95, metric: 'LINE', threshold: 95.0], [criticality: 'ERROR', integerThreshold: 85, metric: 'LINE', threshold: 85.0], [criticality: 'NOTE', metric: 'MODULE']], tools: [[parser: 'COBERTURA', pattern: 'coverage.xml']]
                }
            }
        }
    }
    
    stage ('Results') {
        steps {
            unstash name: 'result-rest'
            unstash name: 'result-unit'
            junit 'result*.xml'
        }
    }
  }
}
