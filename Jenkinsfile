pipeline {
    agent any

     stages {
        stage('Get Code') {
            steps {
                git 'https://github.com/sergiohernaez/practica.git'
            }
        }



                stage('Unit') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            bat '''
                                set PYTHONPATH=%WORKSPACE%
                                coverage run --branch --source=app --omit=app\\__init__.py,app\\app.py -m pytest --junitxml=result-unit.xml test\\unit
                            '''
                            junit 'result-unit.xml'
                        }
                        stash name:'result-unit', includes:'result-unit.xml'
                    }
                }

                stage('Rest') {
                    steps { sleep time: 1000, unit: 'MILLISECONDS'
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            bat '''
                                set FLASK_APP=app\\app.py
                                set FLASK_ENV=development
                                flask run
                                java -jar C:\\Unir\\Ejercicios\\wiremock\\wiremock-jre8-standalone-2.28.0.jar --port 9090 --root-dir test\\wiremock
                                set PYTHONPATH=%WORKSPACE%
                                pytest --junitxml=result-rest.xml test\\rest
                            '''
                            stash name:'result-rest', includes:'result-rest.xml'
                        }
                    }
                }

                stage('Coverage') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            bat '''
                                 coverage xml
                            '''
                        }
                        recordCoverage qualityGates: [[integerThreshold: 95, metric: 'LINE', threshold: 95.0], [criticality: 'ERROR', integerThreshold: 85, metric: 'LINE', threshold: 85.0], [criticality: 'NOTE', metric: 'MODULE']], tools: [[parser: 'COBERTURA', pattern: 'coverage.xml']]
                    }
                }


                stage('Static') {
                    steps {
                        bat '''
                            flake8 --exit-zero --format=pylint app >flake8.out
                        '''
                        recordIssues qualityGates: [[criticality: 'NOTE', integerThreshold: 10, threshold: 10.0, type: 'TOTAL']], sourceCodeRetention: 'LAST_BUILD', tools: [pyLint(pattern: 'flake8.out')]
                    }
                }


                stage('Security') {
                    steps {
                        bat '''
                             bandit --exit-zero -r . -f custom -o bandit.out --msg-template "{abspath}:{line}: {severity}: {test_id}: {msg}"
                        '''
                        recordIssues qualityGates: [[threshold: 1, type: 'TOTAL', unstable: true]], sourceCodeRetention: 'LAST_BUILD', tools: [pyLint(pattern: 'bandit.out')]
                    }
                }

                stage('Performance') {
                    steps { sleep time: 4000, unit: 'MILLISECONDS'
                        bat '''
                            set FLASK_APP=app\\app.py
                            set FLASK_ENV=development
                            flask --app app/app.py run
                            C:\\UNIR\\Ejercicios\\apache-jmeter-5.6.3\\bin\\jmeter -n -t test\\jmeter\\flask.jmx -f -l flask.jtl
                        '''
                        perfReport sourceDataFiles: 'flask.jtl'
                    }
                }
            }

}
