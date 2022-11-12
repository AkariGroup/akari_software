import useAspidaSWR from "@aspida/swr";
import {
  Box,
  Paper,
  Table,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import React from "react";
import { AkiraControllerClient } from "./client";

type Props = {
  controllerClient: AkiraControllerClient;
};

function DataHeader(props: { children: React.ReactNode }) {
  return (
    <TableCell width="30%" align="center" style={{ fontWeight: "bold" }}>
      {props.children}
    </TableCell>
  );
}

function DataValue(props: { children: React.ReactNode }) {
  return (
    <TableCell width="30%" align="center">
      {props.children}
    </TableCell>
  );
}

function BooleanValue(props: { value?: boolean }) {
  return <>{props.value ? "1" : "0"}</>;
}

export function SensorPanel({ controllerClient }: Props) {
  const { data } = useAspidaSWR(controllerClient.sensor.values, {
    refreshInterval: 100, // in ms
    dedupingInterval: 100, // in ms
  });

  return (
    <Box>
      <Typography variant="h6">Sensor input</Typography>
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 30 }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <DataHeader>Button A</DataHeader>
              <DataHeader>Button B</DataHeader>
              <DataHeader>Button C</DataHeader>
            </TableRow>
            <TableRow>
              <DataValue>
                <BooleanValue value={data?.button_a} />
              </DataValue>
              <DataValue>
                <BooleanValue value={data?.button_b} />
              </DataValue>
              <DataValue>
                <BooleanValue value={data?.button_c} />
              </DataValue>
            </TableRow>
            <TableRow>
              <DataHeader>din0</DataHeader>
              <DataHeader>din1</DataHeader>
              <DataHeader>ain0</DataHeader>
            </TableRow>
            <TableRow>
              <DataValue>
                <BooleanValue value={data?.din0} />
              </DataValue>
              <DataValue>
                <BooleanValue value={data?.din1} />
              </DataValue>
              <DataValue>{data?.ain0}</DataValue>
            </TableRow>
            <TableRow>
              <DataHeader>Temperature</DataHeader>
              <DataHeader>Pressure</DataHeader>
              <DataHeader>Brightness</DataHeader>
            </TableRow>
            <TableRow>
              <DataValue>{data?.temperature.toFixed(2)}</DataValue>
              <DataValue>{data?.pressure.toFixed(0)}</DataValue>
              <DataValue>{data?.brightness.toFixed(0)}</DataValue>
            </TableRow>
          </TableHead>
        </Table>
      </TableContainer>
    </Box>
  );
}
