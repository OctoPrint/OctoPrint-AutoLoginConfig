# -*- coding: utf-8 -*-
from __future__ import absolute_import

import flask
import octoprint.plugin
from octoprint.access.permissions import Permissions

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

# API COMMANDS
SAVE_COMMAND = "save_config"


class AutologinConfigPlugin(
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.SimpleApiPlugin,
):

    # TemplatePlugin mixin
    def get_template_configs(self):
        return [
            {
                "type": "settings",
                "name": "AutoLogin Configuration",
                "template": "autologin_config_settings.jinja2",
                "custom_bindings": True,
            }
        ]

    def get_template_vars(self):
        return {"version": self._plugin_version}

    # AssetPlugin mixin
    def get_assets(self):
        return {
            "js": ["js/autologin_config.js"],
            "css": ["css/autologin_config.css"],
        }

    # SimpleApiPlugin mixin
    def get_api_commands(self):
        return {SAVE_COMMAND: ["enabled", "loginAs", "localNetworks"]}

    def on_api_command(self, command, data):
        if Permissions.ADMIN.can():
            if command == SAVE_COMMAND:
                self.save_autologin_settings(data)
        else:
            return flask.abort(403)

        return self.api_response()

    def on_api_get(self, request=None):
        if Permissions.ADMIN.can():
            return self.api_response()
        else:
            return flask.abort(403)

    def api_response(self):
        return flask.jsonify(self.get_autologin_settings())

    def get_autologin_settings(self):
        enabled = self._settings.global_get(["accessControl", "autologinLocal"])
        login_as = self._settings.global_get(["accessControl", "autologinAs"])
        local_networks = self._settings.global_get(["accessControl", "localNetworks"])
        return {
            "enabled": enabled,
            "loginAs": login_as,
            "localNetworks": local_networks,
        }

    def save_autologin_settings(self, data):
        self._settings.global_set(
            ["accessControl", "autologinLocal"],
            data.get("enabled"),
            force=True,
        )
        self._settings.global_set(
            ["accessControl", "autologinAs"],
            data.get("loginAs"),
            force=True,
        )
        self._settings.global_set(
            ["accessControl", "localNetworks"],
            data.get("localNetworks"),
            force=True,
        )
        self._logger.info("Autologin settings saved")

    # Softwareupdate hook
    def get_update_information(self):
        return {
            "autologin_config": {
                "displayName": "Autologin Config",
                "displayVersion": self._plugin_version,
                # version check: github repository
                "type": "github_release",
                "user": "cp2004",
                "repo": "OctoPrint-AutoLoginConfig",
                "current": self._plugin_version,
                "stable_branch": {
                    "name": "Stable",
                    "branch": "master",
                    "comittish": ["main"],
                },
                "prerelease_branches": [
                    {
                        "name": "Release Candidate",
                        "branch": "pre-release",
                        "comittish": ["pre-release", "main"],
                    }
                ],
                # update method: pip
                "pip": "https://github.com/cp2004/OctoPrint-AutoLoginConfig/archive/{target_version}.zip",
            }
        }


__plugin_name__ = "Autologin Configuration"
__plugin_version__ = __version__
__plugin_pythoncompat__ = ">=2.7,<4"  # python 2 and 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = AutologinConfigPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
