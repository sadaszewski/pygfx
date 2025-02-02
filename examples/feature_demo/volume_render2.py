"""
Volume Rendering 2
==================

Render three volumes using different world transforms.
"""
# sphinx_gallery_pygfx_render = True

import imageio.v3 as iio
import numpy as np
from wgpu.gui.auto import WgpuCanvas, run
import pygfx as gfx


canvas = WgpuCanvas()
renderer = gfx.renderers.WgpuRenderer(canvas)
scene = gfx.Scene()

voldata = iio.imread("imageio:stent.npz").astype(np.float32)

geometry = gfx.Geometry(grid=voldata)
material = gfx.VolumeRayMaterial(clim=(0, 2000))

vol1 = gfx.Volume(geometry, material)
vol2 = gfx.Volume(geometry, material)
vol3 = gfx.Volume(geometry, material)
scene.add(vol1, vol2, vol3)

vol2.position.x = -150
vol2.scale.z = 0.5

vol3.position.x = 150

camera = gfx.PerspectiveCamera(70, 16 / 9)
camera.position.y = 500
controller = gfx.OrbitController(
    camera.position.clone(), up=gfx.linalg.Vector3(0, 0, 1)
)
controller.rotate(-0.5, -0.5)
controller.add_default_event_handlers(renderer, camera)

# A clipping plane at z=0 - only the rotating volume will be affected
material.clipping_planes = [(0, 0, 1, 0)]


def animate():
    controller.update_camera(camera)
    rot = gfx.linalg.Quaternion().set_from_euler(gfx.linalg.Euler(0.005, 0.01))
    vol3.rotation.multiply(rot)

    renderer.render(scene, camera)
    canvas.request_draw()


if __name__ == "__main__":
    canvas.request_draw(animate)
    run()
