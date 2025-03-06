
import React, {useEffect, useState} from 'react';
import {ComponentProps, Streamlit, withStreamlitConnection} from "./streamlit";
import {fabric} from 'fabric';

interface PythonArgs {
    canvasWidth: number
    canvasHeight: number
    rectTop: number
    rectLeft: number
    rectWidth: number
    rectHeight: number
    realtimeUpdate: boolean
    boxColor: string
    strokeWidth: number
    imageData: Uint8ClampedArray
    lockAspect: boolean
}

const StreamlitCropper = (props: ComponentProps) => {
    const [canvas, setCanvas] = useState(new fabric.Canvas(""))
    const {canvasWidth, canvasHeight, imageData}: PythonArgs = props.args

    // Create an off-screen canvas and convert imageData to a data URL
    var invisCanvas = document.createElement("canvas")
    var ctx = invisCanvas.getContext('2d')
    invisCanvas.width = canvasWidth
    invisCanvas.height = canvasHeight

    if (ctx) {
      var idata = ctx.createImageData(canvasWidth, canvasHeight);
      idata.data.set(imageData);
      ctx.putImageData(idata, 0, 0);
      var dataUri = invisCanvas.toDataURL()
    } else {
      var dataUri = ""
    }
    
    /**
     * Initialize canvas on mount and add a rectangle
     */
    useEffect(() => {
        const {rectTop, rectLeft, rectWidth, rectHeight, boxColor, strokeWidth, lockAspect}: PythonArgs = props.args
        const canvas = new fabric.Canvas('c', {
            enableRetinaScaling: false,
            backgroundImage: dataUri,
            uniScaleTransform: lockAspect
        })

        var rect = new fabric.Rect({
            left: rectLeft,
            top: rectTop,
            fill: '',
            width: rectWidth,
            height: rectHeight,
            objectCaching: true,
            stroke: boxColor,
            strokeWidth: strokeWidth,
            hasRotatingPoint: false
        });
        canvas.add(rect)

        setCanvas(canvas)
        Streamlit.setFrameHeight()
    }, [canvasHeight, canvasWidth]);

    /**
     * On update (either realtime or doubleclick), send the coordinates of the rectangle
     * back to streamlit, adjusting to remove the stroke width.
     */
    useEffect(() => {
        const {realtimeUpdate}: PythonArgs = props.args
        if (!canvas) return;
        
        const handleEvent = () => {
            canvas.renderAll();
            const rectObj = canvas.getObjects()[0];
            const bounds = rectObj.getBoundingRect();
            const stroke = rectObj.strokeWidth || 0;
            // Adjust coordinates: since stroke is drawn centered, subtract full stroke from width/height.
            const adjustedCoords = {
              left: bounds.left,
              top: bounds.top,
              width: bounds.width - stroke,
              height: bounds.height - stroke
            };
            Streamlit.setComponentValue({coords: adjustedCoords});
        }
        
        if (realtimeUpdate) {
            canvas.on("object:modified", handleEvent)
            return () => {
                canvas.off("object:modified", handleEvent);
            }
        } else {
            canvas.on("mouse:dblclick", handleEvent)
            return () => {
                canvas.off("mouse:dblclick", handleEvent);
            }
        }
    })

    return (
        <>
            <canvas id="c" width={canvasWidth} height={canvasHeight}/>
        </>
    )
};

export default withStreamlitConnection(StreamlitCropper);


