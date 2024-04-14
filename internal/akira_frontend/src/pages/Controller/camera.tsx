import useAspidaSWR from "@aspida/swr";
import {
  Stack,
  ToggleButton,
  ToggleButtonGroup,
  Typography,
} from "@mui/material";
import { Box } from "@mui/system";
import { useSetBackdropValue } from "../../contexts/BackdropContext";
import { CaptureMode } from "../../service-apis/akira-controller-server/@types";
import { AkiraControllerClient } from "./client";

type Props = {
  controllerClient: AkiraControllerClient;
};

export function CameraPanel(props: Props) {
  const { data, mutate } = useAspidaSWR(props.controllerClient.camera.mode);
  const setBusy = useSetBackdropValue();
  const url = props.controllerClient.camera.stream.$path();
  const onModeChange = async (mode: CaptureMode) => {
    setBusy(true);
    try {
      await props.controllerClient.camera.mode.post({
        body: {
          mode,
        },
      });
      mutate();
    } finally {
      setBusy(false);
    }
  };

  return (
    <Box>
      <Typography variant="h6">Camera</Typography>
      <Stack>
        <Box mb={1}>
          <ToggleButtonGroup
            color="primary"
            exclusive
            value={data?.mode}
            size="small"
            onChange={(_, v: string) => {
              if (v !== null) {
                onModeChange(v as CaptureMode);
              }
            }}
          >
            <ToggleButton value="None">None</ToggleButton>
            <ToggleButton value="RGB">RGB</ToggleButton>
            <ToggleButton value="Depth">Depth</ToggleButton>
            <ToggleButton value="FaceDetection">FaceDetection</ToggleButton>
            <ToggleButton value="ObjectDetection">ObjectDetection</ToggleButton>
          </ToggleButtonGroup>
        </Box>
        <Box
          component="img"
          src={url}
          sx={{
            maxHeight: "40vh",
            objectFit: "contain",
          }}
        />
      </Stack>
    </Box>
  );
}
