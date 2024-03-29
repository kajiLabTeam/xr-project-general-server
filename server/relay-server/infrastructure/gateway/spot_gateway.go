package gateway

import (
	"encoding/json"
	"os"
	"strconv"

	"github.com/kajiLabTeam/xr-project-relay-server/config"
	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	common_gateway "github.com/kajiLabTeam/xr-project-relay-server/infrastructure/gateway/common"
	spot_record "github.com/kajiLabTeam/xr-project-relay-server/infrastructure/record/spot"
)

type SpotGateway struct{}

func (sg *SpotGateway) FindForIdAndRawDataFile(
	spotId string,
	rawDataFile []byte,
	a *application_models_domain.Application,
) (*spot_record.FindForIdsAndRawDataFileResponse, error) {
	endpoint := os.Getenv("SPOT_ESTIMATION_SERVER_URL") + "/api/spot/search" + "?spotIds=" + spotId

	request := common_gateway.NewRequest(a)
	if err := request.AddFindSpotForIdsAndRawDataFileRequest(
		config.RAW_DATA_FILE_FIELD,
		config.RAW_DATA_FILE_NAME,
		rawDataFile,
	); err != nil {
		return nil, err
	}

	resBody, err := request.MakeMultipartRequest(
		endpoint,
	)
	if err != nil {
		return nil, err
	}
	// 404エラーの場合
	if resBody == nil {
		return nil, nil
	}

	var findForIdsAndRawDataFileResponse spot_record.FindForIdsAndRawDataFileResponse
	err = json.Unmarshal(resBody, &findForIdsAndRawDataFileResponse)
	if err != nil {
		return nil, err
	}

	return &findForIdsAndRawDataFileResponse, nil
}

func (sg *SpotGateway) FindForIdsAndRawDataFile(
	spotId []string,
	rawDataFile []byte,
	a *application_models_domain.Application,
) (*spot_record.FindForIdsAndRawDataFileResponse, error) {
	var query string
	for _, id := range spotId {
		query += "spotIds=" + id + "&"
	}

	endpoint := os.Getenv("SPOT_ESTIMATION_SERVER_URL") + "/api/spot/search" + "?" + query

	request := common_gateway.NewRequest(a)
	if err := request.AddFindSpotForIdsAndRawDataFileRequest(
		config.RAW_DATA_FILE_FIELD,
		config.RAW_DATA_FILE_NAME,
		rawDataFile,
	); err != nil {
		return nil, err
	}

	resBody, err := request.MakeMultipartRequest(
		endpoint,
	)
	if err != nil {
		return nil, err
	}
	// 404エラーの場合
	if resBody == nil {
		return nil, nil
	}

	var findForIdsAndRawDataFileResponse spot_record.FindForIdsAndRawDataFileResponse
	err = json.Unmarshal(resBody, &findForIdsAndRawDataFileResponse)
	if err != nil {
		return nil, err
	}

	return &findForIdsAndRawDataFileResponse, nil
}

func (sg *SpotGateway) FindForCoordinateAndRadius(
	radius int,
	findForCoordinateAndRadiusReq *spot_record.FindForCoordinateAndRadiusRequest,
	a *application_models_domain.Application,
) (*spot_record.FindForCoordinateAndRadiusResponse, error) {
	endpoint := os.Getenv("AREA_ESTIMATION_SERVER_URL") + "/api/area/search?radius=" + strconv.Itoa(radius)

	request := common_gateway.NewRequest(a)
	resBody, err := request.MakeApplicationJsonRequest(
		endpoint,
		findForCoordinateAndRadiusReq,
	)
	if err != nil {
		return nil, err
	}
	// 404エラーの場合
	if resBody == nil {
		return nil, nil
	}

	var findForCoordinateAndRadiusRes spot_record.FindForCoordinateAndRadiusResponse
	err = json.Unmarshal(resBody, &findForCoordinateAndRadiusRes)
	if err != nil {
		return nil, err
	}

	return &findForCoordinateAndRadiusRes, nil
}

func (sg *SpotGateway) Save(
	rawDataFile []byte,
	saveReq *spot_record.SaveRequest,
	a *application_models_domain.Application,
) (*spot_record.SaveResponse, error) {
	endpoint := os.Getenv("SPOT_ESTIMATION_SERVER_URL") + "/api/spot/create"

	req := common_gateway.NewRequest(a)
	if err := req.AddSaveSpotRequest(
		config.RAW_DATA_FILE_FIELD,
		config.RAW_DATA_FILE_NAME,
		rawDataFile,
		saveReq,
	); err != nil {
		return nil, err
	}

	resBody, err := req.MakeMultipartRequest(
		endpoint,
	)
	if err != nil {
		return nil, err
	}
	// 404エラーの場合
	if resBody == nil {
		return nil, nil
	}

	var saveRes spot_record.SaveResponse
	err = json.Unmarshal(resBody, &saveRes)
	if err != nil {
		return nil, err
	}

	return &saveRes, nil
}
