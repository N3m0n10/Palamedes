package main

import (
	"github.com/hajimehoshi/ebiten/v2"
	"image/color"
)

// Configurações do jogo
const (
	screenWidth  = 640
	screenHeight = 480
	paddleSpeed  = 6
	ballSpeed    = 4
)

// Estrutura do jogo
type Game struct {
	paddleX float64 // Posição X do paddle
	ballX   float64 // Posição X da bola
	ballY   float64 // Posição Y da bola
	ballDX  float64 // Direção X da bola (-1 ou 1)
	ballDY  float64 // Direção Y da bola (-1 ou 1)
	bricks  []Brick // Lista de tijolos
	score   int     // Pontuação
}

// Estrutura de um tijolo
type Brick struct {
	x      float64
	y      float64
	active bool
}

// Inicializar o jogo
func NewGame() *Game {
	g := &Game{
		paddleX: screenWidth/2 - 40, // Centralizar paddle
		ballX:   screenWidth / 2,
		ballY:   screenHeight - 30,
		ballDX:  1,
		ballDY:  -1,
	}

	// Criar tijolos
	for y := 50; y < 150; y += 20 {
		for x := 50; x < screenWidth-50; x += 60 {
			g.bricks = append(g.bricks, Brick{x: float64(x), y: float64(y), active: true})
		}
	}

	return g
}

// Atualizar a lógica do jogo
func (g *Game) Update() error {
	// Movimento do paddle (teclas ← e →)
	if ebiten.IsKeyPressed(ebiten.KeyArrowLeft) && g.paddleX > 0 {
		g.paddleX -= paddleSpeed
	}
	if ebiten.IsKeyPressed(ebiten.KeyArrowRight) && g.paddleX < screenWidth-80 {
		g.paddleX += paddleSpeed
	}

	// Movimento da bola
	g.ballX += ballSpeed * g.ballDX
	g.ballY += ballSpeed * g.ballDY

	// Colisão com as paredes
	if g.ballX <= 0 || g.ballX >= screenWidth-8 {
		g.ballDX *= -1
	}
	if g.ballY <= 0 {
		g.ballDY *= -1
	}

	// Colisão com o paddle
	if g.ballY >= screenHeight-20 && g.ballX >= g.paddleX && g.ballX <= g.paddleX+80 {
		g.ballDY *= -1
	}

	// Colisão com os tijolos
	for i := range g.bricks {
		brick := &g.bricks[i]
		if brick.active &&
			g.ballX >= brick.x && g.ballX <= brick.x+50 &&
			g.ballY >= brick.y && g.ballY <= brick.y+10 {
			brick.active = false
			g.ballDY *= -1
			g.score += 10
		}
	}

	// Resetar se a bola cair
	if g.ballY >= screenHeight {
		g.ballX = screenWidth / 2
		g.ballY = screenHeight - 30
		g.ballDX = 1
		g.ballDY = -1
	}

	return nil
}

// Desenhar os elementos na tela
func (g *Game) Draw(screen *ebiten.Image) {
	// Fundo
	screen.Fill(color.RGBA{0, 0, 0, 255})

	// Paddle
	paddle := ebiten.NewImage(80, 10)
	paddle.Fill(color.RGBA{255, 255, 255, 255})
	op := &ebiten.DrawImageOptions{}
	op.GeoM.Translate(g.paddleX, screenHeight-20)
	screen.DrawImage(paddle, op)

	// Bola
	ball := ebiten.NewImage(8, 8)
	ball.Fill(color.RGBA{255, 0, 0, 255})
	op = &ebiten.DrawImageOptions{}
	op.GeoM.Translate(g.ballX, g.ballY)
	screen.DrawImage(ball, op)

	// Tijolos
	brickImg := ebiten.NewImage(50, 10)
	brickImg.Fill(color.RGBA{0, 255, 0, 255})
	for _, brick := range g.bricks {
		if brick.active {
			op := &ebiten.DrawImageOptions{}
			op.GeoM.Translate(brick.x, brick.y)
			screen.DrawImage(brickImg, op)
		}
	}
}

// Configurações da janela
func (g *Game) Layout(outsideWidth, outsideHeight int) (int, int) {
	return screenWidth, screenHeight
}

// Função principal
func main() {
	ebiten.SetWindowSize(screenWidth, screenHeight)
	ebiten.SetWindowTitle("Breakout Game")
	if err := ebiten.RunGame(NewGame()); err != nil {
		panic(err)
	}
}
