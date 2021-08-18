import json

filter_words = [
    "each image", "both images", "at least", "at most", "all of the animals",
    "every of the animals", "all of the objects", "each of the objects"]

number_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                "an", "a"]
good_words = ["left image", "right image", "lefthand image", 
              "righthand image", "image on the right", 
              "image on the left", "every photo", "leftmost", "rightmost",
              "image to the left", "on the right", "on the left",
              "left photo", "right photo", "left pic", "right pic",
              "an image", "one of the images", "one image"]
advs = ["exactly", "only", "strictly"]
singlar_number_words = ["a", "an", "one"]

def check_filter_words(sent:str) -> bool:
    for i in filter_words:
        if i in sent:
            return True
    return False

def check_good_words(sent:str) -> bool:
    for i in good_words:
        if i in sent:
            return True
    return False
    
def check_there_be(sent:str) -> bool:
    if len(sent.split()) < 4:
        return False
    if sent.startswith("there are"):
        if sent.split()[2] in advs and sent.split()[3] in number_words:
            return True
        elif sent.split()[2] in number_words:
            return True
        else:
            return False
    elif sent.startswith("there is"):
        if sent.split()[2] in singlar_number_words:
            return True
        else:
            return False
    else:
        return False

def check_number_start(sent:str) -> bool:
    if len(sent.split()) < 2:
        return False
    if sent.split()[0] in advs and sent.split()[1] in number_words:
        return True
    elif sent.split()[1] in number_words:
        return True
    else:
        return False

file = open("train.json", "r")
outfile = open("train_out.json", "w")
outtsv = open("out.tsv", "w")

for line in file:
    datum = json.loads(line)
    sent = datum["sentence"].lower()
    if datum["label"] == "False":
        continue
    if check_filter_words(sent):
        if not ("left image" in sent and "right image" in sent):
            continue
    if not (check_good_words(sent) or check_there_be(sent) or check_number_start(sent)):
        continue
    outfile.write(line)
    outtsv.write(f"{datum['identifier']}\t{datum['sentence']}\t{datum['left_url']}\t{datum['right_url']}\t{datum['label']}\n")
