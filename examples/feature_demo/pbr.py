"""
PBR Rendering 1
===============


This example shows a complete PBR rendering effect.
The cubemap of skybox is also the environment cubemap of the helmet.
"""

################################################################################
# .. warning::
#     An external model is needed to run this example.
#
# To run this example, you need a model from the source repo's example
# folder. If you are running this example from a local copy of the code (dev
# install) no further actions are needed. Otherwise, you may have to replace
# the path below to point to the location of the model.

import os
from pathlib import Path

try:
    # modify this line if your model is located elsewhere
    model_dir = Path(__file__).parents[1] / "models"
except NameError:
    # compatibility with sphinx-gallery
    model_dir = Path(os.getcwd()).parent / "models"


################################################################################
# Once the path is set correctly, you can use the model as follows:

# sphinx_gallery_pygfx_render = True

import imageio.v3 as iio
from wgpu.gui.auto import WgpuCanvas, run
import pygfx as gfx


# Init
canvas = WgpuCanvas(size=(640, 480), title="gfx_pbr")
renderer = gfx.renderers.WgpuRenderer(canvas)
scene = gfx.Scene()

# Create camera and controller
camera = gfx.PerspectiveCamera(45, 640 / 480, 0.25, 20)
camera.position.set(-1.8, 0.6, 2.7)
controller = gfx.OrbitController(camera.position.clone())
controller.add_default_event_handlers(renderer, camera)

# Read cube image and turn it into a 3D image (a 4d array)
env_img = iio.imread("imageio:meadow_cube.jpg")
cube_size = env_img.shape[1]
env_img.shape = 6, cube_size, cube_size, env_img.shape[-1]

# Create environment map
env_tex = gfx.Texture(
    env_img, dim=2, size=(cube_size, cube_size, 6), generate_mipmaps=True
)
env_view = env_tex.get_view(
    view_dim="cube", layer_range=range(6), address_mode="repeat", filter="linear"
)

# Apply env map to skybox
background = gfx.Background(None, gfx.BackgroundSkyboxMaterial(map=env_view))
scene.add(background)

# Load meshes, and apply env map
# Note that this lits the helmet already
gltf_path = model_dir / "DamagedHelmet" / "glTF" / "DamagedHelmet.gltf"
meshes = gfx.load_scene(gltf_path)
scene.add(*meshes)
m = meshes[0]  # this example has just one mesh
m.material.env_map = env_view

# Add extra light more or less where the sun seems to be in the skybox
scene.add(gfx.SpotLight(color="#444", position=(-500, 1000, -1000)))


def animate():
    controller.update_camera(camera)
    renderer.render(scene, camera)


if __name__ == "__main__":
    renderer.request_draw(animate)
    run()
