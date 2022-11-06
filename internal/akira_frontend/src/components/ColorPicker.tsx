import { Button, Popover } from "@mui/material";
import { RGBColor, SketchPicker } from "react-color";
import { ColorResult } from "react-color";
import PopupState, { bindTrigger, bindPopover } from "material-ui-popup-state";

type Props = {
  text?: string;
  color: RGBColor;
  onChangeColor: (c: RGBColor) => void;
};

export function ColorPicker(props: Props) {
  const handleChange = (value: ColorResult) => {
    props.onChangeColor(value.rgb);
  };
  return (
    <PopupState variant="popover">
      {(popupState) => (
        <div>
          <Button
            style={{
              backgroundColor: `rgb(${props.color.r}, ${props.color.g}, ${props.color.b})`,
            }}
            variant="contained"
            {...bindTrigger(popupState)}
          >
            {props.text ?? "Choose Color"}
          </Button>
          <Popover {...bindPopover(popupState)}>
            <SketchPicker
              color={props.color}
              onChange={handleChange}
              disableAlpha
            />
          </Popover>
        </div>
      )}
    </PopupState>
  );
}
