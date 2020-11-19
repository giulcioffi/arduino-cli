// This file is part of arduino-cli.
//
// Copyright 2020 ARDUINO SA (http://www.arduino.cc/)
//
// This software is released under the GNU General Public License version 3,
// which covers the main part of arduino-cli.
// The terms of this license can be found at:
// https://www.gnu.org/licenses/gpl-3.0.en.html
//
// You can be released from the requirements of the above licenses by purchasing
// a commercial license. Buying such a license is mandatory if you want to
// modify or otherwise use the software for commercial activities involving the
// Arduino software without disclosing the source code of your own applications.
// To purchase a commercial license, send an email to license@arduino.cc.

package config

// board_manager.additional_urls: []
// daemon.port: "50051"
// directories.data: /home/alien/.arduino15
// directories.downloads: /home/alien/.arduino15/staging
// directories.user: /home/alien/Arduino
// library.enable_unsafe_install: false
// logging.file: ""
// logging.format: text
// logging.level: info
// sketch.always_export_binaries: false
// telemetry.addr: :9090
// telemetry.enabled: true

var validMap = map[string]interface{}{
	"board_manager.additional_urls": []string{},
	"daemon.port":                   "",
	"directories.data":              "",
	"directories.downloads":         "",
	"directories.user":              "",
	"library.enable_unsafe_install": true,
	"logging.file":                  "",
	"logging.format":                "",
	"logging.level":                 "",
	"sketch.always_export_binaries": true,
	"telemetry.addr":                "",
	"telemetry.enabled":             true,
}

// func validate(key string, expectedType interface{}) error {
// 	t, ok := validMap[key]
// 	if !ok {
// 		return fmt.Errorf("DISASTAH")
// 	}

// 	return nil
// }
