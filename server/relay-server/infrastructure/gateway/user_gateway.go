package gateway

import (
	"encoding/json"
	"os"

	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	common_gateway "github.com/kajiLabTeam/xr-project-relay-server/infrastructure/gateway/common"
	user_record "github.com/kajiLabTeam/xr-project-relay-server/infrastructure/record/user"
)

type UserGateway struct{}

func (ug *UserGateway) Save(
	saveReq *user_record.SaveRequest,
	a *application_models_domain.Application,
) (*user_record.SaveResponse, error) {
	endpoint := os.Getenv("AUTHENTICATION_SERVER_URL") + "/api/user/create"

	req := common_gateway.NewRequest(a)

	resBody, err := req.MakeApplicationJsonRequest(
		endpoint,
		saveReq,
	)
	if err != nil {
		return nil, err
	}
	// 404エラーの場合
	if resBody == nil {
		return nil, nil
	}

	var saveRes user_record.SaveResponse
	err = json.Unmarshal(resBody, &saveRes)
	if err != nil {
		return nil, err
	}

	return &saveRes, nil
}
