def docprop(x, doc):
    def getx(self):
        return getattr(self, '_' + x)

    def setx(self, val):
        setattr(self, '_' + x, val)

    def delx(self):
        delattr(self, '_' + x)

    return property(getx, setx, delx, doc)
