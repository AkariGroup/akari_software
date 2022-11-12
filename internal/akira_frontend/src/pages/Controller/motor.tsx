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

const JOYSTICK_CONTROL_HZ = 10;
const JOYSTICK_CONTROL_MS = 1000 / JOYSTICK_CONTROL_HZ;

// max speed is 100 deg/s
const JOYSTICK_GAIN = (100 / JOYSTICK_CONTROL_HZ) * DEG2RAD;
const MIN_VEL = 10;
const MAX_VEL = 1800;
const MIN_ACC = 1;
const MAX_ACC = 10;

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
  const [initialFetch, setInitialFetch] = useState<boolean>(false);
  const pan_min = servoStatus?.pan_min ?? -1.047;
  const pan_max = servoStatus?.pan_max ?? 1.047;
  const tilt_min = servoStatus?.tilt_min ?? -0.576;
  const tilt_max = servoStatus?.tilt_max ?? 0.576;
  const [vel, setVel] = useState<number>(0);
  const [acc, setAcc] = useState<number>(0);

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
  const sendAbsolutePosition = async () => {
    await controllerClient.motor.positions.post({
      body: { pan: panTarget * DEG2RAD, tilt: tiltTarget * DEG2RAD },
    });
  };
  const sendRelativePosition = async (x: number, y: number, amount: number) => {
    if (!positionData) return;
    const theta = Math.atan2(y, x);
    const coeff = Math.pow(amount / 100.0, 2) * JOYSTICK_GAIN;

    const relX = Math.cos(theta) * coeff;
    const relY = Math.sin(theta) * coeff;
    controllerClient.motor.positions.post({
      body: { pan: positionData.pan + relX, tilt: positionData.tilt + relY },
    });
  };
  const sendVel = async (val: number) => {
    val = Math.floor(val);
    setVel(val);
    controllerClient.motor.velocity.post({
      query: { vel: val * DEG2RAD },
    });
  };
  const sendAcc = async (val: number) => {
    val = Math.floor(val);
    setAcc(val);
    controllerClient.motor.acceleration.post({
      query: { acc: acc * DEG2RAD },
    });
  };

  function CheckInitialFetch() {
    if (!initialFetch && servoStatus) {
      setVel(Math.floor(servoStatus.vel * RAD2DEG));
      setAcc(Math.floor(servoStatus.acc * RAD2DEG));
      setInitialFetch(true);
    }
    return <></>;
  }

  return (
    <Box>
      <CheckInitialFetch />
      <Typography variant="h6">Joint</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} lg="auto">
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
          <Joystick
            size={250}
            disabled={!servoEnabled}
            throttle={JOYSTICK_CONTROL_MS}
            move={(e) => {
              if (!e.x || !e.y || !e.distance) return;
              sendRelativePosition(e.x, e.y, e.distance);
            }}
          />
        </Grid>
        <Grid item xs={12} lg>
          <Grid container spacing={3}>
            <Grid item xs={6} lg>
              <Typography>&nbsp;Vel&nbsp;</Typography>
              <Slider
                sx={{ flexGrow: 1, marginRight: 2 }}
                value={vel}
                min={MIN_VEL}
                max={MAX_VEL}
                disabled={!servoEnabled}
                onChange={(_, v) => {
                  const nv = v as number;
                  sendVel(nv);
                }}
              />
              <TextField
                value={vel}
                disabled={!servoEnabled}
                size="small"
                variant="standard"
                type="number"
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">deg/s</InputAdornment>
                  ),
                  inputProps: {
                    style: { textAlign: "right" },
                    step: "1",
                  },
                }}
                onChange={(e) => {
                  if (e.target) {
                    sendVel(+e.target.value);
                  }
                }}
              />
            </Grid>
            <Grid item xs={6} lg>
              <Typography>&nbsp;&nbsp;Acc&nbsp;</Typography>
              <Slider
                sx={{ flexGrow: 1, marginRight: 2 }}
                value={acc}
                min={MIN_ACC}
                max={MAX_ACC}
                disabled={!servoEnabled}
                onChange={(_, v) => {
                  const nv = v as number;
                  sendAcc(nv);
                }}
              />
              <TextField
                value={acc}
                disabled={!servoEnabled}
                size="small"
                variant="standard"
                type="number"
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">deg/s2</InputAdornment>
                  ),
                  inputProps: {
                    style: { textAlign: "right" },
                    step: "1",
                  },
                }}
                onChange={(e) => {
                  if (e.target) {
                    sendAcc(+e.target.value);
                  }
                }}
              />
            </Grid>
          </Grid>
          <Stack>
            <JointControl
              name="Pan"
              current={positionData && positionData.pan * RAD2DEG}
              target={panTarget}
              onChangeTarget={setPanTarget}
              icon={<SwapHorizIcon />}
              min={pan_min * RAD2DEG}
              max={pan_max * RAD2DEG}
              disabled={!servoEnabled}
            />
            <JointControl
              name="Tilt"
              current={positionData && positionData.tilt * RAD2DEG}
              target={tiltTarget}
              onChangeTarget={setTiltTarget}
              icon={<SwapVertIcon />}
              min={tilt_min * RAD2DEG}
              max={tilt_max * RAD2DEG}
              disabled={!servoEnabled}
            />
            <Stack direction="row" spacing={1}>
              <Button
                type="button"
                variant="contained"
                onClick={sendAbsolutePosition}
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
