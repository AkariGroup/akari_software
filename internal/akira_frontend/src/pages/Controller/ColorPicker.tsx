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
  const [cell] = useState<HTMLElement | null>(null);
  const handleChangeComplete = (value: ColorResult) => {
    setColor(value.hex);
    if (cell !== null) cell.style.backgroundColor = value.hex;
  };
  return (
    <PopupState variant="popover" popupId="demo-popup-popover">
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
            <SketchPicker
              color={color}
              onChange={handleChange}
              onChangeComplete={handleChangeComplete}
            />
          </Popover>
        </div>
      )}
    </PopupState>
  );
}
