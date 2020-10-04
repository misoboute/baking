from datetime import datetime
import json
import os.path
import string

class UnitConv:
    def __init__(self):
        with open("Ingredient-Densities.json") as desitiesFile:
            self._densities = json.load(desitiesFile)
        with open("Unit-Conv-Tables.json") as convTableFile:
            convTable = json.load(convTableFile)
            self._massConvTab = convTable['mass']
            self._volConvTab = convTable['volume']
            self._massConvTab[''] = 1
            self._volConvTab[''] = 1
    
    def get_density(self, material):
        if not material:
            raise RuntimeError(
                'Material type must be specified when converting '
                'mass to/from volum')

        if not material in self._densities:
            raise RuntimeError(
                'Failed to determine density of material "{material}". '
                'Entry not found!')

        return self._densities[material]

    def conv(self, value, toUnit, fromUnit = '', material = ''):
        if (material and not material in self._densities):
            raise RuntimeError('Unable to find density value for "{material}"')

        for u in (toUnit, fromUnit):
            for t in (self._massConvTab, self._volConvTab):
                if (u in t): break
            else:
                raise RuntimeError(
                    'Measurement unit "{u}" not found in conversion tables')

        if (toUnit in self._massConvTab):
            return self._conv_mass(value, toUnit, fromUnit, material)
        elif (toUnit in self._volConvTab):
            return self._conv_vol(value, toUnit, fromUnit, material)

    def conv_fmt(self, value, toUnit, fromUnit = '', material = '', fmt = '{}'):
        return (fmt + ' {}').format(
            self.conv(value, toUnit, fromUnit, material), toUnit)

    def _conv_mass(self, value, toUnit, fromUnit, material):
        if (fromUnit in self._volConvTab):
            valueG = (value * self.get_density(material) * 
                self._volConvTab[fromUnit])
            return valueG / self._massConvTab[toUnit]
        return value * self._massConvTab[fromUnit] / self._massConvTab[toUnit]

    def _conv_vol(self, value, toUnit, fromUnit, material):
        if (fromUnit in self._massConvTab):
            valueMl = (value / self.get_density(material) * 
                self._massConvTab[fromUnit])
            return valueMl / self._volConvTab[toUnit]
        return value * self._volConvTab[fromUnit] / self._volConvTab[toUnit]

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
