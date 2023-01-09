"""
Volume Rendering 1
==================

Render a volume. Shift-click to draw white blobs inside the volume.
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


tex = gfx.Texture(voldata, dim=3)
vol = gfx.Volume(
    gfx.Geometry(grid=tex),
    gfx.VolumeRayMaterial(clim=(0, 2000), map=gfx.cm.cividis),
)
slice = gfx.Volume(
    gfx.Geometry(grid=tex),
    gfx.VolumeSliceMaterial(plane=(0, 0, 1, 0), clim=(0, 2000)),
)
scene.add(vol, slice)

for ob in (slice, vol):
    ob.position.set(*(-0.5 * i for i in voldata.shape[::-1]))

camera = gfx.PerspectiveCamera(70, 16 / 9)
camera.position.z = 500
controller = gfx.OrbitController(
    camera.position.clone(), up=gfx.linalg.Vector3(0, 0, 1)
)
controller.rotate(-0.5, -0.5)
controller.add_default_event_handlers(renderer, camera)


@vol.add_event_handler("pointer_down")
def handle_event(event):
    if "Shift" not in event.modifiers:
        return
    info = event.pick_info
    if "index" in info:
        x, y, z = (max(1, int(i)) for i in info["index"])
        print("Picking", x, y, z)
        tex.data[z - 1 : z + 1, y - 1 : y + 1, x - 1 : x + 1] = 2000
        tex.update_range((x - 1, y - 1, z - 1), (3, 3, 3))


def animate():
    controller.update_camera(camera)
    renderer.render(scene, camera)
    canvas.request_draw()


if __name__ == "__main__":
    canvas.request_draw(animate)
    run()