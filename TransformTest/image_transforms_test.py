from torchvision.transforms import v2
from PIL import Image
from paths import TRANSFORM_IMAGE_EXAMPLE

orig_img = Image.open(TRANSFORM_IMAGE_EXAMPLE)

brightness = 0.2  # 0 <= brightness <= 1
saturation = 0.1  # 0 <= saturation <= 1
contrast = 0.1  # 0 <= contrast <= 1
hue = 0.15  # <=0.5

brightness_low = v2.ColorJitter(brightness=(1 - brightness, 1 - brightness))(orig_img)
brightness_high = v2.ColorJitter(brightness=(1 + brightness, 1 + brightness))(orig_img)

saturation_low = v2.ColorJitter(saturation=(1 - saturation, 1 - saturation))(orig_img)
saturation_high = v2.ColorJitter(saturation=(1 + saturation, 1 + saturation))(orig_img)

contrast_low = v2.ColorJitter(contrast=(1 + contrast, 1 + contrast))(orig_img)
contrast_high = v2.ColorJitter(contrast=(1 - contrast, 1 - contrast))(orig_img)

hue_low = v2.ColorJitter(hue=(-hue, -hue))(orig_img)
hue_high = v2.ColorJitter(hue=(hue, hue))(orig_img)

combo_low = v2.ColorJitter(brightness=(1 - brightness, 1 - brightness),
                           saturation=(1 - saturation, 1 - saturation),
                           contrast=(1 - contrast, 1 - contrast),
                           hue=(-hue, -hue))(orig_img)

combo_high = v2.ColorJitter(brightness=(1 + brightness, 1 + brightness),
                            saturation=(1 + saturation, 1 + saturation),
                            contrast=(1 + contrast, 1 + contrast),
                            hue=(hue, hue))(orig_img)

# Display the original and transformed images
#orig_img.show(title="Original")
#brightness_low.show(title="Brightness Low")
#brightness_high.show(title="Brightness High")
#saturation_low.show(title="Saturation Low")
#saturation_high.show(title="Saturation High")
#contrast_low.show(title="Contrast Low")
#contrast_high.show(title="Contrast High")
#hue_low.show(title="Hue Low")
#hue_high.show(title="Hue High")
combo_low.show(title="combo low")
combo_high.show(title="combo high")
