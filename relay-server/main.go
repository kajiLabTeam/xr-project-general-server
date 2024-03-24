package main

import (
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	"github.com/kajiLabTeam/xr-project-relay-server/presentation/handlers"
)

func main() {
	err := godotenv.Load(".env")
	if err != nil {
		panic(err)
	}

	r := gin.Default()

	handlers.CreateUserHandler(r)
	handlers.GetObjectBySpotHandler(r)
	handlers.GetObjectByAreaHandler(r)
	handlers.CreateObjectHandler(r)

	r.Run(":8000")
}
