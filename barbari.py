#!/usr/bin/env python3

import recipeutil
from datetime import datetime, timedelta
import math

class RecipeAdjuster(recipeutil.Adjuster):
    def __init__(self):
        recipeutil.Adjuster.__init__(self, 
            'Barbari.template.md',
            'Barbari.input.json',
            'Barbari.out.md')
            
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
        startTime = self.get_input_time('startTime')
        starterHydrationRatio = self.get_input_perc('starterHydrationPercent')
        starterSeedRatio = self.get_input_perc('starterSeedPercent')
        starterStrengthFactorPerHour = self.get_input('starterStrengthFactorPerHour')
        maintainedStarterGrams = self.get_input('maintainedStarterGrams')
        levainHydrationRatio = self.get_input_perc('levainHydrationPercent')
        autolyseDuration = self.get_input_dur('autolyseDuration')
        bulkRiseDuration = self.get_input_dur('estimBulkRiseDuration')
        timeBetweenStretches = self.get_input_dur('timeBetweenStretches')
        levainSeedRatio = self.get_input_perc('levainSeedPercent')
        finalDoughSeedRatio = self.get_input_perc('finalDoughSeedPercent')
        finalDoughHydrationRatio = self.get_input_perc('finalDoughHydrationPercent')
        finalDoughSaltRatio = self.get_input_perc('finalDoughSaltPercent')
        loafWeightGrams = self.get_input('loafWeightGrams')
        flourTypeNumber = self.get_input('flourTypeNumber')
        numberOfLoaves = self.get_input('numberOfLoaves')
        extraDoughGramsPerLoaf = self.get_input('extraDoughGramsPerLoaf')
        ferniGramsPerLoaf = self.get_input('ferniGramsPerLoaf')
        ferniInitHydrationRatio = self.get_input_perc('ferniInitHydrationPercent')
        ferniFinalHydrationRatio = self.get_input_perc('ferniFinalHydrationPercent')
        finalToBulkRiseRatio = self.get_input_perc('finalToBulkRiseRatioPercent')
        preheatDuration = self.get_input_dur('preheatDuration')
        loafBakeDuration = self.get_input_dur('loafBakeDuration')
        bakeMassReductionRatio = self.get_input_perc('bakeMassReductionPercent')
        
        # Compute values to be placed into the recipe template:
        spillageExtraDoughGrams = numberOfLoaves * extraDoughGramsPerLoaf

        doughRoundWeightGrams = loafWeightGrams / bakeMassReductionRatio

        finalDoughGrams = numberOfLoaves * (doughRoundWeightGrams + extraDoughGramsPerLoaf)

        levainMixEndTime = startTime + timedelta(minutes=15)
        maxLevainSeedContent = 5.08

        levainRiseTime = (math.log(maxLevainSeedContent / levainSeedRatio) / starterStrengthFactorPerHour)

        levainRiseTime = round(levainRiseTime * 12) / 12
        levainRiseEndTime = levainMixEndTime + timedelta(hours=levainRiseTime)

        finalDoughCompositionGrams = self.get_dough_composition(
            finalDoughGrams, finalDoughHydrationRatio, finalDoughSeedRatio, levainHydrationRatio, finalDoughSaltRatio)

        (finalDoughFlourGrams, finalDoughLevainGrams, finalDoughSaltGrams,finalDoughWaterGrams) = (
            finalDoughCompositionGrams[x] for x in ('flour', 'levain', 'salt', 'water'))

        initDoughGrams = finalDoughFlourGrams + finalDoughWaterGrams
        
        levainToMixGrams = finalDoughLevainGrams + maintainedStarterGrams

        levainCompositionGrams = self.get_dough_composition(
            levainToMixGrams, levainHydrationRatio, levainSeedRatio,starterHydrationRatio, 0)

        levainMixFlourGrams, levainMixWaterGrams, levainMixStarterGrams = (
            levainCompositionGrams[x] for x in ('flour', 'water', 'levain'))

        starterCompositionGrams = self.get_dough_composition(
            maintainedStarterGrams, starterHydrationRatio, starterSeedRatio,starterHydrationRatio, 0)

        starterMixFlourGrams, starterMixWaterGrams, starterMixStarterGrams = (
            starterCompositionGrams[x] for x in ('flour', 'water', 'levain'))

        initDoughMixStartTime = levainRiseEndTime - autolyseDuration
        initDoughMixEndTime = initDoughMixStartTime + timedelta(minutes=20)
        finalDoughMixEndTime = levainRiseEndTime + timedelta(minutes=30)
        bulkRiseEndTime = finalDoughMixEndTime + bulkRiseDuration

        stretchFoldTimes = [ i * timeBetweenStretches + finalDoughMixEndTime for i in range(1, 4) ]

        bulkRiseVolIncRatio = (flourTypeNumber - 500) / 1000. + 1.25

        totalFerniGrams = ferniGramsPerLoaf * numberOfLoaves
        ferniFlourGrams = totalFerniGrams / (1 + ferniFinalHydrationRatio)
        ferniWaterGrams = ferniFlourGrams * ferniInitHydrationRatio
        ferniEndTime = bulkRiseEndTime
        ferniStartTime = ferniEndTime - timedelta(minutes=30)
        preshapeEndTime = bulkRiseEndTime + timedelta(minutes=30)
        shapeEndTime = preshapeEndTime + timedelta(minutes=30)

        finalRiseVolIncRatio = finalToBulkRiseRatio * (bulkRiseVolIncRatio - 1) + 1
        
        finalRiseDuration = bulkRiseDuration * math.log(finalRiseVolIncRatio) / math.log(bulkRiseVolIncRatio)

        finalRiseDuration = timedelta(seconds=round(finalRiseDuration.seconds / 300) * 300)
        
        finalRiseEndTime = shapeEndTime + finalRiseDuration
        preheatTime = finalRiseEndTime - preheatDuration
        bakeEndTime = finalRiseEndTime + numberOfLoaves * loafBakeDuration

        # Format and set the template variables
        self.set_template_var_time('levainMixStartTime', startTime)
        self.set_template_var_time('levainMixEndTime', levainMixEndTime)
        self.set_template_var_grams('starterFlourAmount', starterMixFlourGrams)
        self.set_template_var_grams('starterWaterAmount', starterMixWaterGrams)
        self.set_template_var_grams('starterStarterAmount', starterMixStarterGrams)
        self.set_template_var_percent('starterSeedPercent', starterSeedRatio)
        self.set_template_var_percent('starterHydrationPercent', starterHydrationRatio)
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
        self.set_template_var_grams('extraDoughAmountPerRound', extraDoughGramsPerLoaf)
        self.set_template_var_grams('doughRoundWeight', doughRoundWeightGrams)
        self.set_template_var_grams('loafWeight', loafWeightGrams)
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
        self.set_template_var_dur('preheatDuration', preheatDuration)
        self.set_template_var_dur('loafBakeDuration', loafBakeDuration)
        self.set_template_var_time('bakeEndTime', bakeEndTime)

adjuster = RecipeAdjuster()
adjuster.generate_recipe()
