//Setupfunktion
function setup(){
	XValues = []
	YValues = []
	createCanvas(windowWidth*0.99,windowHeight*0.98)
	rectMode(CENTER)
	show()
}

//Showfunktion
function show(){
	r = Math.floor(Math.random()*255)
	g = Math.floor(Math.random()*255)
	b = Math.floor(Math.random()*255)
	background(r,g,b)
	textSize(200)
	fill(255)
	text('White',width*0.1,height/2)
	fill(0)
	text('Black',width*0.6,height/2)
}

//neue Farbe "MOUSECLICK"
function mouseClicked(){
	if (mouseX < width/2){
		p = 1
	}
	else {
		p = 0
	}
	sample = [r/255,g/255,b/255]
	XValues.push(sample)
	YValues.push(p)
	//Aufruf Showfunktion
	show()
}

function keyPressed(){
	//Output jetziger Farbe "SPACE"
	if (keyCode == 32){
		console.log('[['+[r,g,b].join('],[')+']]')
		window.alert('[['+[r,g,b].join('],[')+']]')
	}
	//Output Sample "P"
	if (keyCode == 80){
		console.log('[['+XValues.join('],[')+']]')
		window.alert('[['+XValues.join('],[')+']]')
		console.log('[['+YValues.join(',')+']]')
		window.alert('[['+YValues.join(',')+']]')
	}
	//Reset Sample "R"
	if (keyCode == 82){
		XValues = []
		YValues = []
	}
}
