::set path where everything is
cd /d E:\Extra\API\se_exercise\Dashboard_2Dim
::Open both ports running dashboards

::explorer "http://127.0.0.1:1010/"
::Open dashboards server run in separate cdm view
start cmd.exe /c "python Dashboard.py"
::start cmd.exe /c "python DatasetEx.py"
explorer "http://127.0.0.1:8000/"
::close main cdm view
exit

