function relativeLuminance(RGB) {
    // https://gist.github.com/jfsiii/5641126
    // from http://www.w3.org/TR/WCAG20/#relativeluminancedef

    RGB = RGB.replace(/#/, '');
    var R8bit = parseInt(RGB.substring(0, 2), 16);
    var G8bit = parseInt(RGB.substring(2, 4), 16);
    var B8bit = parseInt(RGB.substring(4, 6), 16);

    var RsRGB = R8bit / 255;
    var GsRGB = G8bit / 255;
    var BsRGB = B8bit / 255;

    var R = (RsRGB <= 0.03928) ? RsRGB / 12.92 : Math.pow((RsRGB + 0.055) / 1.055, 2.4);
    var G = (GsRGB <= 0.03928) ? GsRGB / 12.92 : Math.pow((GsRGB + 0.055) / 1.055, 2.4);
    var B = (BsRGB <= 0.03928) ? BsRGB / 12.92 : Math.pow((BsRGB + 0.055) / 1.055, 2.4);

    // For the sRGB colorspace, the relative luminance of a color is defined as:
    var L = 0.2126 * R + 0.7152 * G + 0.0722 * B;

    return L;
}
