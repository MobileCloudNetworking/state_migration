#!/bin/bash
kill -9 $(lsof -i:25333 -t)
/usr/bin/yes | sudo pip uninstall py4j
sudo pip install py4j

javac -cp py4j/Jama-1.0.2.jar:py4j/py4j0.9.1.jar py4j/Grey.java py4j/IFilter.java
java -cp .:py4j/Jama-1.0.2.jar:py4j/py4j0.9.1.jar py4j/Grey py4j/IFilter &
