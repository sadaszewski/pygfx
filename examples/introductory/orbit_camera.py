"""
Orbit Camera
============

Example showing orbit camera controller.

Press 's' to save the state, and
press 'l' to load the last saved state.
"""
# sphinx_gallery_pygfx_render = True

import imageio.v3 as iio
from wgpu.gui.auto import WgpuCanvas, run
import pygfx as gfx
import numpy as np


canvas = WgpuCanvas()
renderer = gfx.renderers.WgpuRenderer(canvas)
scene = gfx.Scene()

scene.add(gfx.AxesHelper(size=250))

im = iio.imread("imageio:chelsea.png")
tex = gfx.Texture(im, dim=2).get_view(filter="linear")

material = gfx.MeshBasicMaterial(map=tex, side="front")
geometry = gfx.box_geometry(100, 100, 100)
cubes = [gfx.Mesh(geometry, material) for i in range(8)]
for i, cube in enumerate(cubes):
    cube.position.set(350 - i * 100, 150, 0)
    scene.add(cube)

dark_gray = np.array((169, 167, 168, 255)) / 255
light_gray = np.array((100, 100, 100, 255)) / 255
background = gfx.Background(None, gfx.BackgroundMaterial(light_gray, dark_gray))
scene.add(background)

camera = gfx.PerspectiveCamera(70, 16 / 9)
camera.position.set(0, 0, 500)
controller = gfx.OrbitController(camera.position.clone())
controller.add_default_event_handlers(renderer, camera)


def on_key_down(event):
    if event.key == "s":
        controller.save_state()
    elif event.key == "l":
        controller.load_state()
    elif event.key == "r":
        controller.show_object(camera, scene)


renderer.add_event_handler(on_key_down, "key_down")


def animate():
    for i, cube in enumerate(cubes):
        rot = gfx.linalg.Quaternion().set_from_euler(
            gfx.linalg.Euler(0.005 * i, 0.01 * i)
        )
        cube.rotation.multiply(rot)

    controller.update_camera(camera)

    renderer.render(scene, camera)
    canvas.request_draw()


if __name__ == "__main__":
    canvas.request_draw(animate)
    run()
