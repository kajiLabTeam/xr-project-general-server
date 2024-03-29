package middleware

import (
	"io"
	"mime/multipart"
)

func GetBytesFromMultiPartFile(f *multipart.FileHeader) ([]byte, error) {
	src, err := f.Open()
	if err != nil {
		return nil, err
	}
	defer src.Close()

	buf, err := io.ReadAll(src)
	if err != nil {
		return nil, err
	}

	return buf, nil
}
