from abc import ABCMeta
from prev_model import IconConversion

class AbstractModel:
    __metaclass__ = ABCMeta   
    ora = None
    icon = None
    mmlabel = None
    label = None
    precipitazioni = None
    temperatura = None
    temperatura_value = None
    precipitazioni = None
    precipitazioni_value = None

    def setLabel(self, label, ora):
        self.label = label
        self.icon = IconConversion.getIcon(label, ora)
        self.mmlabel = IconConversion.getMMLabel(label)