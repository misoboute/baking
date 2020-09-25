from datetime import datetime, timedelta
import json
import math
import string

def parse_timedelta(input, format):
    return datetime.strptime(input, format) -  datetime(1900, 1, 1, 0, 0, 0)

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
        self._computedValues[name] = '{:.0f}%'.format(percent * 100.)

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
        # Read values from the JSON input file:
        startTime = datetime.strptime(self.inputValues['startTime'], '%H:%M')
        
        starterHydrationRatio = self.inputValues[
            'starterHydrationPercent'] / 100.
        
        starterStrengthFactorHour = self.inputValues[
            'starterStrengthFactorHour']
        
        maintainedStarterGrams = self.inputValues['maintainedStarterGrams']
        levainHydrationRatio = self.inputValues['levainHydrationPercent'] / 100.
        
        autolyseDuration = parse_timedelta(
            self.inputValues['autolyseDuration'], '%H:%M')
        
        bulkRiseDuration = parse_timedelta(
            self.inputValues['estimBulkRiseDuration'], '%H:%M')
        
        timeBetweenStretches = parse_timedelta(
            self.inputValues['timeBetweenStretches'], '%H:%M')
        
        levainSeedRatio = self.inputValues['levainSeedPercent'] / 100.
        finalDoughSeedRatio = self.inputValues['finalDoughSeedPercent'] / 100.

        finalDoughHydrationRatio = self.inputValues[
            'finalDoughHydrationPercent'] / 100.

        finalDoughSaltRatio = self.inputValues['finalDoughSaltPercent'] / 100.
        doughRoundWeightGrams = self.inputValues['doughRoundWeightGrams']
        flourTypeNumber = self.inputValues['flourTypeNumber']
        numberOfLoaves = self.inputValues['numberOfLoaves']
        extraDoughGramsPerRound = self.inputValues['extraDoughGramsPerRound']
        ferniGramsPerLoaf = self.inputValues['ferniGramsPerLoaf']
        
        ferniInitHydrationRatio = self.inputValues[
            'ferniInitHydrationPercent'] / 100.
        
        ferniFinalHydrationRatio = self.inputValues[
            'ferniFinalHydrationPercent'] / 100.
        
        finalToBulkRiseRatio = self.inputValues[
            'finalToBulkRiseRatioPercent'] / 100.
        
        preheatDuration = parse_timedelta(
            self.inputValues['preheatDuration'], '%H:%M')

        loafBakeTime = timedelta(minutes=self.inputValues['loafBakeTimeMins'])
        
        # Compute values to be placed into the recipe template:
        spillageExtraDoughGrams = numberOfLoaves * extraDoughGramsPerRound

        finalDoughGrams = numberOfLoaves * (
            doughRoundWeightGrams + extraDoughGramsPerRound)

        levainMixEndTime = startTime + timedelta(minutes=15)
        maxLevainSeedContent = 5.08

        levainRiseTime = math.log(
            maxLevainSeedContent / levainSeedRatio) / starterStrengthFactorHour

        levainRiseTime = round(levainRiseTime * 12) / 12
        levainRiseEndTime = levainMixEndTime + timedelta(hours=levainRiseTime)

        finalDoughCompositionGrams = self.get_dough_composition(
            finalDoughGrams, finalDoughHydrationRatio, finalDoughSeedRatio,
            levainHydrationRatio, finalDoughSaltRatio)

        (finalDoughFlourGrams, finalDoughLevainGrams, finalDoughSaltGrams,
         finalDoughWaterGrams) = (finalDoughCompositionGrams[x] for x in (
            'flour', 'levain', 'salt', 'water'))

        initDoughGrams = finalDoughFlourGrams + finalDoughWaterGrams
        
        levainToMixGrams = finalDoughLevainGrams + maintainedStarterGrams

        levainCompositionGrams = self.get_dough_composition(
            levainToMixGrams, levainHydrationRatio, levainSeedRatio,
            starterHydrationRatio, 0)

        levainMixFlourGrams, levainMixWaterGrams, levainMixStarterGrams = (
            levainCompositionGrams[x] for x in ('flour', 'water', 'levain'))

        initDoughMixStartTime = levainRiseEndTime - autolyseDuration
        initDoughMixEndTime = initDoughMixStartTime + timedelta(minutes=20)
        finalDoughMixEndTime = levainRiseEndTime + timedelta(minutes=30)
        bulkRiseEndTime = finalDoughMixEndTime + bulkRiseDuration

        stretchFoldTimes = [ i * timeBetweenStretches + finalDoughMixEndTime 
            for i in range(1, 4)]

        bulkRiseVolIncRatio = (flourTypeNumber - 500) / 1000. + 1.25

        totalFerniGrams = ferniGramsPerLoaf * numberOfLoaves
        ferniFlourGrams = totalFerniGrams / (1 + ferniFinalHydrationRatio)
        ferniWaterGrams = ferniFlourGrams * ferniInitHydrationRatio
        ferniEndTime = bulkRiseEndTime
        ferniStartTime = ferniEndTime - timedelta(minutes=30)
        preshapeEndTime = bulkRiseEndTime + timedelta(minutes=30)
        shapeEndTime = preshapeEndTime + timedelta(minutes=30)

        finalRiseVolIncRatio = finalToBulkRiseRatio * (
            bulkRiseVolIncRatio - 1) + 1
        
        finalRiseDuration = bulkRiseDuration * math.log(
            finalRiseVolIncRatio) / math.log(bulkRiseVolIncRatio)

        finalRiseDuration = timedelta(
            seconds=round(finalRiseDuration.seconds / 300) * 300)
        
        finalRiseEndTime = shapeEndTime + finalRiseDuration
        preheatTime = finalRiseEndTime - preheatDuration
        bakeEndTime = finalRiseEndTime + numberOfLoaves * loafBakeTime

        # Format and set the template variables
        self.set_template_var_time('levainMixStartTime', startTime)
        self.set_template_var_time('levainMixEndTime', levainMixEndTime)
        self.set_template_var_grams('levainFlourAmount', levainMixFlourGrams)
        self.set_template_var_grams('levainWaterAmount', levainMixWaterGrams)
        self.set_template_var_grams('levainStarterAmount', levainMixStarterGrams)
        self.set_template_var_grams('levainMixYield', levainToMixGrams)
        self.set_template_var_percent('levainSeedPercent', levainSeedRatio)
        self.set_template_var_percent('levainHydrationPercent', levainHydrationRatio)
        self.set_template_var_grams('maintainedStarterAmount', maintainedStarterGrams)
        self.set_template_var_time('levainRiseEndTime', levainRiseEndTime)
        self.set_template_var_time('initDoughMixStartTime', initDoughMixStartTime)
        self.set_template_var_time('initDoughMixEndTime', initDoughMixEndTime)
        self.set_template_var_time('finalDoughMixEndTime', finalDoughMixEndTime)
        self.set_template_var_grams('finalDoughFlourAmount', finalDoughFlourGrams)
        self.set_template_var_grams('finalDoughLevainAmount', finalDoughLevainGrams)
        self.set_template_var_grams('finalDoughSaltAmount', finalDoughSaltGrams)
        self.set_template_var_grams('finalDoughWaterAmount', finalDoughWaterGrams)
        self.set_template_var_grams('initDoughAmount', initDoughGrams)
        self.set_template_var_grams('finalDoughAmount', finalDoughGrams)
        self.set_template_var_percent('finalDoughHydrationPercent', finalDoughHydrationRatio)
        self.set_template_var_percent('finalDoughSeedPercent', finalDoughSeedRatio)
        self.set_template_var_grams('spillageExtraDoughAmount', spillageExtraDoughGrams)
        self.set_template_var_grams('extraDoughAmountPerRound', extraDoughGramsPerRound)
        self.set_template_var_grams('doughRoundWeight', doughRoundWeightGrams)
        self.set_template_variable('numberOfLoaves', numberOfLoaves)
        self.set_template_var_time('finalDoughMixEndTime', finalDoughMixEndTime)
        self.set_template_var_time('stretchFold1Time', stretchFoldTimes[0])
        self.set_template_var_time('stretchFold2Time', stretchFoldTimes[1])
        self.set_template_var_time('stretchFold3Time', stretchFoldTimes[2])
        self.set_template_var_time('bulkRiseEndTime', bulkRiseEndTime)
        self.set_template_var_percent('bulkRiseVolIncPercent', bulkRiseVolIncRatio)
        self.set_template_var_grams('ferniAmountPerLoaf', ferniGramsPerLoaf)
        self.set_template_var_percent('ferniInitHydrationPercent', ferniInitHydrationRatio)
        self.set_template_var_time('ferniStartTime', ferniStartTime)
        self.set_template_var_time('ferniEndTime', ferniEndTime)
        self.set_template_var_grams('ferniFlourAmount', ferniFlourGrams)
        self.set_template_var_grams('ferniWaterAmount', ferniWaterGrams)
        self.set_template_var_grams('ferniYieldAmount', totalFerniGrams)
        self.set_template_var_time('preshapeEndTime', preshapeEndTime)
        self.set_template_var_time('shapeEndTime', shapeEndTime)
        self.set_template_var_time('finalRiseEndTime', finalRiseEndTime)
        self.set_template_var_percent('finalRiseVolIncPercent', finalRiseVolIncRatio)
        self.set_template_var_time('preheatTime', preheatTime)
        self.set_template_var_time('preheatDuration', datetime(1900, 1, 1) + preheatDuration)
        self.set_template_var_time('loafBakeTime', datetime(1900, 1, 1) + loafBakeTime)
        self.set_template_var_time('bakeEndTime', bakeEndTime)

barbari = BarbariRecipeAdjust()
barbari.generate_recipe()
