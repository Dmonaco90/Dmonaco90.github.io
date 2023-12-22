document.addEventListener("DOMContentLoaded", function() {
    var drawingCanvas = document.getElementById('drawingCanvas');
    var gridCanvas = document.getElementById('gridCanvas');
    var drawingContext = drawingCanvas.getContext('2d');
    var gridContext = gridCanvas.getContext('2d');
    var shapeSelector = document.getElementById('shapeSelector');
    var clearButton = document.getElementById('clearCanvas');
    var start = null;
    var isDrawing = false;
    var shapes = []; // Array per memorizzare le forme disegnate
    var unitSelector = document.getElementById('unitSelector');
    var currentUnit = unitSelector.value; // Prende il valore iniziale selezionato
    var scaleFactor = currentUnit === 'mm' ? 3.8 : 38; // 3.8 pixel per mm, 38 pixel per cm
    var lineButton = document.getElementById('lineButton');
    var rectangleButton = document.getElementById('rectangleButton');
    var squareButton = document.getElementById('squareButton');
    var circleButton = document.getElementById('circleButton');
    var contentDisplayCanvas = document.getElementById('contentDisplayCanvas');
    var contentDisplayContext = contentDisplayCanvas.getContext('2d');
    var inputContainer = document.getElementById('manualInputs');


    function drawShapeInDisplay(shape, numSides) {
        var canvasWidth = contentDisplayCanvas.width;
        var canvasHeight = contentDisplayCanvas.height;
        var shapeSize = 38 * 5; // Ad esempio, 5 cm
        var margin = 10; // Margine dal lato sinistro del canvas per la forma
    
        contentDisplayContext.clearRect(0, 0, canvasWidth, canvasHeight);
    
        // Disegna la sezione per la forma (70% del canvas)
        contentDisplayContext.fillStyle = 'blue'; // Colore di riempimento per la forma
        contentDisplayContext.strokeStyle = 'black'; // Colore del contorno per la forma
        var shapeSectionWidth = canvasWidth * 0.7; // 70% della larghezza del canvas
    
        var startX = margin;
        var centerY = canvasHeight / 2;
        var startY = centerY - shapeSize / 2;
    
        contentDisplayContext.beginPath();
        switch (shape) {
            case 'square':
                contentDisplayContext.rect(startX, startY, shapeSize, shapeSize);
                break;
            case 'circle':
                var radius = shapeSize / 2;
                contentDisplayContext.arc(startX + radius, centerY, radius, 0, 2 * Math.PI);
                break;
            // Aggiungi altri casi se necessario
        }
        contentDisplayContext.fill();
        contentDisplayContext.stroke();
    
       
    
        createInputBoxes(numSides);
    }
    
    
    function displayMeasurements(measurements, startX, startY, shapeSize) {
        var textOffset = 10; // Distanza del testo dal bordo della forma
        var additionalOffset = 80; // Offset aggiuntivo se la forma non è centrata nel div
    
        var textPositions = [
            { x: startX + shapeSize / 2 - additionalOffset, y: startY - textOffset }, // Top side
            { x: startX + shapeSize + textOffset - additionalOffset, y: startY + shapeSize / 2 }, // Right side
            { x: startX + shapeSize / 2 - additionalOffset, y: startY + shapeSize + textOffset }, // Bottom side
            { x: startX - textOffset - additionalOffset, y: startY + shapeSize / 2 } // Left side
        ];
    
        contentDisplayContext.font = "12px Arial";
        contentDisplayContext.fillStyle = "black";
    
        measurements.forEach((measure, index) => {
            if (measure) { // Verifica se la misura è stata inserita
                contentDisplayContext.fillText(measure + " cm", textPositions[index].x, textPositions[index].y);
            }
        });
    }
    
    
    
    function createInputBoxes(numSides, startX, startY, shapeSize) {
        var manualInputs = document.getElementById('manualInputs');
        manualInputs.innerHTML = '';
        var measurements = new Array(numSides).fill(''); // Inizializza l'array con stringhe vuote
    
        for (let i = 0; i < numSides; i++) {
            let input = document.createElement('input');
            input.type = 'number';
            input.placeholder = 'Lunghezza ' + (i + 1);
    
            input.addEventListener('change', function() {
                measurements[i] = input.value;
                displayMeasurements(measurements, startX, startY, shapeSize);
            });
    
            manualInputs.appendChild(input);
        }
    }
    
    
    

     // Aggiungi gli event listener ai pulsanti per disegnare le forme
    document.getElementById('lineButton').addEventListener('click', function() {
        drawShapeInDisplay('line');
    });
    document.getElementById('lineButtonStandard').addEventListener('click', function() {
        drawShapeInDisplay('line');
    });
    document.getElementById('lineButtonManuale').addEventListener('click', function() {
        drawShapeInDisplay('line');
    });
     // Aggiungi gli event listener ai pulsanti per disegnare le forme
     document.getElementById('squareButton').addEventListener('click', function() {
        drawShapeInDisplay('line');
    });
    document.getElementById('squareButtonStandard').addEventListener('click', function() {
        drawShapeInDisplay('line');
    });
    document.getElementById('squareButtonManuale').addEventListener('click', function() {
        var canvasWidth = contentDisplayCanvas.width;
        var canvasHeight = contentDisplayCanvas.height;
        var shapeSize = 38 * 5; // 5 cm
        var margin = 80; // Margine dal lato sinistro del canvas
        var centerY = canvasHeight / 2;
        var startY = centerY - shapeSize / 2; // Centra verticalmente
    
        drawShapeInDisplay('square', 4);
        createInputBoxes(4, margin, startY, shapeSize); // Aggiungi i parametri qui
    });

    lineButton.addEventListener('click', function() {
        shapeSelector.value = 'line';
    });

    rectangleButton.addEventListener('click', function() {
        shapeSelector.value = 'rectangle';
    });

    squareButton.addEventListener('click', function() {
        shapeSelector.value = 'square';
    });

    circleButton.addEventListener('click', function() {
        shapeSelector.value = 'circle';
    });

    unitSelector.addEventListener('change', function() {
        currentUnit = unitSelector.value;
        scaleFactor = currentUnit === 'mm' ? 3.8 : 38;
        redrawCanvas();
    });

    drawGrid(gridContext, gridCanvas.width, gridCanvas.height);

    drawingCanvas.addEventListener('mousedown', function(e) {
        start = getMousePosition(drawingCanvas, e);
        isDrawing = true;
    });

    drawingCanvas.addEventListener('mousemove', function(e) {
        if (isDrawing) {
            var currentPos = getMousePosition(drawingCanvas, e);
            redrawCanvas(); // Ridisegna il canvas con tutte le forme memorizzate
            drawShape(drawingContext, shapeSelector.value, start.x, start.y, currentPos.x, currentPos.y); // Disegna l'anteprima
    
            // Calcolo e visualizzazione della misura in tempo reale
            var realTimeMeasurement = calculateMeasurement(shapeSelector.value, start.x, start.y, currentPos.x, currentPos.y, scaleFactor);
            showMeasurement(drawingContext, realTimeMeasurement, start.x, start.y, currentPos.x, currentPos.y);
        }
    });

    drawingCanvas.addEventListener('mouseup', function(e) {
        if (isDrawing) {
            var endPos = getMousePosition(drawingCanvas, e);
            var shapeDetails = {
                shape: shapeSelector.value,
                startX: start.x,
                startY: start.y,
                endX: endPos.x,
                endY: endPos.y,
                measurement: calculateMeasurement(shapeSelector.value, start.x, start.y, endPos.x, endPos.y, scaleFactor)
            };
            shapes.push(shapeDetails);
            redrawCanvas();
            isDrawing = false;
        }
    });

    clearButton.addEventListener('click', function() {
        shapes = []; // Resetta l'array delle forme
        redrawCanvas();
    });

    function redrawCanvas() {
        clearCanvas(drawingContext, drawingCanvas); // Pulisci il canvas
        drawGrid(gridContext, gridCanvas.width, gridCanvas.height); // Ridisegna la griglia
        shapes.forEach(shape => {
            drawShape(drawingContext, shape.shape, shape.startX, shape.startY, shape.endX, shape.endY);
            showMeasurement(drawingContext, shape.measurement, shape.startX, shape.startY, shape.endX, shape.endY);
        });
    }


    function drawGrid(context, width, height) {
        var gridSpacing = 38; // Ad esempio, 1 cm su un display 96 DPI
        context.strokeStyle = '#e0e0e0';
        for(var x = 0; x <= width; x += gridSpacing) {
            context.beginPath();
            context.moveTo(x, 0);
            context.lineTo(x, height);
            context.stroke();
        }
        for(var y = 0; y <= height; y += gridSpacing) {
            context.beginPath();
            context.moveTo(0, y);
            context.lineTo(width, y);
            context.stroke();
        }
    }

    function getMousePosition(canvas, e) {
        var rect = canvas.getBoundingClientRect();
        return {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };
    }

    function clearCanvas(context, canvas) {
        context.clearRect(0, 0, canvas.width, canvas.height);
    }

    function calculateMeasurement(shape, startX, startY, endX, endY, scaleFactor) {
        var width = Math.abs(endX - startX) / scaleFactor;
        var height = Math.abs(endY - startY) / scaleFactor;

        switch(shape) {
            case 'line':
                var length = Math.sqrt(Math.pow(width, 2) + Math.pow(height, 2)).toFixed(2);
                return length + (currentUnit === 'mm' ? ' mm' : ' cm');
            case 'rectangle':
            case 'square':
                return {
                    width: width.toFixed(2) + (currentUnit === 'mm' ? ' mm' : ' cm'),
                    height: height.toFixed(2) + (currentUnit === 'mm' ? ' mm' : ' cm')
                };
            case 'circle':
                var radius = Math.sqrt(Math.pow(width, 2) + Math.pow(height, 2)) / 2;
                return (radius * 2).toFixed(2) + (currentUnit === 'mm' ? ' mm' : ' cm');
        }
    }

    function showMeasurement(context, measurement, startX, startY, endX, endY) {
        context.font = "12px Arial";
        context.fillStyle = "black";

        if (typeof measurement === 'string') {
            context.fillText(measurement, (startX + endX) / 2, (startY + endY) / 2);
        } else if (typeof measurement === 'object') {
            context.fillText(measurement.width, endX, startY - 10);
            context.fillText(measurement.height, endX + 10, endY);
        }
    }

    function drawShape(context, shape, startX, startY, endX, endY) {
        context.beginPath();
        switch (shape) {
            case 'line':
                context.moveTo(startX, startY);
                context.lineTo(endX, endY);
                break;
            case 'rectangle':
                context.rect(startX, startY, endX - startX, endY - startY);
                break;
            case 'square':
                var sideLength = Math.min(Math.abs(endX - startX), Math.abs(endY - startY));
                context.rect(startX, startY, sideLength, sideLength);
                break;
            case 'circle':
                var radius = Math.sqrt(Math.pow(endX - startX, 2) + Math.pow(endY - startY, 2)) / 2;
                context.arc(startX, startY, radius, 0, Math.PI * 2);
                break;
        }
        context.stroke();
    }
});
