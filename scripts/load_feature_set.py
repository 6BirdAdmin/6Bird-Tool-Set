import bpy
import os
import shutil
import rigify.feature_set_list

def load_feature_set():
    # ==========================
    # USER SETTINGS
    # ==========================

    active_fs = "6_bird_feature_set"  # folder / feature set name
    active_fn = "/6_bird_feature_set/"
    source_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/6_bird_feature_set/'
    rigify_config_path = rigify.feature_set_list.get_install_path()
    installed_sets = rigify.feature_set_list.get_installed_modules_names()
    addon_prefs = rigify.RigifyPreferences.get_instance()

    # ==========================
    # ENSURE RIGIFY IS ENABLED
    # ==========================

    if "rigify" not in bpy.context.preferences.addons:
        bpy.ops.preferences.addon_enable(module="rigify")

    # ==========================
    # UNINSTALL EXISTING FEATURE SET
    # ==========================


    if active_fs in installed_sets:
        active_idx = rigify.feature_set_list.get_installed_modules_names().index(active_fs)
        # Call the 'unregister' callback of the set being removed.
        rigify.feature_set_list.call_register_function(active_fs, do_register=False)

        # Remove the feature set's folder from the file system.
        if rigify_config_path:
            set_path = os.path.join(rigify_config_path, active_fs)
            if os.path.exists(set_path):
                shutil.rmtree(set_path)

        # Remove the feature set's entry from the addon preferences.
        addon_prefs.rigify_feature_sets.remove(active_idx)

        # Remove the feature set's entries from the metarigs and rig types.
        addon_prefs.refresh_installed_feature_sets()
        addon_prefs.update_external_rigs()
        print(f"Removed existing Rigify feature set: {active_fs}")

    # ==========================
    # INSTALL FEATURE SET
    # ==========================
    target_dir = rigify_config_path+active_fn
    os.makedirs(os.path.dirname(target_dir), exist_ok=True)
    shutil.copytree(source_folder, target_dir, dirs_exist_ok = True)
    addon_prefs.refresh_installed_feature_sets()
    rigify.feature_set_list.call_register_function(active_fs, True)
    addon_prefs.update_external_rigs()
    print(f"Installed Rigify feature set {active_fs}")

    # ==========================
    # POPUP: RESTART NOTICE
    # ==========================

    def restart_popup(self, context):
        self.layout.label(text="Rigify Feature Set Installed")
        self.layout.separator()
        self.layout.label(
            text="A Blender restart may be required for the feature set"
        )
        self.layout.label(
            text="to appear due to Python module caching."
        )

    bpy.context.window_manager.popup_menu(
        restart_popup,
        title="Restart Recommended",
        icon='INFO'
    )