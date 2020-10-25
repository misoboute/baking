import recipeutil
from datetime import datetime, timedelta
import math

class RecipeAdjuster(recipeutil.Adjuster):
    def __init__(self):
        recipeutil.Adjuster.__init__(self,
            'Ferni.template.md',
            'Ferni.input.json',
            'Ferni.out.md')

    def compute_values(self):
        # Read values from the JSON input file:
        numberOfServings = self.get_input('numberOfServings')
        servingSizeGrams = self.get_input('servingSizeGrams')
        yieldRatio = self.get_input_perc('yieldRatioPercent')
        cinnamonRatio = self.get_input_perc('cinnamonToFlourPercent')
        milkRatio = self.get_input_perc('milkToFlourPercent')
        waterRatio = self.get_input_perc('waterToFlourPercent')
        sugarRatio = self.get_input_perc('sugarToFlourPercent')
        roseWaterRatio = self.get_input_perc('roseWaterToFlourPercent')
        butterRatio = self.get_input_perc('butterToFlourPercent')
        saffronRatio = self.get_input_perc('saffronToFlourPercent')
        nutsRatio = self.get_input_perc('nutsToFlourPercent')

        # Compute the values:
        yieldGrams = servingSizeGrams * numberOfServings
        totalGrams = yieldGrams / yieldRatio
        flourGrams = totalGrams / (
            1 + milkRatio + waterRatio + sugarRatio + roseWaterRatio +
            butterRatio + saffronRatio + nutsRatio)

        (milkGrams, waterGrams, sugarGrams, roseWaterGrams, butterGrams,
         cinnamonGrams, saffronGrams, nutsGrams) = (
             r * flourGrams for r in (
                milkRatio, waterRatio, sugarRatio, roseWaterRatio,
                butterRatio, cinnamonRatio, saffronRatio, nutsRatio))

        # Format and set the template variables
        self.set_template_variable('numberOfServings', numberOfServings)
        self.fmt_templ_var_amount('yieldAmount', yieldGrams)
        self.fmt_templ_var_amount('flourAmount', flourGrams)
        self.fmt_templ_var_amount('cinnamonAmount', cinnamonGrams, 'g', 'cinnamon')
        self.fmt_templ_var_amount('milkAmount', milkGrams)
        self.fmt_templ_var_amount('waterAmount', waterGrams)
        self.fmt_templ_var_amount('sugarAmount', sugarGrams)
        self.fmt_templ_var_amount('roseWaterAmount', roseWaterGrams, 'g', 'rosewater')
        self.fmt_templ_var_amount('butterAmount', butterGrams)
        self.fmt_templ_var_amount('saffronAmount', saffronGrams, 'g', 'saffron')
        self.fmt_templ_var_amount('nutsAmount', nutsGrams, 'g', 'crushedNuts')

adjuster = RecipeAdjuster()
adjuster.generate_recipe()
