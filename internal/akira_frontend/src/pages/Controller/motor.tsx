import useAspidaSWR from "@aspida/swr";
import {
  Box,
  Button,
  FormControlLabel,
  Grid,
  InputAdornment,
  Slider,
  Stack,
  Switch,
  TextField,
  Typography,
} from "@mui/material";
import SwapVertIcon from "@mui/icons-material/SwapVert";
import SwapHorizIcon from "@mui/icons-material/SwapHoriz";
import { useState } from "react";
import { Joystick } from "react-joystick-component";
import { AkiraControllerClient } from "./client";
import { DEG2RAD, RAD2DEG } from "../../libs/math";
import { useSetBackdropValue } from "../../contexts/BackdropContext";

type JointControlProps = {
  current?: number;
  target: number;
  onChangeTarget: (v: number) => void;
  name: string;
  icon: React.ReactNode;
  min: number;
  max: number;
  disabled: boolean;
};

function JointControl(props: JointControlProps) {
  return (
    <Stack sx={{ marginBottom: 1 }}>
      <Stack direction="row" alignContent="center">
        <Typography>{props.icon}</Typography>
        &nbsp;
        <Typography>{props.name}</Typography>
        &nbsp;
        <Typography variant="body1" color="textSecondary">
          (Current: {`${props.current?.toFixed(2) ?? "-"} deg`})
        </Typography>
      </Stack>
      <Box sx={{ display: "flex", width: "100%", alignItems: "center" }}>
        <Slider
          sx={{ flexGrow: 1, marginRight: 2 }}
          value={props.target}
          min={props.min}
          max={props.max}
          onChange={(_, v) => {
            const nv = v as number;
            props.onChangeTarget(nv);
          }}
          disabled={props.disabled}
        />
        <TextField
          value={props.target}
          size="small"
          variant="standard"
          type="number"
          InputProps={{
            endAdornment: <InputAdornment position="end">deg</InputAdornment>,
            inputProps: {
              style: { textAlign: "right" },
            },
          }}
          disabled={props.disabled}
          onChange={(e) => {
            if (e.target) {
              props.onChangeTarget(+e.target.value);
            }
          }}
        />
      </Box>
    </Stack>
  );
}

type Props = {
  controllerClient: AkiraControllerClient;
};

export function MotorPanel({ controllerClient }: Props) {
  const { data: servoStatus, mutate: mutateServo } = useAspidaSWR(
    controllerClient.motor.servo,
    {
      refreshInterval: 500, // in ms
      dedupingInterval: 500, // in ms
    }
  );
  const { data: positionData } = useAspidaSWR(
    controllerClient.motor.positions,
    {
      refreshInterval: 100, // in ms
      dedupingInterval: 100, // in ms
    }
  );
  const setBusy = useSetBackdropValue();
  const servoEnabled = servoStatus?.enabled ?? false;

  const toggleServo = async (enabled: boolean) => {
    setBusy(true);
    try {
      await controllerClient.motor.servo.post({
        query: { enabled },
      });
    } finally {
      mutateServo();
      setBusy(false);
    }
  };
  const [panTarget, setPanTarget] = useState<number>(0);
  const [tiltTarget, setTiltTarget] = useState<number>(0);
  const onCurrentClicked = () => {
    if (!positionData) {
      return;
    }

    setPanTarget(+(positionData.pan * RAD2DEG).toFixed(2));
    setTiltTarget(+(positionData.tilt * RAD2DEG).toFixed(2));
  };
  const onReset = () => {
    setPanTarget(0);
    setTiltTarget(0);
  };
  const updateServoPosition = async () => {
    await controllerClient.motor.positions.post({
      body: { pan: panTarget * DEG2RAD, tilt: tiltTarget * DEG2RAD },
    });
  };

  return (
    <Box>
      <Typography variant="h6">Joint</Typography>
      <Box mb={3}>
        <FormControlLabel
          control={
            <Switch
              checked={servoEnabled}
              onChange={(_, v) => toggleServo(v)}
            />
          }
          label="Servo"
          value={!servoEnabled}
        />
      </Box>
      <Grid container spacing={3}>
        <Grid item xs={12} lg="auto" >
          <Joystick size={250} disabled={!servoEnabled} />
        </Grid>
        <Grid item xs={12} lg>
          <Stack>
            <JointControl
              name="Pan"
              current={positionData && positionData.pan * RAD2DEG}
              target={panTarget}
              onChangeTarget={setPanTarget}
              icon={<SwapHorizIcon />}
              min={-2.355 * RAD2DEG}
              max={2.355 * RAD2DEG}
              disabled={!servoEnabled}
            />
            <JointControl
              name="Tilt"
              current={positionData && positionData.tilt * RAD2DEG}
              target={tiltTarget}
              onChangeTarget={setTiltTarget}
              icon={<SwapVertIcon />}
              min={-0.91 * RAD2DEG}
              max={0.91 * RAD2DEG}
              disabled={!servoEnabled}
            />
            <Stack direction="row" spacing={1}>
              <Button
                type="button"
                variant="contained"
                onClick={updateServoPosition}
                disabled={!servoEnabled}
              >
                Send
              </Button>
              <Button
                type="button"
                variant="text"
                onClick={onCurrentClicked}
                disabled={!servoEnabled}
              >
                Current
              </Button>
              <Button
                type="button"
                variant="text"
                onClick={onReset}
                disabled={!servoEnabled}
              >
                Reset
              </Button>
            </Stack>
          </Stack>
        </Grid>
      </Grid>
    </Box>
  );
}
