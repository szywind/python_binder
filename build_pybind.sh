g++ -O3 -Wall -Werror -shared -std=c++11 -fPIC `python -m pybind11 --includes` -I /usr/include/python3.8 -I . pybind11_wrapper.cpp -o pybind11_example`python3.8-config --extension-suffix`
-L. -lcppmult -Wl,-rpath,.