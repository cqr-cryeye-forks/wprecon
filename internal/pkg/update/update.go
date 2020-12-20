package update

import (
	"encoding/json"

	version "github.com/blackcrw/wprecon/internal/pkg/version"
	"github.com/blackcrw/wprecon/pkg/gohttp"
	"github.com/blackcrw/wprecon/pkg/printer"
)

type githubAPIJSON struct {
	Author struct {
		Name        string `json:"name"`
		Description string `json:"description"`
		Email       string `json:"email"`
	} `json:"Author"`
	App struct {
		Description     string `json:"description"`
		Version         string `json:"version"`
		VersionReselase string `json:"version-reselase"`
	} `json:"App"`
}

// CheckUpdate :: This function will be responsible for checking and printing on the screen whether there is an update or not.
func CheckUpdate() {
	var githubJSON githubAPIJSON

	printer.Loading("Checking Version!")

	options := &gohttp.HTTPOptions{
		URL: gohttp.URLOptions{
			Simple: "https://raw.githubusercontent.com/blackcrw/wprecon/dev/internal/config/config.json",
		},
	}

	request, err := gohttp.HTTPRequest(options)

	if err != nil {
		printer.Fatal("Error checking for an update (", err, ")")
	}

	err = json.NewDecoder(request.Body).Decode(&githubJSON)

	if err != nil {
		printer.LoadingDanger("An error occurred while trying to check the version.")
	} else if githubJSON.App.Version != version.Version {
		printer.LoadingDone("There is a new version!", "New:", githubJSON.App.Version, "Download: https://github.com/blackcrw/wprecon")
	} else {
		printer.LoadingWarning("You have the most updated version.")
	}
}
