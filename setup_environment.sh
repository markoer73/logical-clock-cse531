# If you want graphical interface
#sudo apt install python3-tk

CURR=${PWD}
cd ..
virtualenv logical-clock 2&>/dev/null
source logical-clock/bin/activate
cd ${CURR}
bin/python3 -m pip install --upgrade pip
bin/python3 -m pip install --upgrade filelock
bin/python3 -m pip install --upgrade distlib
bin/python3 -m pip install --upgrade grpcio  --ignore-installed
bin/python3 -m pip install --upgrade grpcio-tools --ignore-installed
bin/python3 -m pip install --upgrade protobuf
bin/python3 -m pip install --upgrade pysimplegui

cd CSE531

