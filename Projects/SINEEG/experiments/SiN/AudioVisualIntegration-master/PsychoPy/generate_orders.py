#!/usr/bin/env python3

import itertools
import random
import os

 prefix = "video/Experiment/"

halves = [
    [
        [2,3,5,1,4], # 1st half of 1st order
        [3,5,1,4,2], # 1st half of 2nd order
        [5,1,4,2,3], # ...
        [1,4,2,3,5],
        [4,2,3,5,1]
    ],[
        [1,4,5,3,2], # 2nd half of 1st order
        [3,2,1,4,5], # 2st half of 2nd order
        [5,3,2,1,4], # ...
        [2,1,4,5,3],
        [4,5,3,2,1]
    ]
]

properties = [
    ["Ad","Dr","Ti","Un"],
    ["Ge","Gr","Ro","We"],
    ["1","2","3","4"]
]

conditions = [
    "NVocInAudio_GlobalThetaInVideo",
    "NVocInAudio_NoVideo",
    "NoThetaInAudio_GlobalThetaInVideo",
    "NoThetaInAudio_NoVideo",
    "GlobalTheta_NoVideo",
]

labels = {
  "NVocInAudio": "vocoded",
  "NoVideo": "noVideo",
  "NoThetaInAudio": "noTheta",
  "GlobalThetaInVideo": "plusVideo",
  "GlobalTheta": "globalTheta",
}

speakers = [
    "sp01",
    "sp07"
]

half_ids = ["A", "B"]

# 64 combinations of all three properties
combinations = list(itertools.product(*properties))
print(combinations)

# 2 times 32 combinations where number and color are balanced, but the first has only Ad/Dr, second only Ti/Un
parts = [combinations[0:32], combinations[32:64]]


# 8 random indices out of 16. These 8 indices will be switched between the first/second and third/fourth quarters
to_switch = sorted(random.sample(range(16), 8))
for n in to_switch:
    s = parts[0][n]
    parts[0][n] = parts[0][n+16]
    parts[0][n+16] = s
    s = parts[1][n]
    parts[1][n] = parts[1][n+16]
    parts[1][n+16] = s

# 16 random indices out of 32. These 16 indices will be switched between the two halves
to_switch = sorted(random.sample(range(32), 16))
for n in to_switch:
    s = parts[0][n]
    parts[0][n] = parts[1][n]
    parts[1][n] = s

print("Generating orders:")

all_stimuli = {}
for condition in conditions:
    all_stimuli[condition] = [[],[]]
    for p, part in enumerate(parts):
        randomSpeakers = speakers * 16
        random.shuffle(randomSpeakers)

        for i, combination in enumerate(part):
            speaker = randomSpeakers[i]
            all_stimuli[condition][p].append([speaker] + list(combination))

for condition, stimuli in all_stimuli.items():
    for part in stimuli:
        # check if each unique parameter appears exactly 32 times in each set of combinations
        for prop_kind in range(3):
            for prop in properties[prop_kind]:
                matching = [x for x in part if x[prop_kind+1] is prop]
                print(matching)
                assert(len(matching) == 8)
        # check if each unique speaker appears exactly 16 times in each set of combinations
        for speaker in speakers:
            matching = [x for x in part if x[0] is speaker]
            assert(len(matching) == 16)

os.makedirs("flow/orders", exist_ok=True)
os.makedirs("flow/blocks", exist_ok=True)

for h, half in enumerate(halves):
    print("Blocks %s" % half_ids[h])
    for oi, order in enumerate(half):
        print(order)
        with open("flow/orders/order%d%s.csv" % (oi+1, half_ids[h]), "w") as output:
            output.write("seq,id,block\n")
            for seq, o in enumerate(order):
                half_id = half_ids[seq % 2] if h == 0 else half_ids[1 - seq % 2]
                output.write("%d,%d,flow/blocks/%s_%s.csv\n" % (seq, o, conditions[o-1], half_id))


for label, stimuli in all_stimuli.items():
    for half, part in enumerate(stimuli):
        with open("flow/blocks/%s_%s.csv" % (label, half_ids[half]), "w") as output:
            output.write("videoFile,condition,video,speaker,callSign,colour,number\n")
            for stimulus in part:
                conditionParameters = label.split("_")[0:2]
                conditionLabels = [labels[c] for c in conditionParameters]
                path = "%szh_%s_%s_%s_%s_%s.avi,%s,%s,%s,%s,%s,%s" % (prefix, *stimulus, "_".join(conditionParameters), *conditionLabels, *stimulus)
                output.write("%s\n" % path)

