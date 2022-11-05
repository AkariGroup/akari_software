import { Button, Popover } from "@mui/material";
import { useState } from "react";
import { SketchPicker } from "react-color";
import { ColorResult } from "react-color";
import PopupState, { bindTrigger, bindPopover } from "material-ui-popup-state";

export function ColorPicker() {
  const [color, setColor] = useState("#333");
  const handleChange = (value: ColorResult) => {
    setColor(value.hex);
  };
  return (
    <PopupState variant="popover">
      {(popupState) => (
        <div>
          <Button
            style={{ backgroundColor: color }}
            variant="contained"
            {...bindTrigger(popupState)}
          >
            Choose Display Color
          </Button>
          <Popover {...bindPopover(popupState)}>
            <SketchPicker color={color} onChange={handleChange} />
          </Popover>
        </div>
      )}
    </PopupState>
  );
}
