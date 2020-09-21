import datetime
import json
import math
import string

class RecipeAdjust:
    def __init__(self, templateFilePath, inputFilePath, outputFilePath):
        with open(templateFilePath) as templateFile:
            self._template = string.Template(templateFile.read())
        with open(inputFilePath) as inputFile:
            self.inputValues = json.load(inputFile)
        self._outputFilePath = outputFilePath
        self._computedValues = {}
    
    def set_template_variable(self, name, value):
        self._computedValues[name] = value

    def set_template_var_time(self, name, time):
        self._computedValues[name] = time.strftime('%H:%M')

    def set_template_var_grams(self, name, amount):
        self._computedValues[name] = '{:.0f}g'.format(amount)

    def set_template_var_percent(self, name, percent):
        self._computedValues[name] = '{:.0f}%'.format(percent)

    def compute_values(self):
        pass

    def generate_recipe(self):
        self.compute_values()
        recipeText = self._template.substitute(self._computedValues)
        with open(self._outputFilePath, 'w') as outputFile:
            outputFile.write(recipeText)

class BarbariRecipeAdjust(RecipeAdjust):
    def __init__(self):
        RecipeAdjust.__init__(self, 
            'Sourdough-Barbari-Bread.template.md',
            'Sourdough-Barbari-Bread.input.json',
            'Sourdough-Barbari-Bread-autogen.md')
            
    def get_dough_composition(self, totalDough, doughHydrationRatio, seedRatio,
                              levainHydrationRatio, saltRatio):
        levainToFlourRatio = seedRatio * (1 + levainHydrationRatio) / (
            levainHydrationRatio * (1 - seedRatio))
        waterToFlourRatio = (
            doughHydrationRatio * levainHydrationRatio - seedRatio) / (
                levainHydrationRatio * (1 - seedRatio))
        saltToFlourRatio = (
            1 + levainHydrationRatio + levainToFlourRatio) * saltRatio / (
                1 + levainHydrationRatio)
        flourAmount = totalDough / (
            1 + waterToFlourRatio + levainToFlourRatio + saltToFlourRatio)
        waterAmount = waterToFlourRatio * flourAmount
        levainAmount = levainToFlourRatio * flourAmount
        saltAmount = saltToFlourRatio * flourAmount
        return { 'flour' : flourAmount, 'levain' : levainAmount, 
            'salt' : saltAmount, 'water' : waterAmount}

    def compute_values(self):
        startTime = datetime.datetime.strptime(
            self.inputValues['startTime'], '%H:%M')
        starterHydrationRatio = self.inputValues[
            'starterHydrationPercent'] / 100.
        starterStrengthFactorHour = self.inputValues[
            'starterStrengthFactorHour']
        maintainedStarterGrams = self.inputValues['maintainedStarterGrams']
        levainHydrationRatio = self.inputValues['levainHydrationPercent'] / 100.
        levainSeedRatio = self.inputValues['levainSeedPercent'] / 100.
        finalDoughSeedRatio = self.inputValues['finalDoughSeedPercent'] / 100.
        finalDoughHydrationRatio = self.inputValues[
            'finalDoughHydrationPercent'] / 100.
        finalDoughSaltRatio = self.inputValues['finalDoughSaltPercent'] / 100.
        doughRoundWeightGrams = self.inputValues['doughRoundWeightGrams']
        numberOfLoaves = self.inputValues['numberOfLoaves']
        extraDoughGramsPerRound = self.inputValues['extraDoughGramsPerRound']
        
        finalDoughGrams = numberOfLoaves * (
            doughRoundWeightGrams + extraDoughGramsPerRound)
        levainMixEndTime = startTime + datetime.timedelta(minutes=15)

        maxLevainSeedContent = 5.08
        levainRiseTime = math.log(
            maxLevainSeedContent / levainSeedRatio) / starterStrengthFactorHour

        finalDoughCompositionGrams = self.get_dough_composition(
            finalDoughGrams, finalDoughHydrationRatio, finalDoughSeedRatio,
            levainHydrationRatio, finalDoughSaltRatio)

        (finalDoughFlourGrams, finalDoughLevainGrams, finalDoughSaltGrams,
         finalDoughWaterGrams) = (finalDoughCompositionGrams[x] for x in (
            'flour', 'levain', 'salt', 'water'))
        
        levainToMixGrams = finalDoughLevainGrams + maintainedStarterGrams

        levainCompositionGrams = self.get_dough_composition(
            levainToMixGrams, levainHydrationRatio, levainSeedRatio,
            starterHydrationRatio, 0)

        levainMixFlourGrams, levainMixWaterGrams, levainMixStarterGrams = (
            levainCompositionGrams[x] for x in ('flour', 'water', 'levain'))

        self.set_template_var_time('levainMixStartTime', startTime)
        self.set_template_var_time('levainMixEndTime', levainMixEndTime)
        self.set_template_var_grams('levainFlourAmount', levainMixFlourGrams)
        self.set_template_var_grams('levainWaterAmount', levainMixWaterGrams)
        self.set_template_var_grams(
            'levainStarterAmount', levainMixStarterGrams)
        self.set_template_var_grams('levainMixYield', levainToMixGrams)
        self.set_template_var_percent(
            'levainSeedPercent', levainSeedRatio * 100.)
        self.set_template_var_percent(
            'levainHydrationPercent', levainHydrationRatio * 100.)
        self.set_template_var_grams(
            'maintainedStarterAmount', maintainedStarterGrams)
        self.set_template_var_grams(
            'finalDoughFlourAmount', finalDoughFlourGrams)
        self.set_template_var_grams(
            'finalDoughLevainAmount', finalDoughLevainGrams)
        self.set_template_var_grams(
            'finalDoughSaltAmount', finalDoughSaltGrams)
        self.set_template_var_grams(
            'finalDoughWaterAmount', finalDoughWaterGrams)
         
barbari = BarbariRecipeAdjust()
barbari.generate_recipe()
