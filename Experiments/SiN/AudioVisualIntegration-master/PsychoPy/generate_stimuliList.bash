#!/bin/bash

CALLSIGN_COL=3
COLOR_COL=4
NUMBER_COL=5
CONDITION_COL=6
VIDEO_COL=7
SPEAKER_COL=2

echo "videoFile,group,speaker,condition,video,callSign,colour,number" > stimuliList.csv

while read line
do
  callSign="$(echo "$line" | awk -F'_' '{print $'"$CALLSIGN_COL"'}')"
  color="$(echo "$line" | awk -F'_' '{print $'"$COLOR_COL"'}')"
  number="$(echo "$line" | awk -F'_' '{print $'"$NUMBER_COL"'}')" 
  speaker="$(echo "$line" | awk -F'_' '{print $'"$SPEAKER_COL"'}')"
  condition="$(echo "$line" | awk -F'_' '{print $'"$CONDITION_COL"'}')"
  video="$(echo "$line" | awk -F'_' '{print $'"$VIDEO_COL"'}' | sed -e 's/\..*//g')"
  case "$callSign" in
    "Ti") callSign="tiger" ;;
    "Dr") callSign="drossel" ;;
    "Ad") callSign="adler" ;;
    "Un") callSign="unke" ;;
  esac
  case "$color" in
    "We") color="weiss" ;;
    "Ro") color="rot" ;;
    "Ge") color="gelb" ;;
    "Gr") color="gruen" ;;
  esac
  case "$condition" in
    "NoThetaInAudio") condition="noTheta" ;;
    "NVocInAudio") condition="vocoded" ;;
    "GlobalTheta") condition="globalTheta" ;;
  esac
  case "$video" in
    "NoVideo") video="noVideo" ;;
    "GlobalThetaInVideo") video="plusVideo" ;;
  esac
  group="${condition}_${video}"
  echo "${line},${group},${speaker},${condition},${video},${callSign},${color},${number}" >> stimuliList.csv
done < <(find video/Experiment -name "*.mkv")
