
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
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    Switch,
    FormGroup,
    FormControlLabel,
    Slider,
    Input,
    Box,
} from "@mui/material";
import { useRef, useState, useCallback } from "react";
import { Joystick } from 'react-joystick-component';
//TODO: Remove from npm
import Webcam from "react-webcam";

type Props = {

};

function valuetext(value: number) {
    return `${value}°C`;
}

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
    const [value, setValue] = useState<number | string | Array<number | string>>(
        0,
    );

    const handleSliderChange = (event: Event, newValue: number | number[]) => {
        setValue(newValue);
    };

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setValue(event.target.value === '' ? '' : Number(event.target.value));
    };

    return (
        <Container maxWidth="xl">
            <Grid container mt={1} spacing={1}>
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
                <Grid item xl={5}>
                    <h4>Input</h4>
                    <TableContainer component={Paper}>
                        <Table sx={{ minWidth: 30 }} aria-label="simple table">
                            <TableHead>
                                <TableRow>
                                    <TableCell width='30%' align='center' style={{ fontWeight: 'bold' }}>Button A</TableCell>
                                    <TableCell width='30%' align='center' style={{ fontWeight: 'bold' }}>Button B</TableCell>
                                    <TableCell width='30%' align='center' style={{ fontWeight: 'bold' }}>Button C</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell width='30%' align='center'>0</TableCell>
                                    <TableCell width='30%' align='center'>1</TableCell>
                                    <TableCell width='30%' align='center'>0</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell width='30%' align='center' style={{ fontWeight: 'bold' }}>din0</TableCell>
                                    <TableCell width='30%' align='center' style={{ fontWeight: 'bold' }}>din1</TableCell>
                                    <TableCell width='30%' align='center' style={{ fontWeight: 'bold' }}>ain0</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell width='30%' align='center'>0</TableCell>
                                    <TableCell width='30%' align='center'>1</TableCell>
                                    <TableCell width='30%' align='center'>100</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell width='30%' align='center' style={{ fontWeight: 'bold' }}>Temperature</TableCell>
                                    <TableCell width='30%' align='center' style={{ fontWeight: 'bold' }}>Pressure</TableCell>
                                    <TableCell width='30%' align='center' style={{ fontWeight: 'bold' }}>Brightness</TableCell>
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
                <Grid item xl={2.5}>
                    <Grid container mt={1}>
                        <h4 >Motor control</h4>
                    </Grid>
                    <div>
                        <Joystick size={250} />
                    </div>
                </Grid>
                <Grid item xl={2.5}>
                    <Grid item xl={9}>
                        <Grid container mt={9}>
                        </Grid>
                        <Grid container mt={1}>
                            <TextField id="pan" label="pan" variant="outlined" defaultValue="0" />
                        </Grid>
                        <Grid container mt={1}>
                            <TextField id="tilt" label="tilt" variant="outlined" defaultValue="0" />
                        </Grid>
                        <Grid container mt={1}>
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
                <Grid item xl={2}>
                    <Grid container mt={1}>
                        <h4 >Pinout</h4>
                    </Grid>
                    <FormControl>
                        <FormGroup row>
                            <FormControlLabel
                                control={
                                    <Switch name="dout0" />
                                }
                                label="dout0"
                                labelPlacement="top"
                            />
                            <FormControlLabel
                                control={
                                    <Switch name="dout1" />
                                }
                                label="dout1"
                                labelPlacement="top"
                            />
                        </FormGroup>
                        pwmout0
                        <Stack spacing={2} direction="row" sx={{ mb: 2 }} alignItems="center">
                            <Slider aria-label="Volume"
                                value={typeof value === 'number' ? value : 0}
                                onChange={handleSliderChange}
                                min={0}
                                max={255}
                            />
                            <Input
                                value={value}
                                size="small"
                                onChange={handleInputChange}
                                inputProps={{
                                    min: 0,
                                    max: 255,
                                    type: 'number',
                                    'aria-labelledby': 'input-slider',
                                }}
                            />
                        </Stack>
                        <Button
                            align-items="center"
                            type="button"
                            variant="contained"
                        >
                            Send
                        </Button>
                    </FormControl>
                </Grid>
                <Grid item xl={5}>
                    <Grid container mt={1}>
                        <h4 >Display</h4>
                    </Grid>
                    <Grid container direction="row" alignItems="center">
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
                        &nbsp;
                       <Button
                            type="button"
                            variant="contained"
                        >
                            Send
                        </Button>
                    </Grid>
                    <Grid container mt={2}>
                    </Grid>
                    <Grid container direction="row" alignItems="center">
                        <TextField style={{ width: "80%" }} id="display" label="display" variant="outlined" />
                        &nbsp;
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