package application_models_domain

import (
	"encoding/base64"
	"errors"
	"strings"
)

type Application struct {
	id        string
	secretKey string
}

func NewApplication(
	id string,
	secretKey string,
) *Application {
	return &Application{
		id:        id,
		secretKey: secretKey,
	}
}

func (a *Application) GetId() string {
	return a.id
}

func (a *Application) GetSecretKey() string {
	return a.secretKey
}

type ApplicationFactory struct{}

func (af *ApplicationFactory) Create(
	header string,
) (*Application, error) {
	authParts := strings.Fields(header)
	if len(authParts) != 2 || authParts[0] != "Basic" {
		return nil, errors.New("invalid authorization header")
	}

	// base64エンコードされた文字列をデコード
	decodedBytes, err := base64.StdEncoding.DecodeString(authParts[1])
	if err != nil {
		return nil, errors.New("failed to decode authorization header")
	}

	// デコードされた文字列を ":" で分割してユーザー名とパスワードを取得
	credentials := strings.SplitN(string(decodedBytes), ":", 2)
	if len(credentials) != 2 {
		return nil, errors.New("invalid authorization header")
	}

	appId := credentials[0]
	secretKey := credentials[1]

	return NewApplication(appId, secretKey), nil

}
