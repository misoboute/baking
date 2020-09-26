import recipeutil
from datetime import datetime, timedelta
import math

class RecipeAdjuster(recipeutil.Adjuster):
    def __init__(self):
        recipeutil.Adjuster.__init__(self, 
            'Sourdough-Doughnut.template.md',
            'Sourdough-Doughnut.input.json',
            'Sourdough-Doughnut.out.md')
            
    def compute_values(self):
        # Read values from the JSON input file:
        numberOfDoughnuts = self.get_input('numberOfDoughnuts')
        doughnutWeightGrams = self.get_input('doughnutWeightGrams')
        levainHydrationRatio = self.get_input_perc('levainHydrationPercent')
        doughHydrationRatio = self.get_input_perc('doughHydrationPercent')
        doughSeedRatio = self.get_input_perc('doughSeedPercent')
        sugarToFlourRatio = self.get_input_perc('sugarToFlourPercent')
        saltToFlourRatio = self.get_input_perc('saltToFlourPercent')
        butterToFlourRatio = self.get_input_perc('butterToFlourPercent')
        eggToFlourRatio = self.get_input_perc('eggToFlourPercent')
        butterWaterContentRatio = self.get_input_perc('butterWaterContentPercent')
        milkWaterContentRatio = self.get_input_perc('milkWaterContentPercent')
        eggWaterContentRatio = self.get_input_perc('eggWaterContentPercent')
        eggWeightGrams = self.get_input('eggWeightGrams')

        # Compute the values:
        totalDoughGrams = numberOfDoughnuts * doughnutWeightGrams
        T = totalDoughGrams
        sd = doughSeedRatio
        h = levainHydrationRatio
        wb = butterWaterContentRatio
        rb = butterToFlourRatio
        we = eggWaterContentRatio
        re = eggToFlourRatio
        H = doughHydrationRatio
        wm = milkWaterContentRatio
        rs = sugarToFlourRatio
        rst = saltToFlourRatio

        F = T / (sd * (1 + h) + (H - h * sd - wb * rb - we * re) / wm + 
                 rs + rst + re + rb + (1 - sd))
        print("F", F)
        levainGrams = sd * (1 + h) * F
        milkGrams = (H - h * sd - wb * rb - we * re) * F / wm
        saltGrams = rst * F
        sugarGrams = rs * F
        butterGrams = rb * F
        eggGrams = re * F
        numberOfEggs = round(eggGrams / eggWeightGrams, 1)
        flourGrams = (1 - sd) * F

        # Format and set the template variables
        self.set_template_variable('numberOfDoughnuts', numberOfDoughnuts)
        self.set_template_var_grams('doughnutWeightAmount', doughnutWeightGrams)
        self.set_template_var_percent('levainHydration', levainHydrationRatio)
        self.set_template_var_grams('levainAmount', levainGrams)
        self.set_template_var_grams('milkAmount', milkGrams)
        self.set_template_var_grams('sugarAmount', sugarGrams)
        self.set_template_var_grams('saltAmount', saltGrams)
        self.set_template_variable('numberOfEggs', numberOfEggs)
        self.set_template_var_grams('butterAmount', butterGrams)
        self.set_template_var_grams('flourAmount', flourGrams)

adjuster = RecipeAdjuster()
adjuster.generate_recipe()
