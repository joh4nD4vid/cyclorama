bl_info = {
    "name": "Cyclorama",
    "author": "Johan David",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "Object context menu",
    "description": "Crée un cyclorama et des presets de rendus dans une scène spéciale, autour de l'objet choisi.",
    "category": "Object",
}

import bpy

class OBJECT_OT_cyclorama(bpy.types.Operator):
    bl_idname = "object.cyclorama"
    bl_label = "Créer un Cyclorama"
    bl_description = "Crée une scène dédiée avec un cyclorama autour de l'objet actif"

    def execute(self, context):
        if bpy.context.active_object is None:
            self.report({'WARNING'}, "Aucun objet actif.")
            return {'CANCELLED'}

        active_object = bpy.context.active_object
        new_object_name = active_object.name + '_cyclorama'

        new_object = active_object.copy()
        new_object.data = active_object.data.copy()
        new_object.name = new_object_name
        new_object.data.name = new_object_name

        # Nouvelle scène vide
        bpy.ops.scene.new(type="EMPTY")
        cyclo_scene = bpy.context.window.scene
        cyclo_scene.name = "Cyclorama_scene"

        cyclo_scene.collection.objects.link(new_object)
        new_object.location = [0.58, -0.83, 5.43]
        new_object.rotation_euler = [0, 0, 2.95]
        new_object.scale = [1.15, 1.15, 1.15]

        # Paramètres de rendu
        cyclo_scene.render.engine = 'CYCLES'
        cyclo_scene.cycles.device = 'GPU'
        cyclo_scene.cycles.use_preview_denoising = True
        cyclo_scene.render.resolution_x = 1000
        cyclo_scene.render.resolution_y = 1000
        cyclo_scene.render.pixel_aspect_x = 1
        cyclo_scene.render.pixel_aspect_y = 1

        # Création caméra
        cam_data = bpy.data.cameras.new(name="Cyclorama_camera")
        cam_data.lens = 100
        cam_obj = bpy.data.objects.new("Cyclorama_camera", cam_data)
        cam_obj.location = [0.58, 9.69, 6.06]
        cam_obj.rotation_euler = [1.50, 0.0, 3.14159]
        cyclo_scene.collection.objects.link(cam_obj)
        cyclo_scene.camera = cam_obj

        # Création du mesh cyclorama
        verts = [[-5.638736248016357, -1.0, 3.5e-07], [-5.638736248016357, 12.0, 3.5e-07],
                 [1.0, -1.0, 4.638736248016357], [1.0, 12.0, 4.638736248016357],
                 [1.0, -1.0, 1.7637410163879395], [-0.7637408971786499, -1.0, 9.3e-08],
                 [0.9820477962493896, -1.0, 1.5127345323562622], [0.9285562038421631, -1.0, 1.2668378353118896],
                 [0.8406143188476562, -1.0, 1.0310566425323486], [0.7200123071670532, -1.0, 0.8101906776428223],
                 [0.5692055225372314, -1.0, 0.6087362766265869], [0.3912637233734131, -1.0, 0.43079447746276855],
                 [0.18980944156646729, -1.0, 0.27998781204223633], [-0.031056463718414307, -1.0, 0.15938591957092285],
                 [-0.2668376564979553, -1.0, 0.07144403457641602], [-0.5127344131469727, -1.0, 0.017952442169189453],
                 [-0.7637407779693604, 12.0, 9.3e-08], [1.0, 12.0, 1.76374089717865],
                 [-0.5127342939376831, 12.0, 0.017952442169189453], [-0.26683756709098816, 12.0, 0.07144403457641602],
                 [-0.031056344509124756, 12.0, 0.15938591957092285], [0.18980950117111206, 12.0, 0.27998781204223633],
                 [0.39126384258270264, 12.0, 0.43079447746276855], [0.5692055225372314, 12.0, 0.6087362766265869],
                 [0.7200123071670532, 12.0, 0.8101906180381775], [0.8406143188476562, 12.0, 1.031056523323059],
                 [0.9285562038421631, 12.0, 1.2668377161026], [0.9820477962493896, 12.0, 1.5127344131469727]]

        faces = [[17, 4, 2, 3], [4, 17, 27, 6], [6, 27, 26, 7], [7, 26, 25, 8], [8, 25, 24, 9],
                 [9, 24, 23, 10], [10, 23, 22, 11], [11, 22, 21, 12], [12, 21, 20, 13],
                 [13, 20, 19, 14], [14, 19, 18, 15], [15, 18, 16, 5], [0, 5, 16, 1]]

        mesh = bpy.data.meshes.new("Cyclorama_mesh")
        mesh.from_pydata(verts, [], faces)
        mesh.update()

        obj = bpy.data.objects.new("Cyclorama", mesh)
        cyclo_scene.collection.objects.link(obj)

        # Matériau
        mat = bpy.data.materials.new(name="Cyclorama_Material")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Specular"].default_value = 0.0
        obj.data.materials.append(mat)

        return {'FINISHED'}

# Menu clic droit dans le viewport
def menu_func(self, context):
    self.layout.operator(OBJECT_OT_cyclorama.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_cyclorama)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)
    bpy.utils.unregister_class(OBJECT_OT_cyclorama)

if __name__ == "__main__":
    register()
