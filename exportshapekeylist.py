bl_info = {
    "name": "Export Shape Keys List",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy

class OBJECT_OT_export_shape_keys(bpy.types.Operator):
    bl_idname = "object.export_shape_keys"
    bl_label = "Export Shape Keys List"
    bl_description = "Export the list of shape keys of the selected object to a text file"
    bl_options = {'REGISTER', 'UNDO'}

    # ファイルパスのプロパティを定義
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    # ファイルブラウザのフィルター設定用のプロパティ
    filter_glob: bpy.props.StringProperty(
        default='*.txt',
        options={'HIDDEN'}
    )

    def execute(self, context):
        obj = context.active_object

        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected")
            return {'CANCELLED'}

        shape_keys = obj.data.shape_keys
        if shape_keys is None or len(shape_keys.key_blocks) == 0:
            self.report({'ERROR'}, "Selected object has no shape keys")
            return {'CANCELLED'}

        try:
            with open(self.filepath, 'w') as file:
                for key in shape_keys.key_blocks:
                    file.write(key.name + "\n")
            self.report({'INFO'}, "Shape keys list exported successfully")
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        return {'FINISHED'}

    def invoke(self, context, event):
        if context.active_object:
            self.filepath = context.active_object.name + "_ShapeKeysList.txt"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def draw_func(self, context):
    layout = self.layout
    layout.operator(OBJECT_OT_export_shape_keys.bl_idname)

class VIEW3D_PT_tools_export_shape_keys(bpy.types.Panel):
    bl_label = "Export Shape Keys List"
    bl_idname = "OBJECT_PT_export_shape_keys"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    bl_context = 'objectmode'
    
    def draw(self, context):
        draw_func(self, context)

def register():
    bpy.utils.register_class(OBJECT_OT_export_shape_keys)
    bpy.utils.register_class(VIEW3D_PT_tools_export_shape_keys)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_export_shape_keys)
    bpy.utils.unregister_class(VIEW3D_PT_tools_export_shape_keys)

if __name__ == "__main__":
    register()
