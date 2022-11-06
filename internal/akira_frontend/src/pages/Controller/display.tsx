import { Box, Button, Stack, TextField, Typography } from "@mui/material";
import { useState } from "react";
import { RGBColor } from "react-color";
import { ColorPicker } from "../../components/ColorPicker";
import { AkiraControllerClient } from "./client";

type Props = {
  controllerClient: AkiraControllerClient;
};

const DEFAULT_BACKGROUND_COLOR: RGBColor = {
  r: 255,
  g: 255,
  b: 255,
};

export function DisplayPanel(props: Props) {
  const [backgroundColor, setBackgroundColor] = useState<RGBColor>(
    () => DEFAULT_BACKGROUND_COLOR
  );
  const [text, setText] = useState<string>("");

  const onSubmit = async () => {
    await props.controllerClient.display.values.post({
      body: {
        text: text,
        bg_color: backgroundColor,
      },
    });
  };
  const onReset = () => {
    setBackgroundColor(DEFAULT_BACKGROUND_COLOR);
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
        <Stack direction="row" spacing={1} alignItems="center">
          <Typography>Background: </Typography>
          <ColorPicker
            text="&nbsp;"
            color={backgroundColor}
            onChangeColor={setBackgroundColor}
          />
        </Stack>
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
