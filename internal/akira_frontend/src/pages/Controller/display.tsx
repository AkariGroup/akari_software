import {
  Box,
  Button,
  Slider,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { useState } from "react";
import { RGBColor } from "react-color";
import { ColorPicker } from "../../components/ColorPicker";
import { AkiraControllerClient } from "./client";

const DEFAULT_FOREGROUND_COLOR: RGBColor = {
  r: 0,
  g: 0,
  b: 0,
};
const DEFAULT_DISPLAY_COLOR: RGBColor = {
  r: 255,
  g: 255,
  b: 255,
};

const DEFAULT_FONT_SIZE: number = 3;

type ColorSectionProps = {
  heading: string;
  color: RGBColor;
  onChangeColor: (c: RGBColor) => void;
};

function ColorSection(props: ColorSectionProps) {
  return (
    <Stack direction="row" alignItems="center" mr={1} mb={1}>
      <Typography>{props.heading}</Typography>
      &nbsp;
      <ColorPicker
        text="&nbsp;"
        color={props.color}
        onChangeColor={props.onChangeColor}
      />
    </Stack>
  );
}

type Props = {
  controllerClient: AkiraControllerClient;
};

export function DisplayPanel(props: Props) {
  const [foregroundColor, setForegroundColor] = useState<RGBColor>(
    () => DEFAULT_FOREGROUND_COLOR
  );
  const [displayColor, setDisplayColor] = useState<RGBColor>(
    () => DEFAULT_DISPLAY_COLOR
  );
  const [fontSize, setFontSize] = useState<number>(() => DEFAULT_FONT_SIZE);
  const [text, setText] = useState<string>("");

  const onSubmit = async () => {
    await props.controllerClient.display.values.post({
      body: {
        text: text,
        display_color: displayColor,
        foreground_color: foregroundColor,
        font_size: fontSize,
      },
    });
  };
  const onReset = () => {
    setForegroundColor(DEFAULT_FOREGROUND_COLOR);
    setDisplayColor(DEFAULT_DISPLAY_COLOR);
    setFontSize(DEFAULT_FONT_SIZE);
    setText("");
  };

  return (
    <Box>
      <Typography variant="h6">Display</Typography>
      <Stack spacing={1} mt={1}>
        <TextField
          style={{ width: "100%" }}
          label="Text"
          variant="outlined"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <Box sx={{ display: "flex", flexWrap: "wrap" }}>
          <ColorSection
            heading="FontColor: "
            color={foregroundColor}
            onChangeColor={setForegroundColor}
          />
          <ColorSection
            heading="DisplayColor: "
            color={displayColor}
            onChangeColor={setDisplayColor}
          />
        </Box>
        <Box
          sx={{
            display: "flex",
            width: "100%",
            alignItems: "center",
            marginBottom: 1,
          }}
        >
          <Typography style={{ width: "20%" }}>font size</Typography>
          <Slider
            style={{ width: "80%" }}
            value={fontSize}
            aria-label="font size"
            defaultValue={DEFAULT_FONT_SIZE}
            step={1}
            marks
            min={1}
            max={7}
            valueLabelDisplay="auto"
            onChange={(_, v) => {
              const nv = v as number;
              setFontSize(nv);
            }}
          />
        </Box>
        <Stack direction="row" spacing={1}>
          <Button type="button" variant="contained" onClick={onSubmit}>
            Send
          </Button>
          <Button type="button" variant="text" onClick={onReset}>
            Reset
          </Button>
        </Stack>
      </Stack>
    </Box>
  );
}
