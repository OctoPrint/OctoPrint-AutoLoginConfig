/*
 * View model for OctoPrint-AutoLoginConfig
 *
 * Author: Charlie Powell
 * License: AGPLv3
 */
$(function () {
    function Autologin_configViewModel(parameters) {
        var self = this;
        console.log(parameters);
        self.settingsViewModel = parameters[0];
        self.accessViewModel = parameters[1];
        self.loginState = parameters[2];

        // Initialise observables
        self.enabled = ko.observable(false);
        self.loginAs = ko.observable();
        self.localNetworks = ko.observableArray([]);

        self.newLocalNetwork = ko.observable('');
        self.newLocalNetworkIsValid = ko.computed(function(){
            var filtered_networks = ko.utils.arrayFilter(self.localNetworks(), function(item) {
                return item === self.newLocalNetwork();
            });
            return filtered_networks.length === 0 && (self.newLocalNetwork().match(/^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/(3[0-2]|[1-2][0-9]|[0-9]))?$/));
        })
        self.allUsers = ko.observableArray([]);

        self.addLocalNetwork = function () {
            if (!self.check_admin()) {
                return;
            }
            self.localNetworks.unshift(self.newLocalNetwork());
            self.newLocalNetwork("");
        };

        self.removeLocalNetwork = function (network) {
            if (!self.check_admin()) {
                return;
            }

            self.localNetworks.remove(network);
        };

        self.check_admin = function () {
            return self.loginState.hasPermission(
                self.accessViewModel.permissions.ADMIN
            );
        };

        self.onSettingsBeforeSave = function () {
            if (!self.check_admin()) {
                return;
            }

            OctoPrint.simpleApiCommand("autologin_config", "save_config", {
                enabled: self.enabled(),
                loginAs: self.loginAs(),
                localNetworks: self.localNetworks(),
            }).done(self.on_api_repsonse);
        };

        self.onAllBound = function () {
            if (self.check_admin()) {
                OctoPrint.simpleApiGet("autologin_config").done(
                    self.on_api_repsonse
                );
            }
            OctoPrint.access.users.list().done(function (response) {
                _.each(response.users, function (user) {
                    self.allUsers.push(user.name);
                });
            });
        };

        self.on_api_repsonse = function (response) {
            if (response.enabled) {
                self.enabled(true);
            }
            if (response.loginAs) {
                self.loginAs(response.loginAs);
            }
            if (response.localNetworks) {
                self.localNetworks(response.localNetworks);
            }
        };
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: Autologin_configViewModel,
        dependencies: [
            "settingsViewModel",
            "accessViewModel",
            "loginStateViewModel",
        ],
        elements: ["#settings_plugin_autologin_config"],
    });
});
