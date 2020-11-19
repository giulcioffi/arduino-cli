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

import (
	"os"
	"strconv"

	"github.com/arduino/arduino-cli/cli/errorcodes"
	"github.com/arduino/arduino-cli/cli/feedback"
	"github.com/arduino/arduino-cli/configuration"
	"github.com/spf13/cobra"
)

func initSetCommand() *cobra.Command {
	addCommand := &cobra.Command{
		Use:   "set",
		Short: "Sets a settings value.",
		Long:  "Sets a settings value.",
		Example: "" +
			"  " + os.Args[0] + " config set logging.level trace\n" +
			"  " + os.Args[0] + " config set logging.file my-log.txt\n" +
			"  " + os.Args[0] + " config set sketch.always_export_binaries true",
		Args: cobra.ExactArgs(2),
		Run:  runSetCommand,
	}
	return addCommand
}

func runSetCommand(cmd *cobra.Command, args []string) {
	key := args[0]
	t, ok := validMap[key]
	if !ok {
		// TODO: Better error
		feedback.Errorf("Setting doesn't exist")
		os.Exit(errorcodes.ErrGeneric)
	}

	var value interface{}
	switch t.(type) {
	case []string:
		feedback.Errorf("%v is not of type %T", key, t)
		os.Exit(errorcodes.ErrGeneric)
	case string:
		value = args[1]
	case int:
		var err error
		value, err = strconv.Atoi(args[1])
		if err != nil {
			feedback.Errorf("error parsing value: %v", err)
			os.Exit(errorcodes.ErrGeneric)
		}
	case bool:
		var err error
		value, err = strconv.ParseBool(args[1])
		if err != nil {
			feedback.Errorf("error parsing value: %v", err)
			os.Exit(errorcodes.ErrGeneric)
		}
	}

	configuration.Settings.Set(key, value)

	if err := configuration.Settings.WriteConfig(); err != nil {
		// TODO: Better error
		feedback.Errorf("Writing config file: %v", err)
		os.Exit(errorcodes.ErrGeneric)
	}
}
