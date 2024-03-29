package common_gateway

import (
	"bytes"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"strconv"

	application_models_domain "github.com/kajiLabTeam/xr-project-relay-server/domain/models/application"
	spot_record "github.com/kajiLabTeam/xr-project-relay-server/infrastructure/record/spot"
)

type AnyStructType interface{}

type Request struct {
	body        *bytes.Buffer
	writer      *multipart.Writer
	application *application_models_domain.Application
}

func NewRequest(a *application_models_domain.Application) *Request {
	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)
	return &Request{
		body:        body,
		writer:      writer,
		application: a,
	}
}

func (r *Request) GetBody() *bytes.Buffer {
	return r.body
}

func (r *Request) AddFindSpotForIdsAndRawDataFileRequest(fieldName string, fileName string, file []byte) error {
	fileWriter, err := r.writer.CreateFormFile(fieldName, fileName)
	if err != nil {
		return err
	}

	_, err = io.Copy(fileWriter, bytes.NewReader(file))
	if err != nil {
		return err
	}

	if err := r.writer.Close(); err != nil {
		return err
	}

	return nil
}

func (r *Request) AddSaveSpotRequest(
	fieldName string,
	fileName string,
	file []byte,
	sr *spot_record.SaveRequest,
) error {
	fileWriter, err := r.writer.CreateFormFile(fieldName, fileName)
	if err != nil {
		return err
	}

	_, err = io.Copy(fileWriter, bytes.NewReader(file))
	if err != nil {
		return err
	}

	if err := r.writer.WriteField("name", sr.Name); err != nil {
		return err
	}
	if err := r.writer.WriteField("floor", strconv.Itoa(sr.Floor)); err != nil {
		return err
	}
	if err := r.writer.WriteField("locationType", sr.LocationType); err != nil {
		return err
	}
	if err := r.writer.WriteField("latitude", fmt.Sprintf("%f", sr.Latitude)); err != nil {
		return err
	}
	if err := r.writer.WriteField("longitude", fmt.Sprintf("%f", sr.Longitude)); err != nil {
		return err
	}

	if err := r.writer.Close(); err != nil {
		return err
	}

	return nil
}

func (r *Request) MakeApplicationJsonRequest(endpoint string, req AnyStructType) ([]byte, error) {
	jsonData, err := json.Marshal(req)
	if err != nil {
		return nil, err
	}

	request, err := http.NewRequest("POST", endpoint, bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, err
	}

	base64EncodedHeader := base64.StdEncoding.EncodeToString([]byte(r.application.GetId() + ":" + r.application.GetSecretKey()))
	request.Header.Set("Authorization", "Basic "+base64EncodedHeader)
	request.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	response, err := client.Do(request)
	if err != nil {
		return nil, err
	}
	if response.StatusCode == http.StatusNotFound {
		return nil, nil
	}
	defer response.Body.Close()

	responseBody, err := io.ReadAll(response.Body)
	if err != nil {
		return nil, err
	}

	return responseBody, nil
}

func (r *Request) MakeMultipartRequest(endpoint string) ([]byte, error) {
	base64EncodedHeader := base64.StdEncoding.EncodeToString([]byte(r.application.GetId() + ":" + r.application.GetSecretKey()))

	request, err := http.NewRequest("POST", endpoint, r.GetBody())
	if err != nil {
		return nil, err
	}

	request.Header.Set("Authorization", "Basic "+base64EncodedHeader)
	request.Header.Set("Content-Type", r.writer.FormDataContentType())

	client := &http.Client{}
	response, err := client.Do(request)
	if err != nil {
		return nil, err
	}
	if response.StatusCode == http.StatusNotFound {
		return nil, nil
	}
	defer response.Body.Close()

	responseBody, err := io.ReadAll(response.Body)
	if err != nil {
		return nil, err
	}

	return responseBody, nil
}
