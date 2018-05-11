def docprop(x, doc):
    '''
    Nifty function that can add docstrings to attributes
    Curtesy of http://stackoverflow.com/a/15537029
    '''

    def getx(self):
        return getattr(self, '_' + x)

    def setx(self, val):
        setattr(self, '_' + x, val)

    def delx(self):
        delattr(self, '_' + x)

    return property(getx, setx, delx, doc)
