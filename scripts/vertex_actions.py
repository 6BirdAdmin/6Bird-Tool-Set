import bpy
import bmesh

def select_verts_below_weight_threshold(obj, threshold=0.1):

    # Ensure there's an active object and it's a mesh
    if not obj or obj.type != 'MESH':
        print("Active object is not a mesh.")
        return

    # Switch to Edit Mode
    bpy.ops.object.mode_set(mode='EDIT')

    mesh = obj.data
    bm = bmesh.from_edit_mesh(mesh)

    # Ensure vertex selection mode
    bpy.ops.mesh.select_mode(type="VERT")

    # Deselect everything first
    for v in bm.verts:
        v.select = False

    # Access mesh vertices for weight data
    mesh_verts = mesh.vertices

    # Select vertices whose total weight is below the threshold
    for v in bm.verts:
        total_weight = 0.0

        for g in mesh_verts[v.index].groups:
            total_weight += g.weight

        if total_weight < threshold:
            v.select = True

    # Update the mesh
    bmesh.update_edit_mesh(mesh, loop_triangles=False)

    text = f"Selected vertices with total weight below {threshold}"
    print(text)
    return text