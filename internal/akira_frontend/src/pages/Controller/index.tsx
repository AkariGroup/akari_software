
import {
    Box,
    Card,
    CardContent,
    Container,
    Divider,
    Grid,
    Stack,
    TextField,
    Button,
    IconButton,
    Link,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Typography,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    Switch,
    FormLabel,
    FormGroup,
    FormHelperText,
    FormControlLabel,
    Slider,
} from "@mui/material";
import { useRef, useState, useCallback } from "react";
import { Joystick } from 'react-joystick-component';
//TODO: Remove from npm
import Webcam from "react-webcam";

type Props = {

};


export function Controller(props: Props) {
    const videoConstraints = {
        width: 720,
        height: 360,
        facingMode: "user"
    };
    const [isCaptureEnable, setCaptureEnable] = useState<boolean>(false);
    const webcamRef = useRef<Webcam>(null);
    const [url, setUrl] = useState<string | null>(null);
    const capture = useCallback(() => {
        const imageSrc = webcamRef.current?.getScreenshot();
        if (imageSrc) {
            setUrl(imageSrc);
        }
    }, [webcamRef]);

    return (
        <Container maxWidth="xl">
            <Grid container mt={2} spacing={3}>
                <Grid item xl={6}>
                    <div>
                        <Webcam
                            audio={false}
                            width={640}
                            height={480}
                            ref={webcamRef}
                            screenshotFormat="image/jpeg"
                            videoConstraints={videoConstraints}
                        />
                    </div>
                </Grid>
                <Grid item xl={3}>
                    <h4>Input</h4>
                    <TableContainer component={Paper}>
                        <Table sx={{ minWidth: 30 }} aria-label="simple table">
                            <TableHead>
                                <TableRow>
                                    <TableCell width='30%' align='center'>Button A</TableCell>
                                    <TableCell width='30%' align='center'>Button B</TableCell>
                                    <TableCell width='30%' align='center'>Button C</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell width='30%' align='center'>0</TableCell>
                                    <TableCell width='30%' align='center'>1</TableCell>
                                    <TableCell width='30%' align='center'>0</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell width='30%' align='center'>din0</TableCell>
                                    <TableCell width='30%' align='center'>din1</TableCell>
                                    <TableCell width='30%' align='center'>ain0</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell width='30%' align='center'>0</TableCell>
                                    <TableCell width='30%' align='center'>1</TableCell>
                                    <TableCell width='30%' align='center'>100</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell width='30%' align='center'>Temperature</TableCell>
                                    <TableCell width='30%' align='center'>Pressure</TableCell>
                                    <TableCell width='30%' align='center'>Brightness</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell width='30%' align='center'>25.6</TableCell>
                                    <TableCell width='30%' align='center'>1014.02</TableCell>
                                    <TableCell width='30%' align='center'>100</TableCell>
                                </TableRow>
                            </TableHead>
                        </Table>
                    </TableContainer>
                </Grid>
            </Grid>
            <Grid container mt={1}>
                <Grid item xl={4.5}>
                    <h4 >Motor control</h4>
                </Grid>
                <Grid item xl={1.5}>
                    <h4>Pinout</h4>
                </Grid>
                <Grid item xl={2}>
                    <h4>Display</h4>
                </Grid>
            </Grid>
            <Grid container mt={1}>
                <Grid item xl={2}>
                    <div>
                        <Joystick size={200} />
                    </div>
                </Grid>
                <Grid item xl={2}>
                    <TableContainer component={Paper}>
                        <Table sx={{ minWidth: 30 }}>
                            <TableRow>
                                <TableCell width='30%'>Pan</TableCell>
                                <TableCell width='30%'>Tilt</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell width='30%'>100</TableCell>
                                <TableCell width='30%'>200</TableCell>
                            </TableRow>
                        </Table>
                    </TableContainer>
                    <TextField sx={{ width: { sm: "40%" } }} id="pan" label="pan" variant="outlined" />
                    &nbsp;
                    <TextField sx={{ width: { sm: "40%" } }} id="tilt" label="tilt" variant="outlined" />
                    <Button
                        type="button"
                        variant="contained"
                    >
                        Send
                    </Button>
                </Grid>

                <Grid item xl={0.5}></Grid>
                <Grid item xl={1.5}>
                    <FormControl component="fieldset" variant="standard">
                        <FormGroup>
                            <FormControlLabel
                                control={
                                    <Switch name="dout0" />
                                }
                                label="dout0"
                            />
                            <FormControlLabel
                                control={
                                    <Switch name="dout1" />
                                }
                                label="dout1"
                            />
                        </FormGroup>
                        <Stack spacing={2} direction="row" sx={{ mb: 1 }} alignItems="center">
                            <Slider aria-label="Volume" />
                        </Stack>
                        pwmout0
                    </FormControl>
                </Grid>
                <Grid item xl={3}>
                    <Grid >
                            <FormControl style={{ width: "80%" }}>
                                <InputLabel id="color">Color</InputLabel>
                                <Select
                                    label="Color"
                                >
                                    <MenuItem value={"Red"}>Red</MenuItem>
                                    <MenuItem value={"Green"}>Green</MenuItem>
                                    <MenuItem value={"Blue"}>Blue</MenuItem>
                                </Select>
                            </FormControl>
                            <Button
                                type="button"
                                variant="contained"
                            >
                                Send
                            </Button>
                    </Grid>
                    <Grid container mt={2}>
                    </Grid>
                    <Grid >
                        <TextField style={{ width: "80%" }} id="display" label="display" variant="outlined" />
                        <Button
                            align-items="center"
                            type="button"
                            variant="contained"
                        >
                            Send
                        </Button>
                    </Grid>
                </Grid>
            </Grid>
        </Container >
    );
}