import { Box, Button, Stack, TextField, Typography } from "@mui/material";
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
  const [text, setText] = useState<string>("");

  const onSubmit = async () => {
    await props.controllerClient.display.values.post({
      body: {
        text: text,
        display_color: displayColor,
        foreground_color: foregroundColor,
      },
    });
  };
  const onReset = () => {
    setForegroundColor(DEFAULT_FOREGROUND_COLOR);
    setDisplayColor(DEFAULT_DISPLAY_COLOR);
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
