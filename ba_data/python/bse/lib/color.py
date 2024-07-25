""" Module containing nifty color groups and functions. """
import colorsys

sok_color   = (0.10, 0.85, 0.45)
sok_color2  = (0.10, 0.60, 0.30)
sok_color3  = (0.90, 0.80, 0.25)

def hsv(
        color:tuple,
        mode:str = 'set',
        hue = None,
        saturation = None,
        value = None
        ) -> tuple:
    ''' Interprets a color in a HSV format and let's the user change it's values.
        returns a normal color once done. '''

    if not mode in ['set','add']:
        raise Exception(f'unknown mode: "{mode}". (must be "set" or "add".)')
    if not len(color) > 2 and not len(color) < 5:
        raise Exception(f'color tuple isn\'t a color: "{color}".')

    color = list(color); opacity = None

    # Vault opacity, we don't really want to mess with that
    if len(color) == 4:
        opacity = color[3]
        color.pop(3)

    h,s,v = colorsys.rgb_to_hsv(*color)

    # Check the values we have and use them
    # Hue
    if hue:
        nh = hue if mode == 'set' else h+hue
        h = max(0, min(1, nh))
    # Saturation
    if saturation:
        ns = saturation if mode == 'set' else s+saturation
        s = max(0, min(1, ns))
    # Value
    if value:
        nv = value if mode == 'set' else v+value
        v = max(0, min(1, nv))
    
    # Return our colors to rgb and round them before packing out (they can get pretty wild sometimes)
    r,g,b = colorsys.hsv_to_rgb(h,s,v)

    outlist = [r,g,b]
    if opacity: outlist.append(opacity)
    
    out = (round(x,3) for x in outlist)

    return tuple(out)

def resaturate(r:float,g:float,b:float, strength:float = 0.6) -> tuple[float, float, float]:
    """ Changes the saturation of a given color. """
    return strength * r, strength * g, strength * b