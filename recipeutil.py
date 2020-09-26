from datetime import datetime
import json
import os.path
import string

class Adjuster:
    def __init__(self, templateFilePath, inputFilePath, outputFilePath):
        with open(templateFilePath) as templateFile:
            self._template = string.Template(templateFile.read())
        with open(inputFilePath) as inputFile:
            self._inputValues = json.load(inputFile)
        self._outputFilePath = outputFilePath
        self._computedValues = {}

    def get_input(self, paramName):
        return self._inputValues[paramName]

    def get_input_time(self, paramName):
        return datetime.strptime(self._inputValues[paramName], '%H:%M')

    def get_input_dur(self, paramName):
        return self.get_input_time(paramName) - datetime(1900, 1, 1, 0, 0, 0)

    def get_input_perc(self, paramName):
        return self._inputValues[paramName] / 100.

    def set_template_variable(self, name, value):
        self._computedValues[name] = value

    def set_template_var_time(self, name, time):
        self._computedValues[name] = time.strftime('%H:%M')

    def set_template_var_dur(self, name, duration):
        timeRep = datetime(1900, 1, 1) + duration
        self._computedValues[name] = timeRep.strftime('%H:%M')

    def set_template_var_grams(self, name, amount):
        self._computedValues[name] = '{:.0f}g'.format(amount)

    def set_template_var_percent(self, name, percent):
        self._computedValues[name] = '{:.0f}%'.format(percent * 100.)

    def compute_values(self):
        pass

    def generate_recipe(self):
        self.compute_values()
        recipeText = self._template.substitute(self._computedValues)
        directory = os.path.dirname(self._outputFilePath)
        if (not os.path.exists(directory) and not directory == ''):
            os.mkdir(directory)

        with open(self._outputFilePath, 'w') as outputFile:
            outputFile.write(recipeText)
