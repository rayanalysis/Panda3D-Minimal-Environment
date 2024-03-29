# Copyright (C) 2020 Logan Bier. All rights reserved.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
'''
Copyright (c) 2008, Carnegie Mellon University.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. Neither the name of Carnegie Mellon University nor the names of
   other contributors may be used to endorse or promote products
   derived from this software without specific prior written
   permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHORS "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

(This is the Modified BSD License.  See also
http://www.opensource.org/licenses/bsd-license.php )
'''
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
        loadPrcFileData('', 'framebuffer-srgb #t')
        # loadPrcFileData('', 'fullscreen #t')
        loadPrcFileData('', 'win-size 1680 1050')
         
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
        p_light.setShadowCaster(True, 1024, 1024)
        lens = PerspectiveLens()
        p_light.setLens(lens)
        p_light_node = self.render.attachNewNode(p_light)
        p_light_node.setPos(-5, -5, 5)
        p_light_node.lookAt(first_model)
        self.render.setLight(p_light_node)
      
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
