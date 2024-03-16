package object_models_domain

type PreSignedUrl struct {
	value string
}

func NewPreSignedUrl(value *string) (*PreSignedUrl, error) {
	if value == nil {
		return nil, nil
	}
	return &PreSignedUrl{value: *value}, nil
}

func (psu *PreSignedUrl) GetValue() string {
	return psu.value
}
