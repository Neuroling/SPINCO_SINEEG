---
  title: "tst"
author: "G.Fraga Gonzalez"
date: "`r Sys.Date()`"
output:
  html_document:
 
---
 
 
```{nomnoml , echo = FALSE, out.height=400,out.width=850}
# From  https://nomnoml.com/
#arrowSize: 1
#bendSize: 0.3
#direction:  right 
#gutter: 15
#edgeMargin: 0
#gravity: 1
#edges: hard | rounded
#background: transparent
#fill: #eee8d5; #fdf6e3
#fillArrows: false
#font: Calibri
#fontSize: 12
#leading: 1.25
#lineWidth: 1.5
#padding: 8
#spacing: 45
#stroke: #33322E
#title: filename
#zoom: 1
#acyclicer: greedy
#ranker: network-simplex | tight-tree | longest-path
#.box: fill=#8f8 dashed
#.blob: visual=ellipse title=bold

[<usecase>raw | versions] ->  [<table> Separate files (prorrec) | words | pseudowords]
[<table> Separate files (prorrec)] -->  [<state>inspect | +trim]

[inspect ] --> [<actor>audiocheck|plots]

[<actor>audiocheck] --> if OK  [<abstract>Audacity macro | trunc silence | fade ends | add silence | normalize loudness]
[<abstract>Audacity macro] --> [Experiment]
[<abstract>Experiment]  -->  [<state>clear]
[<abstract>Experiment] --> [<state>in SSN]
[<abstract>Experiment] --> [<state>vocoder]
[<state>vocoder] -- Lvls[<start>st.]
[<state>in SSN] -- SNRs[<start>st]
[<actor>audiocheck] <--> not OK?[<abstract>audioLabeler app | or discard]

```
 