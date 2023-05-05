#! /usr/bin/env python3
from p5 import *

import os
import re
import math

PATTERN = re.compile(r"^coordinates_(\d+)_(\d+).coo$")

matches = [PATTERN.match(p) for p in os.listdir()]
matches = sorted([(m[0],int(m[1]),int(m[2])) for m in matches if m is not None], key = lambda m: m[2])

grids = dict()
for (path, region, step) in matches:
    if region != 1:
        continue
    with open(path) as f:
        curgrid = None
        subregion = -1
        translation = (0,0)
        while True:
            line = f.readline()
            if line == "":
                break
            cur = line.split(" ")
            if cur[0] == "ID":
                if curgrid is not None:
                    grids[(region, subregion, step)] = curgrid
                subregion = int(cur[1])
                curgrid = []
                t = f.readline().split(" ")
                translation = (int(t[0]), -int(t[1]))
                continue
            curgrid.append((int(cur[0]), -int(cur[1])))
        if curgrid is not None:
            grids[(region, subregion, step)] = curgrid

print(grids.keys())

timeline = [{(r,sr): g for ((r,sr,t2),g) in grids.items() if t2 == t} for t in sorted({t for (_,_,t) in grids.keys()})]
regions = {(r,sr): (random_uniform(255), random_uniform(255), random_uniform(255)) for (r,sr,_) in grids.keys()}

def boundingbox(grids):
    minx, miny =  math.inf,  math.inf
    maxx, maxy = -math.inf, -math.inf
    
    for grid in grids:
        for (x,y) in grid:
            if x < minx:
                minx = x
            if x > maxx:
                maxx = x
            if y < miny:
                miny = y
            if y > maxy:
                maxy = y
    return (minx, miny, maxx, maxy)

region_bounds = [{r: boundingbox([ts[(r,sr)] for (r2,sr) in ts.keys() if r2 == r]) for r in {r for (r,_) in ts.keys()} } for ts in timeline]

bounds = {(r,sr): boundingbox([ts[(r,sr)] for ts in timeline]) for (r,sr) in regions.keys()}

overall_bounds = (min(a for (a,_,_,_) in bounds.values()), min(a for (_,a,_,_) in bounds.values()), max(a for (_,_,a,_) in bounds.values()), max(a for (_,_,_,a) in bounds.values()))
overall_size = (overall_bounds[2]-overall_bounds[0], overall_bounds[3]-overall_bounds[1])

print(region_bounds)
print(overall_size)

def setup():
    size(1280, 900)
    no_stroke()
    background(5)
    
timestep = 0

def draw():
    background(5)
    
    for region in {r for (r,_) in regions.keys()}:
        with push_matrix():
            scale(16)
            
            this_bounds = region_bounds[timestep][region]
            this_size = (this_bounds[2]-this_bounds[0], this_bounds[3]-this_bounds[1])
            this_center = ((this_bounds[2]+this_bounds[0])/2, (this_bounds[3]+this_bounds[1])/2)
            
            translate(-this_center[0], -this_center[1])
            
            translate(640/16,450/16)
            
            no_fill()
            stroke("white")
            stroke_weight(.4)
            rect((this_bounds[0]-2, this_bounds[1]-2), this_size[0]+5, this_size[1]+5)
            
            for ((r,sr),grid) in timeline[timestep].items():
                fill(*regions[(r,sr)])
                for (x,y) in grid:
                    rect((x,y),1,1)
    
    noLoop()

def key_pressed(event):
    global timestep
    global regions
    if event.key == ",":
        timestep = max(0,timestep-1)
        loop()
    if event.key == ".":
        timestep = min(timestep+1,len(timeline)-1)
        loop()
    if event.key == "r":
        regions = {(r,sr): (random_uniform(255), random_uniform(255), random_uniform(255)) for (r,sr,_) in grids.keys()}
        loop()

run(renderer="vispy")
