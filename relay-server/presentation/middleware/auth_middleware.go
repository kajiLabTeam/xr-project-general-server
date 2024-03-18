package middleware

import (
	"net/http"
	"os"
	"strings"

	"github.com/gin-gonic/gin"
)

func AuthMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		endpoint := os.Getenv("APPLICATION_AUTHENTICATION_SERVER_URL") + "/api/application/auth"
		headerValue := c.GetHeader("Authorization")

		authParts := strings.Fields(headerValue)
		if len(authParts) != 2 || authParts[0] != "Basic" {
			c.Abort()
		}

		request, err := http.NewRequest("GET", endpoint, nil)
		if err != nil {
			c.Abort()
		}

		request.Header.Set("Authorization", headerValue)

		client := &http.Client{}
		response, err := client.Do(request)
		if err != nil {
			c.Abort()
		}
		if response.StatusCode != http.StatusOK {
			c.Abort()
		}

		c.Next()
	}
}
