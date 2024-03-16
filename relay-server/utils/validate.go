package utils

import (
	"net/url"

	"github.com/oklog/ulid/v2"
)

func IsValidURL(u string) bool {
	_, err := url.ParseRequestURI(u)
	return err == nil
}

func IsULID(str string) bool {
	_, err := ulid.Parse(str)
	return err == nil
}
