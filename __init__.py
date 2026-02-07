bl_info = {
    "name": "6 Bird Studio Tool Set",
    "author": "6 Bird Studio",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > 6 Bird",
    "description": "Custom animation tools",
    "category": "3D View",
}

import bpy
from bpy.types import Panel, Operator
from bpy.props import EnumProperty, FloatProperty
from .scripts.vertex_actions import *
from .scripts.load_feature_set import *



# -------------------------------------------------
# Operators
# -------------------------------------------------

class BIRD_VERT_button(Operator):
    bl_idname = "vert1.button"
    bl_label = "Selected vertices based on threshold."

    def execute(self, context):
        scene = context.scene

        # Prepare Arguments
        value = getattr(scene, f"bird_value_1")
        obj = bpy.context.active_object

        # Call external logic
        text = select_verts_below_weight_threshold(obj, value)

        self.report({'INFO'}, text)
        return {'FINISHED'}

class BIRD_LOAD_button(Operator):
    bl_idname = "load1.button"
    bl_label = "Load Rigify feature set."

    def execute(self, context):
        load_feature_set()
        self.report({'INFO'}, "Feature Set Updated")
        return {'FINISHED'}


# -------------------------------------------------
# Properties
# -------------------------------------------------

def register_properties():
        setattr(
            bpy.types.Scene,
            f"bird_enum_1",
            EnumProperty(
                name="Mode",
                items=[
                    ("A", "Option A", ""),
                    ("B", "Option B", ""),
                    ("C", "Option C", ""),
                ],
                default="A",
            ),
        )

        setattr(
            bpy.types.Scene,
            f"bird_value_1",
            FloatProperty(
                name="Value",
                default=0.5,
                min=0.0,
                max=1.0,
            ),
        )


def unregister_properties():
    delattr(bpy.types.Scene, f"bird_enum_1")
    delattr(bpy.types.Scene, f"bird_value_1")


# -------------------------------------------------
# Panel
# -------------------------------------------------

class VIEW3D_PT_six_bird(Panel):
    bl_label = "6 Bird Control"
    bl_idname = "VIEW3D_PT_six_bird"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "6 Bird"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Load Features
        box1 = layout.box()
        box1.label(text=f"Load Features")
        box1.prop(scene, f"bird_enum_1", expand=True)
        box1.operator("load1.button", text="Run")

        # Mesh Tools
        box2 = layout.box()
        box2.label(text=f"Select Verts by Weight")
        box2.prop(scene, f"bird_value_1", slider=True)
        box2.operator("vert1.button", text="Run")


# -------------------------------------------------
# Registration
# -------------------------------------------------

classes = (
    BIRD_VERT_button,
    BIRD_LOAD_button,
    VIEW3D_PT_six_bird,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_properties()


def unregister():
    unregister_properties()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
