import { Container, Grid } from "@mui/material";
import { CameraPanel } from "./camera";
import { useAkiraControllerClient } from "./client";
import { DisplayPanel } from "./display";
import { MotorPanel } from "./motor";
import { PinoutPanel } from "./pinout";
import { SensorPanel } from "./sensors";
import { useTheme } from "@mui/material/styles";
import useMediaQuery from "@mui/material/useMediaQuery";
import * as React from "react";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import { TabPanel } from "../../components/ControllerTabPanel";

type Props = {};

export function Controller(props: Props) {
  const theme = useTheme();
  const matches = useMediaQuery(theme.breakpoints.up("md"));
  const controllerClient = useAkiraControllerClient();

  const [upper_tab_value, setUpperValue] = React.useState(0);
  const [lower_tab_value, setLowerValue] = React.useState(0);
  const handleUpperChange = (event: React.SyntheticEvent, newValue: number) => {
    setUpperValue(newValue);
  };
  const handleLowerChange = (event: React.SyntheticEvent, newValue: number) => {
    setLowerValue(newValue);
  };

  if (matches) {
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
  } else {
    return (
      <Container maxWidth={false}>
        <Grid container mt={1} spacing={2}>
          <Tabs
            value={upper_tab_value}
            onChange={handleUpperChange}
            aria-label="upper_tab"
          >
            <Tab label="Camera" />
            <Tab label="Sensors" />
          </Tabs>
        </Grid>
        <Grid container mt={1} spacing={2}>
          <TabPanel value={upper_tab_value} index={0}>
            <CameraPanel controllerClient={controllerClient} />
          </TabPanel>
          <TabPanel value={upper_tab_value} index={1}>
            <SensorPanel controllerClient={controllerClient} />
          </TabPanel>
        </Grid>
        <Grid container mt={1} spacing={2}>
          <Tabs
            value={lower_tab_value}
            onChange={handleLowerChange}
            aria-label="lower_tab"
          >
            <Tab label="Motor" />
            <Tab label="Pinout" />
            <Tab label="Display" />
          </Tabs>
        </Grid>
        <Grid container mt={1} spacing={2}>
          <TabPanel value={lower_tab_value} index={0}>
            <MotorPanel controllerClient={controllerClient} />
          </TabPanel>
          <TabPanel value={lower_tab_value} index={1}>
            <PinoutPanel controllerClient={controllerClient} />
          </TabPanel>
          <TabPanel value={lower_tab_value} index={2}>
            <DisplayPanel controllerClient={controllerClient} />
          </TabPanel>
        </Grid>
      </Container>
    );
  }
}
