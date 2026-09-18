"""Render the conceptual research instrument used on the site homepage.

Run from the repository root:

    blender --background --python scripts/render_research_figure.py

The script builds the complete scene, saves an editable .blend source, and
renders the final 1600 x 1000 WebP. No external textures or fonts are used.
"""

from __future__ import annotations

import math
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "images" / "research-instrument.webp"
BLEND_FILE = ROOT / "artwork" / "research-instrument.blend"


def hex_color(value: str) -> tuple[float, float, float, float]:
    """Convert an sRGB hex color to Blender's linear color space."""

    value = value.lstrip("#")
    channels = [int(value[index : index + 2], 16) / 255 for index in (0, 2, 4)]

    def linear(channel: float) -> float:
        return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4

    return (*[linear(channel) for channel in channels], 1.0)


PALETTE = {
    "paper": "#F5F1E8",
    "ivory": "#E9DFC9",
    "ivory_light": "#FBF8F1",
    "sage": "#758F78",
    "sage_light": "#B5C4AD",
    "sage_dark": "#405B4E",
    "ink": "#25342D",
    "clay": "#C97F5B",
    "ochre": "#D5AE68",
}


def material(name: str, color: str, roughness: float = 0.55) -> bpy.types.Material:
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = hex_color(color)
    principled = mat.node_tree.nodes.get("Principled BSDF")
    principled.inputs["Base Color"].default_value = hex_color(color)
    principled.inputs["Roughness"].default_value = roughness
    principled.inputs["Metallic"].default_value = 0.0
    return mat


def assign(obj: bpy.types.Object, mat: bpy.types.Material) -> bpy.types.Object:
    obj.data.materials.append(mat)
    return obj


def smooth(obj: bpy.types.Object) -> None:
    if hasattr(obj.data, "polygons"):
        for polygon in obj.data.polygons:
            polygon.use_smooth = True


def rounded_box(
    name: str,
    location: tuple[float, float, float],
    dimensions: tuple[float, float, float],
    mat: bpy.types.Material,
    bevel: float = 0.12,
    rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    modifier = obj.modifiers.new(name="Soft edges", type="BEVEL")
    modifier.width = min(bevel, min(dimensions) * 0.45)
    modifier.segments = 4
    return assign(obj, mat)


def cylinder(
    name: str,
    location: tuple[float, float, float],
    radius: float,
    depth: float,
    mat: bpy.types.Material,
    rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
    vertices: int = 48,
    bevel: float = 0.04,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    if bevel:
        modifier = obj.modifiers.new(name="Soft edges", type="BEVEL")
        modifier.width = bevel
        modifier.segments = 3
    assign(obj, mat)
    smooth(obj)
    return obj


def sphere(
    name: str,
    location: tuple[float, float, float],
    radius: float,
    mat: bpy.types.Material,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=40,
        ring_count=20,
        radius=radius,
        location=location,
    )
    obj = bpy.context.object
    obj.name = name
    assign(obj, mat)
    smooth(obj)
    return obj


def cone(
    name: str,
    location: tuple[float, float, float],
    radius1: float,
    radius2: float,
    depth: float,
    mat: bpy.types.Material,
    rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cone_add(
        vertices=48,
        radius1=radius1,
        radius2=radius2,
        depth=depth,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    modifier = obj.modifiers.new(name="Soft edges", type="BEVEL")
    modifier.width = 0.06
    modifier.segments = 3
    assign(obj, mat)
    smooth(obj)
    return obj


def pawn(
    name: str,
    location: tuple[float, float, float],
    scale: float,
    mat: bpy.types.Material,
) -> None:
    x, y, z = location
    cylinder(f"{name} base", (x, y, z + 0.08 * scale), 0.27 * scale, 0.16 * scale, mat)
    cone(
        f"{name} body",
        (x, y, z + 0.45 * scale),
        0.24 * scale,
        0.13 * scale,
        0.58 * scale,
        mat,
    )
    sphere(f"{name} head", (x, y, z + 0.86 * scale), 0.20 * scale, mat)


def bar_on_horizontal_card(
    name: str,
    location: tuple[float, float, float],
    length: float,
    mat: bpy.types.Material,
) -> None:
    rounded_box(name, location, (length, 0.09, 0.055), mat, bevel=0.025)


def connector_curve(mat: bpy.types.Material) -> None:
    curve = bpy.data.curves.new("Instrument path", type="CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 20
    curve.bevel_depth = 0.065
    curve.bevel_resolution = 4
    spline = curve.splines.new("BEZIER")
    points = [(-6.2, 1.82, 0.34), (-2.35, 1.76, 0.34), (2.05, 1.80, 0.34), (6.1, 1.72, 0.34)]
    spline.bezier_points.add(len(points) - 1)
    for point, coordinate in zip(spline.bezier_points, points):
        point.co = coordinate
        point.handle_left_type = "AUTO"
        point.handle_right_type = "AUTO"
    obj = bpy.data.objects.new("Instrument path", curve)
    curve.materials.append(mat)
    bpy.context.collection.objects.link(obj)
    for index, (x, y, z) in enumerate(points, start=1):
        sphere(f"Path node {index}", (x, y, z), 0.13, mat)


def create_game_stage(materials: dict[str, bpy.types.Material]) -> None:
    # A raised board with varied terrain and pieces reads as the simulated game.
    rounded_box("Game pedestal", (-6.15, 0.05, 0.48), (3.15, 3.25, 0.30), materials["sage_dark"], 0.24)
    rounded_box("Game board", (-6.15, -0.02, 0.72), (2.78, 2.88, 0.24), materials["ivory"], 0.18)
    tile_colors = [
        "sage_light", "ivory_light", "sage_light",
        "ivory_light", "sage", "ivory_light",
        "sage_light", "ivory_light", "sage_light",
    ]
    for index, (row, column) in enumerate((r, c) for r in range(3) for c in range(3)):
        x = -6.15 + (column - 1) * 0.82
        y = -0.02 + (row - 1) * 0.86
        z = 0.88 + (0.035 if index % 2 else 0.0)
        rounded_box(
            f"Terrain tile {row + 1}-{column + 1}",
            (x, y, z),
            (0.69, 0.72, 0.12),
            materials[tile_colors[index]],
            0.10,
        )

    pawn("Clay game pawn", (-6.93, -0.78, 0.98), 0.78, materials["clay"])
    pawn("Ochre game pawn", (-5.36, 0.06, 0.98), 0.68, materials["ochre"])
    # A miniature landmark makes the stage feel environmental rather than like a chart.
    cylinder("Tree trunk", (-6.15, 0.80, 1.13), 0.10, 0.42, materials["sage_dark"])
    cone("Tree crown", (-6.15, 0.80, 1.55), 0.40, 0.05, 0.78, materials["sage"])


def create_ai_cards(materials: dict[str, bpy.types.Material]) -> None:
    rounded_box("AI card dock", (-2.28, 0.34, 0.49), (3.00, 2.85, 0.32), materials["ivory"], 0.24)
    cards = [
        (-2.76, 0.47, 2.00, -0.13, "sage_light"),
        (-2.18, 0.28, 2.16, 0.00, "ivory_light"),
        (-1.55, 0.50, 1.96, 0.13, "sage"),
    ]
    for number, (x, y, z, angle, color) in enumerate(cards, start=1):
        rounded_box(
            f"AI suggestion card {number}",
            (x, y, z),
            (1.28, 0.18, 2.25),
            materials[color],
            0.16,
            rotation=(0.0, angle, angle * 0.45),
        )

    # The front card carries a text-free network glyph and confidence-like bars.
    face_y = 0.15
    nodes = [(-2.55, 1.79), (-2.15, 2.28), (-1.78, 1.78), (-2.15, 1.46)]
    for index, (x, z) in enumerate(nodes, start=1):
        cylinder(
            f"Network node {index}",
            (x, face_y, z),
            0.105 if index != 2 else 0.14,
            0.075,
            materials["ivory_light" if index != 2 else "clay"],
            rotation=(math.pi / 2, 0.0, 0.0),
            bevel=0.02,
        )
    links = [
        (-2.36, 0.14, 2.03, 0.59, 0.69),
        (-1.96, 0.14, 2.03, 0.55, -0.75),
        (-2.35, 0.14, 1.63, 0.48, -0.40),
        (-1.95, 0.14, 1.62, 0.48, 0.40),
    ]
    for index, (x, y, z, length, angle) in enumerate(links, start=1):
        rounded_box(
            f"Network link {index}",
            (x, y, z),
            (length, 0.05, 0.055),
            materials["ivory_light"],
            0.02,
            rotation=(0.0, angle, 0.0),
        )
    for index, length in enumerate((0.72, 0.50, 0.31), start=1):
        rounded_box(
            f"AI measure {index}",
            (-2.46 + length / 2, 0.12, 1.02 - index * 0.16),
            (length, 0.055, 0.075),
            materials["sage_dark"],
            0.025,
        )


def create_human_choice(materials: dict[str, bpy.types.Material]) -> None:
    rounded_box("Decision pedestal", (2.05, 0.22, 0.45), (3.15, 3.05, 0.24), materials["sage_light"], 0.24)
    cylinder("Decision token", (2.05, 0.38, 0.73), 0.82, 0.30, materials["ivory_light"], bevel=0.08)
    pawn("Human decision maker", (2.05, 0.38, 0.88), 1.30, materials["ink"])

    # A physical fork and two large pads show the human decision point.
    rounded_box("Decision stem", (2.05, -0.52, 0.69), (0.13, 0.88, 0.12), materials["ivory_light"], 0.05)
    rounded_box(
        "Left decision branch",
        (1.60, -0.92, 0.69),
        (0.13, 0.85, 0.12),
        materials["ivory_light"],
        0.05,
        rotation=(0.0, 0.0, -0.82),
    )
    rounded_box(
        "Right decision branch",
        (2.50, -0.92, 0.69),
        (0.13, 0.85, 0.12),
        materials["ivory_light"],
        0.05,
        rotation=(0.0, 0.0, 0.82),
    )
    cylinder("Alternative choice", (1.28, -1.23, 0.78), 0.36, 0.20, materials["sage_dark"], bevel=0.06)
    cylinder("Selected choice", (2.81, -1.23, 0.80), 0.42, 0.24, materials["clay"], bevel=0.07)
    # A small marker rising from the selected pad creates an unmistakable selection gesture.
    cone(
        "Selection marker",
        (2.81, -1.23, 1.18),
        0.18,
        0.03,
        0.50,
        materials["ochre"],
    )


def create_event_records(materials: dict[str, bpy.types.Material]) -> None:
    rounded_box("Record pedestal", (6.05, 0.26, 0.46), (3.20, 3.08, 0.28), materials["ivory"], 0.24)
    # An open archive tray supports a staggered stack of event sheets.
    rounded_box("Archive tray base", (6.05, 0.34, 0.70), (2.72, 2.38, 0.22), materials["sage_dark"], 0.18)
    rounded_box("Archive tray left", (4.78, 0.44, 1.05), (0.18, 2.30, 0.74), materials["sage_dark"], 0.08)
    rounded_box("Archive tray right", (7.32, 0.44, 1.05), (0.18, 2.30, 0.74), materials["sage_dark"], 0.08)
    sheets = [
        (5.90, 0.53, 0.93, "sage_light"),
        (6.05, 0.32, 1.08, "ivory_light"),
        (6.20, 0.08, 1.23, "ivory_light"),
    ]
    for number, (x, y, z, color) in enumerate(sheets, start=1):
        rounded_box(
            f"Event sheet {number}",
            (x, y, z),
            (2.25, 1.72, 0.14),
            materials[color],
            0.12,
            rotation=(0.0, 0.0, 0.045 * (number - 2)),
        )

    # Repeating dot-and-bar rows signal timestamped records without tiny text.
    row_y = [-0.49, -0.06, 0.37, 0.79]
    lengths = [1.05, 0.73, 1.18, 0.88]
    for index, (y, length) in enumerate(zip(row_y, lengths), start=1):
        sphere(f"Record dot {index}", (5.46, y, 1.39), 0.095, materials["clay" if index == 1 else "sage"])
        bar_on_horizontal_card(
            f"Record row {index}",
            (5.68 + length / 2, y, 1.39),
            length,
            materials["ink" if index == 1 else "sage_dark"],
        )
    cylinder("Archive index", (6.97, 0.74, 1.46), 0.22, 0.12, materials["ochre"], bevel=0.05)


def point_camera(camera: bpy.types.Object, target: tuple[float, float, float]) -> None:
    direction = Vector(target) - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def setup_camera_and_lights(materials: dict[str, bpy.types.Material]) -> None:
    bpy.ops.object.camera_add(location=(14.7, -20.5, 15.2))
    camera = bpy.context.object
    camera.name = "Orthographic camera"
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = 17.8
    camera.data.lens = 55
    point_camera(camera, (0.0, 0.10, 1.05))
    bpy.context.scene.camera = camera

    lights = [
        ("Large warm key", (-6.0, -8.0, 14.0), 1150, 7.5, "#FFF3DF"),
        ("Soft fill", (8.0, -1.0, 10.0), 800, 6.0, "#E2ECDD"),
        ("Rear rim", (1.0, 8.0, 12.0), 900, 5.0, "#FFF8EE"),
    ]
    for name, location, energy, size, color in lights:
        data = bpy.data.lights.new(name=name, type="AREA")
        data.energy = energy
        data.shape = "DISK"
        data.size = size
        data.color = hex_color(color)[:3]
        obj = bpy.data.objects.new(name, data)
        obj.location = location
        point_camera(obj, (0.0, 0.0, 0.4))
        bpy.context.collection.objects.link(obj)

    # An ivory studio floor catches soft shadows and matches the site's paper ground.
    rounded_box("Instrument plinth", (0.0, 0.26, 0.16), (16.20, 4.70, 0.25), materials["paper"], 0.52)
    rounded_box("Studio floor", (0.0, 0.0, -0.09), (70.0, 70.0, 0.18), materials["ivory_light"], 0.03)


def configure_render() -> None:
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "WEBP"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "8"
    scene.render.image_settings.quality = 88
    scene.render.filepath = str(OUTPUT)
    scene.render.film_transparent = False
    scene.render.image_settings.color_management = "FOLLOW_SCENE"
    scene.render.use_file_extension = True

    if scene.world is None:
        scene.world = bpy.data.worlds.new("Paper world")
    scene.world.color = hex_color(PALETTE["paper"])[:3]
    background = scene.world.node_tree.nodes.get("Background")
    background.inputs["Color"].default_value = hex_color(PALETTE["paper"])
    background.inputs["Strength"].default_value = 0.72

    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.view_settings.exposure = 0.15

    scene.render.image_settings.color_mode = "RGB"
    scene.render.film_transparent = False


def build_scene() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    materials = {name: material(name.replace("_", " ").title(), value) for name, value in PALETTE.items()}

    setup_camera_and_lights(materials)
    connector_curve(materials["sage"])
    create_game_stage(materials)
    create_ai_cards(materials)
    create_human_choice(materials)
    create_event_records(materials)
    configure_render()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    BLEND_FILE.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_FILE))
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    build_scene()
