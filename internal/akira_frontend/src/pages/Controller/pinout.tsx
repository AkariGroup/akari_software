import {
  Box,
  Button,
  FormControlLabel,
  Slider,
  Stack,
  Switch,
  TextField,
  Typography,
} from "@mui/material";
import { useState } from "react";
import { AkiraControllerClient } from "./client";

type Props = {
  controllerClient: AkiraControllerClient;
};

export function PinoutPanel(props: Props) {
  const [dout0, setDout0] = useState<boolean>(false);
  const [dout1, setDout1] = useState<boolean>(false);
  const [pwmout0, setPwmout0] = useState<number>(0);

  const onSubmit = async () => {
    await props.controllerClient.pinout.values.post({
      body: {
        dout0,
        dout1,
        pwmout0,
      },
    });
  };
  const onReset = () => {
    setDout0(false);
    setDout1(false);
    setPwmout0(0);
  };

  return (
    <Stack>
      <Typography variant="h6">Pinout</Typography>
      <Stack direction="row">
        <FormControlLabel
          control={<Switch checked={dout0} onChange={(_, v) => setDout0(v)} />}
          label="dout0"
        />
        <FormControlLabel
          control={<Switch checked={dout1} onChange={(_, v) => setDout1(v)} />}
          label="dout1"
        />
      </Stack>
      <Box
        sx={{
          display: "flex",
          width: "100%",
          alignItems: "center",
          marginBottom: 1,
        }}
      >
        <Typography>pwmout0</Typography>
        <Slider
          sx={{ flexGrow: 1, marginLeft: 2, marginRight: 2 }}
          value={pwmout0}
          min={0}
          max={255}
          onChange={(_, v) => {
            const nv = v as number;
            setPwmout0(nv);
          }}
        />
        <TextField
          value={pwmout0}
          size="small"
          variant="standard"
          type="number"
          InputProps={{
            inputProps: {
              style: { textAlign: "right" },
            },
          }}
          onChange={(e) => {
            if (e.target) {
              setPwmout0(+e.target.value);
            }
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
  );
}
