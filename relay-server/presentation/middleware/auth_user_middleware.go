package middleware

import (
	"bytes"
	"encoding/json"
	"net/http"
	"os"
)

func AuthUserMiddleware(
	header string,
	userId string,
) error {
	endpoint := os.Getenv("AUTHENTICATION_SERVER_URL") + "/api/user/auth"

	userReq := struct {
		Id string `json:"id"`
	}{
		Id: userId,
	}

	jsonData, err := json.Marshal(userReq)
	if err != nil {
		return err
	}

	request, err := http.NewRequest("POST", endpoint, bytes.NewBuffer(jsonData))
	if err != nil {
		return err
	}

	request.Header.Set("Authorization", header)

	client := &http.Client{}
	response, err := client.Do(request)
	if err != nil {
		return err
	}
	if response.StatusCode == http.StatusUnauthorized {
		return nil
	}

	return nil
}
