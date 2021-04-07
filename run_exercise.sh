python3 -m pip install virtualenv
cd ..
virtualenv logical-clock 2&>/dev/null
source logical-clock/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install grpcio
python3 -m pip install grpcio-tools
python3 -m pip install protobuf

cd logical-clock/CSE531

# Debug
#python3 -m pdb Main.py -i test1.json -o output.json

# Test 1
python3 Main.py -i test1.json -o output1.json

# Test 2
#python3 Main.py -i test2.json -o output2.json