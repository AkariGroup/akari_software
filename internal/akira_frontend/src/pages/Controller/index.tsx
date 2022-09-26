import {
  Container,
  Grid,
  Stack,
  TextField,
  Button,
  Paper,
  Table,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Switch,
  FormControlLabel,
  Slider,
  Input,
} from "@mui/material";
import { useState } from "react";
import { Joystick } from "react-joystick-component";
import { ColorPicker } from "./ColorPicker";
//TODO: Remove from npm

type Props = {};

export function Controller(props: Props) {
  const [value, setValue] = useState<number | string | Array<number | string>>(
    0
  );

  const handleSliderChange = (event: Event, newValue: number | number[]) => {
    setValue(newValue);
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValue(event.target.value === "" ? "" : Number(event.target.value));
  };

  return (
    <Container maxWidth="xl">
      <Grid container mt={1} spacing={1}>
        <Grid item xl={6}></Grid>
        <Grid item xs={5} md={5} xl={5}>
          <h4>Input</h4>
          <TableContainer component={Paper}>
            <Table sx={{ minWidth: 30 }} aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell
                    width="30%"
                    align="center"
                    style={{ fontWeight: "bold" }}
                  >
                    Button A
                  </TableCell>
                  <TableCell
                    width="30%"
                    align="center"
                    style={{ fontWeight: "bold" }}
                  >
                    Button B
                  </TableCell>
                  <TableCell
                    width="30%"
                    align="center"
                    style={{ fontWeight: "bold" }}
                  >
                    Button C
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell width="30%" align="center">
                    0
                  </TableCell>
                  <TableCell width="30%" align="center">
                    1
                  </TableCell>
                  <TableCell width="30%" align="center">
                    0
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell
                    width="30%"
                    align="center"
                    style={{ fontWeight: "bold" }}
                  >
                    din0
                  </TableCell>
                  <TableCell
                    width="30%"
                    align="center"
                    style={{ fontWeight: "bold" }}
                  >
                    din1
                  </TableCell>
                  <TableCell
                    width="30%"
                    align="center"
                    style={{ fontWeight: "bold" }}
                  >
                    ain0
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell width="30%" align="center">
                    0
                  </TableCell>
                  <TableCell width="30%" align="center">
                    1
                  </TableCell>
                  <TableCell width="30%" align="center">
                    100
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell
                    width="30%"
                    align="center"
                    style={{ fontWeight: "bold" }}
                  >
                    Temperature
                  </TableCell>
                  <TableCell
                    width="30%"
                    align="center"
                    style={{ fontWeight: "bold" }}
                  >
                    Pressure
                  </TableCell>
                  <TableCell
                    width="30%"
                    align="center"
                    style={{ fontWeight: "bold" }}
                  >
                    Brightness
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell width="30%" align="center">
                    25.6
                  </TableCell>
                  <TableCell width="30%" align="center">
                    1014.02
                  </TableCell>
                  <TableCell width="30%" align="center">
                    100
                  </TableCell>
                </TableRow>
              </TableHead>
            </Table>
          </TableContainer>
        </Grid>
      </Grid>
      <Grid container>
        <Grid item xs={7} md={4} xl={2.5}>
          <Grid container mt={1}>
            <h4>Motor control</h4>
          </Grid>
          <div>
            <Joystick size={250} />
          </div>
        </Grid>
        <Grid item xs={5} md={5} xl={2.5}>
          <Grid item xs={9} md={9} xl={9}>
            <Grid container mt={8}></Grid>
            <Stack spacing={2} sx={{ mb: 2 }} alignItems="center">
              <TableContainer component={Paper}>
                <Table sx={{ minWidth: 30 }}>
                  <TableHead>
                    <TableRow>
                      <TableCell align="center" style={{ fontWeight: "bold" }}>
                        Pan
                      </TableCell>
                      <TableCell align="center" style={{ fontWeight: "bold" }}>
                        Tilt
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell align="center">0.34</TableCell>
                      <TableCell align="center">-0.66</TableCell>
                    </TableRow>
                  </TableHead>
                </Table>
              </TableContainer>
            </Stack>
            <Stack direction="row" spacing={2} alignItems="center">
              <TextField
                id="pan"
                label="pan"
                variant="outlined"
                defaultValue="0"
              />
              <TextField
                id="tilt"
                label="tilt"
                variant="outlined"
                defaultValue="0"
              />
            </Stack>
            <Grid container mt={1}>
              <Button align-items="center" type="button" variant="contained">
                Send
              </Button>
            </Grid>
            <Grid container mt={1}>
              <Button align-items="center" type="button" variant="contained">
                Reset
              </Button>
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={6} md={4} xl={2}>
          <Grid container mt={1}>
            <h4>Pinout</h4>
          </Grid>
          <Stack direction="row" sx={{ mb: 2 }}>
            <Grid container mt={1}>
              <FormControlLabel
                sx={{ margin: 0, width: 36 }}
                control={<Switch name="dout0" />}
                label="dout0"
                labelPlacement="top"
              />
              <FormControlLabel
                control={<Switch name="dout1" />}
                label="dout1"
                labelPlacement="top"
              />
            </Grid>
          </Stack>
          pwmout0
          <Stack spacing={2} direction="row" sx={{ mb: 1 }} alignItems="center">
            <Grid item xs={7} md={6} xl={5}>
              <Slider
                aria-label="Volume"
                value={typeof value === "number" ? value : 0}
                onChange={handleSliderChange}
                min={0}
                max={255}
              />
            </Grid>
            <Grid item xs={4} md={3} xl={2}>
              <Input
                value={value}
                size="small"
                onChange={handleInputChange}
                inputProps={{
                  min: 0,
                  max: 255,
                  type: "number",
                  "aria-labelledby": "input-slider",
                }}
              />
            </Grid>
          </Stack>
          <Button align-items="center" type="button" variant="contained">
            Send
          </Button>
          <Grid container mt={1}>
            <Button align-items="center" type="button" variant="contained">
              Reset
            </Button>
          </Grid>
        </Grid>
        <Grid item xs={5} md={4} xl={4}>
          <Grid container mt={1}>
            <h4>Display</h4>
          </Grid>

          <Stack spacing={2} direction="row" sx={{ mb: 1 }} alignItems="center">
            <Grid item xs={9} md={9} xl={7}>
              <ColorPicker />
            </Grid>
            <Grid item xl={3}>
              <Button type="button" variant="contained">
                Send
              </Button>
            </Grid>
          </Stack>
          <Stack spacing={2} direction="row" sx={{ mb: 1 }} alignItems="center">
            <Grid item xs={9} md={9} xl={7}>
              <TextField
                style={{ width: "100%" }}
                id="display"
                label="display text"
                variant="outlined"
              />
            </Grid>
            <Grid item xl={3}>
              <Button type="button" variant="contained">
                Send
              </Button>
            </Grid>
          </Stack>

          <Grid container mt={1}>
            <Button align-items="center" type="button" variant="contained">
              Reset
            </Button>
          </Grid>
        </Grid>
      </Grid>
    </Container>
  );
}
