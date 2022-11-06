import { Container, Grid } from "@mui/material";
import { CameraPanel } from "./camera";
import { useAkiraControllerClient } from "./client";
import { DisplayPanel } from "./display";
import { MotorPanel } from "./motor";
import { PinoutPanel } from "./pinout";
import { SensorPanel } from "./sensors";

type Props = {};

export function Controller(props: Props) {
  const controllerClient = useAkiraControllerClient();

  return (
    <Container maxWidth={false}>
      <Grid container mt={1} spacing={2}>
        <Grid item sm={12} md={6}>
          <CameraPanel controllerClient={controllerClient} />
        </Grid>
        <Grid item sm={12} md={6}>
          <SensorPanel controllerClient={controllerClient} />
        </Grid>
        <Grid item sm={12} md={6}>
          <MotorPanel controllerClient={controllerClient} />
        </Grid>
        <Grid item sm={12} md={3}>
          <PinoutPanel controllerClient={controllerClient} />
        </Grid>
        <Grid item sm={12} md={3}>
          <DisplayPanel controllerClient={controllerClient} />
        </Grid>
      </Grid>
    </Container>
  );
}
