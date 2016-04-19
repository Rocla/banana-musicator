__author__ = 'stevevisinand'

class HSBColor:
    def __init__(self, h, s, b):
        """
        :param h: entre 0 et 255
        :param s: entre 0 et 255
        :param b: entre 0 et 255
        :return:
        """
        self._h = h #hue
        self._s = s #saturation
        self._b = b #brightness

    def __repr__(self):
        return "HSB: ("+str(self._h)+","+str(self._s)+","+str(self._b)+")"

    def hue(self):
        """
        :return: hue value : float [0-255[
        """
        return self._h

    def saturation(self):
        """
        :return: saturation value : int [0-255[
        """
        return self._s

    def brightness(self):
        """
        :return: brightness value : int [0-255[
        """
        return self._b

    def _warm(self):
        """
        :return: warm value [0-1] (float)
        """
        # Banana's estimated hot values
        INF_LIMIT = 195
        SUP_LIMIT = 42
        PERFECT_WARM = 0 #255
        MAX_VALUE = 255

        if((self._h<=MAX_VALUE and self._h >= INF_LIMIT) or self._h==PERFECT_WARM):
            work_color = (self._h + (MAX_VALUE-INF_LIMIT)) % 255
            work_hot = PERFECT_WARM + (MAX_VALUE-INF_LIMIT)

            return work_color / work_hot

        if(self._h>PERFECT_WARM and self._h < SUP_LIMIT):
            work_color = self._h
            work_hot = SUP_LIMIT
            return 1.0-(work_color / work_hot)

        return 0

    def _cold(self):
        """
        :return: cold value [(-1)-0] (float)
        """
        # Banana's estimated cold values
        INF_LIMIT = 42
        SUP_LIMIT = 195
        PERFECT_COLD = 180

        if(self._h<=PERFECT_COLD and self._h>=INF_LIMIT):
            work_color = self._h - INF_LIMIT
            work_cold = PERFECT_COLD-INF_LIMIT

            return float(work_color) / float(work_cold)

        if(self._h>PERFECT_COLD and self._h < SUP_LIMIT):
            work_color = self._h - PERFECT_COLD
            work_cold = SUP_LIMIT - PERFECT_COLD

            return 1.0-(float(work_color) / float(work_cold))

        return 0

    def temperature(self):
        """
        :return: temperature estimation [-1.0 - 1.0] (float)
        """

        return self._warm() - self._cold()