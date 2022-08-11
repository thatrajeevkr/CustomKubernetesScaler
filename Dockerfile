FROM custompodautoscaler/python:latest
ADD config.yaml evaluate.py metric.py /