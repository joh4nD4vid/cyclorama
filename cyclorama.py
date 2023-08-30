bl_info = {
    "name": "Cyclorama",
    "author": "Johan David",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "Object context menu",
    "description": "Crée un cyclorama et des présets de rendus dans une scène spéciale, autour d'un l'objet choisi.",
}


import bpy


class OBJECT_OT_cyclorama(bpy.types.Operator):


    bl_idname = "object.cyclorama"
    bl_label = "Cyclorama"


    def execute(self, context):
        # Code à exécuter lorsque le bouton est cliqué

        # Seulement si un objet a été sélectionné
        if bpy.context.active_object is not None:

            # On récupère l'objet
            active_object = bpy.context.active_object
            new_object_name = active_object.name + '_cyclorama'

            new_object = active_object.copy()
            new_object.data = active_object.data.copy()
            new_object.name = new_object_name
            new_object.data.name = new_object_name

            # Nouvelle scène
            bpy.ops.scene.new(type="EMPTY")
            cyclo_scene = bpy.data.scenes[-1]
            bpy.context.window.scene = cyclo_scene
            cyclo_scene.name = "Cyclorama_scene"

            cyclo_scene.collection.objects.link(new_object)
            scene_new_object = bpy.data.objects.get(new_object_name)
            scene_new_object.location = [0.58, -0.83, 5.43]
            scene_new_object.rotation_euler = [0, 0, 2.95]
            scene_new_object.scale = [1.15, 1.15, 1.15]

            # Méthode de rendu de la scène
            new_scene = bpy.context.scene
            new_scene.render.engine = 'CYCLES'
            new_scene.cycles.device = 'GPU'
            new_scene.cycles.use_preview_denoising = True
            new_scene.render.resolution_x = 1000
            new_scene.render.resolution_y = 1000
            new_scene.render.pixel_aspect_x = 1
            new_scene.render.pixel_aspect_y = 1

            # Nouvelle zone
            bpy.ops.screen.area_split(direction='VERTICAL', factor=0.5)
            render_zone = bpy.context.screen.areas[-2]
            render_zone.spaces.active.shading.type = 'RENDERED'

            # Nouvelle caméra
            data_cyclo_cam = bpy.data.cameras.new(name="Cyclorama_camera")
            data_cyclo_cam.lens = 100

            object_cyclo_cam = bpy.data.objects.new(name="Cyclorama_camera", object_data=data_cyclo_cam)
            cyclo_cam = bpy.data.objects['Cyclorama_camera']

            cyclo_cam.location = [0.58,9.69,6.06]
            cyclo_cam.location = [0.58,9.69,6.06]
            cyclo_cam.rotation_euler = [1.50,0.0,3.14159]

            bpy.context.collection.objects.link(object_cyclo_cam)

            # La dernière zone créée se positionne sur la caméra
            bpy.context.scene.camera = object_cyclo_cam
            bpy.ops.view3d.view_camera()

            # On crée le Cyclorama
            data_cyclorama_faces = [[17, 4, 2, 3],[4, 17, 27, 6],[6, 27, 26, 7],[7, 26, 25, 8],[8, 25, 24, 9],[9, 24, 23, 10],[10, 23, 22, 11],[11, 22, 21, 12],[12, 21, 20, 13],[13, 20, 19, 14],[14, 19, 18, 15],[15, 18, 16, 5],[0, 5, 16, 1]]
            data_cyclorama_vertices = [[-5.638736248016357, -1.0, 3.502148615552869e-07], [-5.638736248016357, 12.0, 3.502148615552869e-07], [1.0000003576278687, -1.0, 4.638736248016357], [1.0000003576278687, 12.0, 4.638736248016357], [1.0000001192092896, -1.0, 1.7637410163879395], [-0.7637408971786499, -1.0, 9.304305592650053e-08], [0.9820477962493896, -1.0, 1.5127345323562622], [0.9285562038421631, -1.0, 1.2668378353118896], [0.8406143188476562, -1.0, 1.0310566425323486], [0.7200123071670532, -1.0, 0.8101906776428223], [0.5692055225372314, -1.0, 0.6087362766265869], [0.3912637233734131, -1.0, 0.43079447746276855], [0.18980944156646729, -1.0, 0.27998781204223633], [-0.031056463718414307, -1.0, 0.15938591957092285], [-0.2668376564979553, -1.0, 0.07144403457641602], [-0.5127344131469727, -1.0, 0.017952442169189453], [-0.7637407779693604, 12.0, 9.304304171564581e-08], [1.0000001192092896, 12.0, 1.76374089717865], [-0.5127342939376831, 12.0, 0.017952442169189453], [-0.26683756709098816, 12.0, 0.07144403457641602], [-0.031056344509124756, 12.0, 0.15938591957092285], [0.18980950117111206, 12.0, 0.27998781204223633], [0.39126384258270264, 12.0, 0.43079447746276855], [0.5692055225372314, 12.0, 0.6087362766265869], [0.7200123071670532, 12.0, 0.8101906180381775], [0.8406143188476562, 12.0, 1.031056523323059], [0.9285562038421631, 12.0, 1.2668377161026], [0.9820477962493896, 12.0, 1.5127344131469727]]

            cyclo_mesh = bpy.data.meshes.new('cyclo_mesh')
            cyclo_mesh.from_pydata(data_cyclorama_vertices, [], data_cyclorama_faces)
            cyclo_mesh.update()

            cyclo_object = bpy.data.objects.new(name="Cyclorama", object_data=cyclo_mesh)
            bpy.context.collection.objects.link(cyclo_object)

            # Matériau du cyclorama
            bpy.context.view_layer.objects.active = bpy.data.objects['Cyclorama']
            bpy.ops.material.new()
            cyclorama_materiel = bpy.data.materials[-1]
            cyclorama_materiel.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.85
            Cyclo_object = bpy.data.objects["Cyclorama"]
            Cyclo_object.data.materials.append(cyclorama_materiel)

            # Active le smooth sur le cyclorama
            bpy.ops.object.select_all(action='DESELECT')
            Cyclo_object.select_set(True)
            bpy.context.view_layer.objects.active = Cyclo_object
            bpy.ops.object.shade_smooth()

            # Positionne l'objet
            bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY")
            Cyclo_object.location = (0.58,-3.15,3.28)
            Cyclo_object.rotation_euler = (0,0,-1.5708)
            Cyclo_object.scale = (3.54,3.54,3.54)

            # Ajoute les lumières
            data_key_light = bpy.data.lights.new(name="key_light", type="AREA")
            object_key_light = bpy.data.objects.new(name="Key_Light", object_data=data_key_light)
            bpy.context.collection.objects.link(object_key_light)

            data_fill_light = bpy.data.lights.new(name="fill_light", type="AREA")
            object_fill_light = bpy.data.objects.new(name="Fill_Light", object_data=data_fill_light)
            bpy.context.collection.objects.link(object_fill_light)

            data_back_light = bpy.data.lights.new(name="back_light", type="AREA")
            object_back_light = bpy.data.objects.new(name="Back_Light", object_data=data_back_light)
            bpy.context.collection.objects.link(object_back_light)

            # Positionnement des lumières
            object_key_light.location = [-4.0, 5.59, 7.36]
            object_key_light.rotation_euler = [1.35, 0.0, 3.75]

            object_fill_light.location = [4.10, 5.78, 6.55]
            object_fill_light.rotation_euler = [3.14159, 1.71, 4.406]

            object_back_light.location = [-1.26, -2.65, 7.34]
            object_back_light.rotation_euler = [1.57, 0, -0.32]

            # Propriétés des lumières
            data_key_light.energy = 520
            data_key_light.size = 1.92
            data_key_light.color = (1.0, 0.9, 0.9)
            data_key_light.spread = 3.14159

            data_fill_light.energy = 150
            data_fill_light.size = 2.5
            data_fill_light.color = (1.0, 0.69, 0.45)
            data_fill_light.spread = 2.52

            data_back_light.energy = 500
            data_back_light.size = 0.75
            data_back_light.color = (0.75, 0.88, 1.0)
            data_back_light.spread = 3.14159

            bpy.context.view_layer.update()

            return {'FINISHED'}


        else:
            print("Veuillez sélectionner un objet avant de lancer le Cyclorama.")
            return {'FINISHED'}



# Ajoute Cyclorama dans le menu objet 3D
def add_menu_cyclorama(self, context):
    self.layout.separator()
    self.layout.operator('object.cyclorama', icon='OUTLINER_DATA_CAMERA')

bpy.types.VIEW3D_MT_object_context_menu.append(add_menu_cyclorama)



# Enregistre/Désenregistre la classe
def register():
    bpy.utils.register_class(OBJECT_OT_cyclorama)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_cyclorama)



# Appel de la fonction de départ
if __name__ == "__main__":
    register()