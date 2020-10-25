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
                'mass to/from volume.')

        if not material in self._densities:
            raise RuntimeError(
                'Failed to determine density of material "{material}". '
                'Entry not found!')

        return self._densities[material]

    def conv(self, value, toUnit, fromUnit = '', material = '', roundOff = 0):
        if (material and not material in self._densities):
            raise RuntimeError('Unable to find density value for "{material}"')

        for u in (toUnit, fromUnit):
            for t in (self._massConvTab, self._volConvTab):
                if (u in t): break
            else:
                raise RuntimeError(
                    'Measurement unit "{u}" not found in conversion tables')

        if self.is_mass_unit(toUnit):
            convValue = self._conv_mass(value, toUnit, fromUnit, material)
        else:
            convValue = self._conv_vol(value, toUnit, fromUnit, material)
        
        if roundOff:
            convValue = round(convValue / roundOff) * roundOff

        return convValue

    def is_mass_unit(self, unit):
        return unit and unit in self._massConvTab

    def is_vol_unit(self, unit):
        return unit and unit in self._volConvTab

    def _conv_mass(self, value, toUnit, fromUnit, material):
        if (self.is_vol_unit(fromUnit)):
            valueG = (value * self.get_density(material) * 
                self._volConvTab[fromUnit])
            return valueG / self._massConvTab[toUnit]
        return value * self._massConvTab[fromUnit] / self._massConvTab[toUnit]

    def _conv_vol(self, value, toUnit, fromUnit, material):
        if (self.is_mass_unit(fromUnit)):
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
        self.unitConv = UnitConv()

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

    def fmt_templ_var_amount(self, name, value, unit = '', material = ''):
        if self.unitConv.is_vol_unit(unit) and not material:
            value = self.unitConv.conv(value, 'mL', unit, roundOff=5/8)
            if value >= 1000:
                valueMl = self.unitConv.conv(value, 'mL')
                self.set_template_variable(name, f'{valueMl:.2f}L')
            elif value >= 75:
                self.set_template_variable(name, f'{value:.0f}mL')
            elif value >= 15:
                valueTbsp = self.unitConv.conv(
                    value, 'tbsp', 'mL', roundOff=1/8)
                self.set_template_variable(
                    name, f'{valueTbsp} tbsp ({value:.2f}mL)')
            else:
                valueTsp = self.unitConv.conv(
                    value, 'tsp', 'mL', roundOff=1/8)
                self.set_template_variable(
                    name, f'{valueTsp} tsp ({value:.2f}mL)')
        else:
            value = self.unitConv.conv(value, 'g', unit, material, 0.1)
            if value >= 1000:
                valueKg = self.unitConv.conv(value, 'kg')
                self.set_template_variable(name, f'{valueKg:.3f}kg')
            elif value >= 40:
                self.set_template_variable(name, f'{value:.0f}g')
            elif value >= 10:
                valueTbsp = self.unitConv.conv(
                    value, 'tbsp', 'g', material, 1/8)
                self.set_template_variable(
                    name, f'{valueTbsp} tbsp ({value:.1f}g)')
            else:
                if material == 'saffron': print('value =', value)
                valueTsp = self.unitConv.conv(value, 'tsp', 'g', material, 1/8)
                self.set_template_variable(
                    name, f'{valueTsp} tsp ({value:.1f}g)')

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
