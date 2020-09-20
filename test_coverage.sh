export COVERAGE_REPORT_DIR='coverage_report'
mkdir -p $COVERAGE_REPORT_DIR

# cleanup the old coverage data (and silence output)
{
  rm -rf $COVERAGE_REPORT
  mkdir $COVERAGE_REPORT
  coverage erase
} &> /dev/null

# run coverage
coverage run  --source='.' manage.py test apps common --no-input

if [ $? -eq 0 ]; then
    coverage report
    coverage xml -o $COVERAGE_REPORT_DIR/coverage.xml
    echo OK
fi