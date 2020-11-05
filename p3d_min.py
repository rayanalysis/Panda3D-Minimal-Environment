# Copyright (C) 2020 Logan Bier

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from direct.showbase.ShowBase import ShowBase
from panda3d.core import PerspectiveLens
from panda3d.core import loadPrcFileData
from panda3d.core import PointLight
from panda3d.core import Spotlight
from panda3d.core import AmbientLight
from panda3d.bullet import BulletWorld
from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.LerpInterval import LerpPosHprInterval
import random
import simplepbr
import gltf

class main(ShowBase):
     def __init__(self):
         # load data for self.render first
         loadPrcFileData('', 'framebuffer-srgb')
         # loadPrcFileData('', 'fullscreen #t')
         loadPrcFileData('', 'win-size 1200 700')
         
         # new initialization routine for Panda3D
         # use super().__init__() instead of ShowBase
         # use simplepbr.init() to initialize pbr replacement of setShaderAuto
         # simplepbr works automatically
         # use gltf.patch_loader(self.loader) to use gltf exports from Blender
         super().__init__()
         simplepbr.init()
         gltf.patch_loader(self.loader)
         
         amb_light = AmbientLight('amblight')
         amb_light.setColor((0.2, 0.2, 0.2, 1))
         amb_light_node = self.render.attachNewNode(amb_light)
         self.render.setLight(amb_light_node)
         
         first_model = self.loader.loadModel('untitled.gltf')
         first_model.reparentTo(self.render)
         first_model.setPos(0, 0, 0.5)
         first_model.setScale(1)

         p_light = Spotlight('p_light')
         p_light.setColor((1, 1, 1, 1))
         p_light.setShadowCaster(True, 1028, 1028)
         lens = PerspectiveLens()
         p_light.setLens(lens)
         p_light_node = self.render.attachNewNode(p_light)
         p_light_node.setPos(-5, -5, 5)
         p_light_node.lookAt(first_model)
         self.render.setLight(p_light_node)
         
         # girls = self.loader.loadTexture('image.png')
         # first_model.setTexture(girls)
         
         nice = LerpPosHprInterval(first_model, 5, (4, 4, 3), (180, 90, 180)).loop()
         nice_2 = LerpPosInterval(p_light_node, 2, (7, 7, 7)).loop()
         
         self.cam.setPos(10, 10, 5)
         self.cam.lookAt(first_model)
         
         world = BulletWorld()
         print(world)
         
         def task_1(Task):
             p_light_node.lookAt(first_model)
             
             return Task.cont
         
         self.taskMgr.add(task_1)
         
app = main()
app.run()
