from abc import ABCMeta

class AbstractMeteo:
    __metaclass__ = ABCMeta
    
    def get_query_url(self, comune, day):
        raise NotImplementedError()

    def get_meteo_by_day(self, comune, day):
        raise NotImplementedError()
    
    def get_meteo_week(self, comune, day):
        raise NotImplementedError()