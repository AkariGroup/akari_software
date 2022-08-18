
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
                <Grid item xl={6}>
                    <TableContainer component={Paper}>
                        <Table sx={{ minWidth: 30 }} aria-label="simple table">
                            <TableHead>
                                <TableRow>
                                    <TableCell>din0</TableCell>
                                    <TableCell>din1</TableCell>
                                    <TableCell>ain0</TableCell>
                                    <TableCell>Temperature</TableCell>
                                    <TableCell>Pressure</TableCell>
                                    <TableCell>Brightness</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell>0</TableCell>
                                    <TableCell>1</TableCell>
                                    <TableCell>100</TableCell>
                                    <TableCell>25.6</TableCell>
                                    <TableCell>1014.02</TableCell>
                                    <TableCell>100</TableCell>
                                </TableRow>
                            </TableHead>
                        </Table>
                    </TableContainer>
                </Grid>
            </Grid>
            <Grid container mt={2} spacing={3}>
                <Grid item xl={2}>
                    <div>
                        <Joystick size={200} />
                    </div>
                </Grid>
                <Grid item xl={3}>
                    <TableContainer component={Paper}>
                        <Table sx={{ minWidth: 30 }} aria-label="simple table">
                            <TableHead>
                                <TableRow>
                                    <TableCell>Pan</TableCell>
                                    <TableCell>100</TableCell>
                                    <TableCell>Tilt</TableCell>
                                    <TableCell>200</TableCell>
                                </TableRow>
                            </TableHead>
                        </Table>
                    </TableContainer>
                    <TextField id="pan" label="pan" variant="outlined" />
                    <TextField id="tilt" label="tilt" variant="outlined" />
                    <Button
                        type="button"
                        variant="contained"
                    >
                        Send
                    </Button>
                </Grid>
                <Grid item xl={3}>
                    <FormControl component="fieldset" variant="standard">
                        <FormLabel component="legend">GPIO pinout</FormLabel>
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
                    <FormControl fullWidth>
                        <InputLabel id="demo-simple-select-label">Color</InputLabel>
                        <Select
                            labelId="demo-simple-select-label"
                            id="demo-simple-select"
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
                    <TextField id="display" label="display" variant="outlined" />
                    <Button
                        type="button"
                        variant="contained"
                    >
                        Send
                    </Button>
                </Grid>
                <Grid item xl={3}>
                </Grid>
            </Grid>
        </Container >
    );
}