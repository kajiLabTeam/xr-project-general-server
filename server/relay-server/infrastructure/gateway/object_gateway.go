package gateway

import (
	"encoding/json"
	"os"

	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	common_gateway "github.com/kajiLabTeam/xr-project-relay-server/infrastructure/gateway/common"
	object_record "github.com/kajiLabTeam/xr-project-relay-server/infrastructure/record/object"
)

type ObjectGateway struct{}

func (og ObjectGateway) FindForSpotId(
	findForSpotIdReq *object_record.FindForSpotIdRequest,
	application *application_models_domain.Application,
) (*object_record.FindForSpotIdResponse, error) {
	endpoint := os.Getenv("OBJECT_SERVER_URL") + "/api/object/get"

	request := common_gateway.NewRequest(application)

	responseBody, err := request.MakeApplicationJsonRequest(
		endpoint,
		findForSpotIdReq,
	)
	if err != nil {
		return nil, err
	}
	// 404エラーの場合
	if responseBody == nil {
		return nil, nil
	}

	var findForSpotIdRes object_record.FindForSpotIdResponse
	err = json.Unmarshal(responseBody, &findForSpotIdRes)
	if err != nil {
		return nil, err
	}

	return &findForSpotIdRes, nil
}

func (og ObjectGateway) FindForSpotIds(
	FindForSpotIdAndRawDataReq *object_record.FindForSpotIdsRequest,
	a *application_models_domain.Application,
) (*object_record.FindForObjectBySpotIAndRawDataFiledResponse, error) {
	endpoint := os.Getenv("OBJECT_SERVER_URL") + "/api/object/collection/get"

	request := common_gateway.NewRequest(a)

	responseBody, err := request.MakeApplicationJsonRequest(
		endpoint,
		FindForSpotIdAndRawDataReq,
	)
	if err != nil {
		return nil, err
	}
	// 404エラーの場合
	if responseBody == nil {
		return nil, nil
	}

	var findForSpotIdAndRawDataRes object_record.FindForObjectBySpotIAndRawDataFiledResponse
	err = json.Unmarshal(responseBody, &findForSpotIdAndRawDataRes)
	if err != nil {
		return nil, err
	}

	return &findForSpotIdAndRawDataRes, nil
}

func (og ObjectGateway) Save(
	saveRequest *object_record.SaveRequest,
	a *application_models_domain.Application,
) (*object_record.SaveResponse, error) {
	endpoint := os.Getenv("OBJECT_SERVER_URL") + "/api/object/create"

	request := common_gateway.NewRequest(a)

	resBody, err := request.MakeApplicationJsonRequest(
		endpoint,
		saveRequest,
	)
	if err != nil {
		return nil, err
	}
	// 404エラーの場合
	if resBody == nil {
		return nil, nil
	}

	var createObjectRes object_record.SaveResponse
	err = json.Unmarshal(resBody, &createObjectRes)
	if err != nil {
		return nil, err
	}

	return &createObjectRes, nil
}
