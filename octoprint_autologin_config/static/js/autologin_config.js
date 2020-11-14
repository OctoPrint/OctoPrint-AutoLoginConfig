/*
 * View model for OctoPrint-AutoLoginConfig
 *
 * Author: Charlie Powell
 * License: AGPLv3
 */
$(function () {
    function Autologin_configViewModel(parameters) {
        var self = this;
        self.settingsViewModel = parameters[1];
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: Autologin_configViewModel,
        dependencies: [],
        // Elements to bind to, e.g. #settings_plugin_autologin_config, #tab_plugin_autologin_config, ...
        elements: [""],
    });
});
