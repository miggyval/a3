import math


class ColorHandler:
    # @staticmethod
    # def hex2hsv(hex_in):
    #     r_in, g_in, b_in = ColorHandler.hex2rgb(hex_in)
    #     min_max = sorted([r_in/255, g_in/255, b_in/255]).pop(1)
    #     if (r_in == b_in == c_in):
    #         s_out = 0
    #         h_out = 0
    #     else:
    #     min_val = min_max[0]
    #     max_val = min_max[1]
    #     v_out = (min_val + max_val) / 2
    #     if v_out < 0.5:
    #         s_out = (max_val - min_val) / (max_val + min_val)
    #     else:
    #         s_out = (max_val - min_val) / (2.0 - (max_val + min_val))
    #     hsv_out = (floor(h_out*255), floor(s_out*255), floor(v_out*255))
    #     return hsv_out
    #
    # @staticmethod
    # def adjust_saturation(hex_in, saturation):
    #     h_in, s_in, v_in = hex2hsv(hex_in)
    #     s_in = saturation
    @staticmethod
    def mix_colors(hex1, hex2, mix=0.5):
        r1, g1, b1 = ColorHandler.hex2rgb(hex1)
        r2, g2, b2 = ColorHandler.hex2rgb(hex2)
        r3 = math.floor(math.sqrt((mix * (r1 ** 2) + (1 - mix) * (r2 ** 2))))
        g3 = math.floor(math.sqrt((mix * (g1 ** 2) + (1 - mix) * (g2 ** 2))))
        b3 = math.floor(math.sqrt((mix * (b1 ** 2) + (1 - mix) * (b2 ** 2))))
        hex3 = ColorHandler.rgb2hex(r3, g3, b3)
        return hex3

    @staticmethod
    def rgb2hex(r,g,b):
        hex = "#{:02x}{:02x}{:02x}".format(r, g, b)
        return hex

    @staticmethod
    def hex2rgb(hexcode):
        rgb = (int(hexcode[1:3], 16), int(hexcode[3:5], 16), int(hexcode[5:7], 16))
        return rgb
