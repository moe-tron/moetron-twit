import random
import hashlib
import os

class Generate_util():

    def __init__(self, generator, delete_images = False):
        self.generator = generator
        self.generator.generate_one_image(1)
        self.delete_images = delete_images

    #----------------------------------------------------------------------------

    def parse_msg(self, text):
        # Get rid of mention
        text.replace("@Moetron ","")
        text.replace("@Moetron", "")

        # currently only supporting rand, mess, and name
        if "moerand" in text:
            return self.rand()
        elif "moemess" in text:
            return self.mess()
        else:
            return self.name(text)

    def rand(self):
        seed = random.randint(0, 4294967295)
        img_path = self.generator.generate_one_image(seed)
        return img_path

    def mess(self):
        seed = random.randint(0, 4294967295)
        img_path = self.generator.generate_one_image(seed, truncation_psi=1, op="mess")
        return img_path

    def name(self, input_string):
        seed = self.convertToSeed(input_string)
        img_path = self.generator.generate_one_image(seed)
        return img_path

    ## Helper Methods
    def convertToSeed(self, arg:str):
        return int.from_bytes(hashlib.md5(arg.encode('utf-8')).digest(), byteorder='big', signed=False) % 1000000000 if not arg.isdigit() else int(arg)
