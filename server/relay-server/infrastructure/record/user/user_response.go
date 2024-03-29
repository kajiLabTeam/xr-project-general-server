package user_record

type SaveResponse struct {
	Id         string  `json:"id"`
	Name       string  `json:"name"`
	Email      string  `json:"email"`
	Gender     string  `json:"gender"`
	Age        int     `json:"age"`
	Height     float64 `json:"height"`
	Weight     float64 `json:"weight"`
	Occupation string  `json:"occupation"`
	Address    string  `json:"address"`
}
