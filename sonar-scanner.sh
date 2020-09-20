sonar-scanner \
  -Dsonar.projectKey=soCan \
  -Dsonar.sources=. \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.login= \
  -Dsonar.python.coverage.reportPaths=./coverage_report/coverage.xml \
  -Dsonar.exclusions=manage.py,apps/fb/**,**/*.js/*,**/*.css
